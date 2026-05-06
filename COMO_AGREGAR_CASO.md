# Cómo agregar un nuevo caso de prueba

Esta guía explica paso a paso cómo agregar un nuevo escenario de prueba sobre la app AppiumDemo, siguiendo el patrón POM del proyecto.

---

## Antes de empezar

Identifica en la app la pantalla que vas a automatizar. Para eso usa **Appium Inspector** o el **Layout Inspector** de Android Studio mientras la app está abierta en el emulador.

Lo que necesitas anotar de cada elemento:
- `resource-id` → se usa con `AppiumBy.ID`
- `content-desc` → se usa con `AppiumBy.ACCESSIBILITY_ID`
- `text` → se usa con `AppiumBy.XPATH` (último recurso)

Ejemplo de lo que verías en Appium Inspector:
```
resource-id: io.appium.android.apis:id/mi_elemento
content-desc: Mi Elemento
```

---

## Paso 1 — Decide si necesitas un Page Object nuevo

Pregúntate: ¿la pantalla que voy a automatizar ya tiene un Page Object en `pages/`?

```
pages/
  home_page.py          ← pantalla principal
  app_page.py           ← submenú App
  search_page.py        ← submenú Search
  invoke_search_page.py ← pantalla Invoke Search
  fragment_page.py      ← submenú Fragment
  nesting_tabs_page.py  ← pantalla Nesting Tabs
```

- **Si ya existe** → ve al Paso 3 directamente.
- **Si no existe** → crea uno nuevo en el Paso 2.

---

## Paso 2 — Crear el Page Object de la nueva pantalla

Crea el archivo en `pages/nombre_pantalla.py`. Sigue exactamente esta estructura:

```python
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class NombrePantallaPage(BasePage):
    """Page Object de la pantalla NombrePantalla."""

    # 1. Define los localizadores como atributos privados de clase
    _ELEMENTO_PRINCIPAL = (AppiumBy.ACCESSIBILITY_ID, "Texto del elemento")
    _BOTON_ACCION       = (AppiumBy.ID, "io.appium.android.apis:id/id_del_boton")

    def is_displayed(self) -> bool:
        """Verifica que esta pantalla está visible."""
        return self.is_element_present(self._ELEMENTO_PRINCIPAL)

    def hacer_accion(self) -> "NombrePantallaPage":
        """Descripción de la acción. Retorna self para encadenamiento."""
        self.wait_and_click(self._BOTON_ACCION)
        return self

    def ir_a_siguiente_pantalla(self):
        """Navega a la siguiente pantalla y retorna su Page Object."""
        from pages.siguiente_pantalla_page import SiguientePantallaPage
        self.wait_and_click(self._BOTON_ACCION)
        return SiguientePantallaPage(self.driver)

    def volver(self):
        """Vuelve a la pantalla anterior."""
        from pages.pantalla_anterior_page import PantallaAnteriorPage
        self.driver.back()
        return PantallaAnteriorPage(self.driver)
```

### Reglas del Page Object

| Regla | Correcto | Incorrecto |
|---|---|---|
| Localizadores | Atributos privados de clase (`_NOMBRE`) | Strings sueltos en los métodos |
| Métodos de navegación | Retornan el Page Object destino | Retornan `None` |
| Métodos de acción | Retornan `self` para encadenamiento | No retornan nada |
| Esperas | Usan `wait_and_click` o `wait_for_element` de `BasePage` | Usan `time.sleep()` |
| Imports de otros Page Objects | Dentro del método (import local) | Al inicio del archivo |

### Métodos disponibles en BasePage

```python
self.wait_and_click(locator, timeout=10)      # Espera y hace click
self.wait_for_element(locator, timeout=10)    # Espera y retorna el elemento
self.is_element_present(locator, timeout=5)   # Retorna True/False
```

---

## Paso 3 — Agregar navegación desde la pantalla anterior

Si la nueva pantalla se accede desde una pantalla existente, agrega el método de navegación en ese Page Object.

Ejemplo: si la nueva pantalla se accede desde `AppPage`, edita `pages/app_page.py`:

```python
# Agrega el localizador
_MI_NUEVA_OPCION = (AppiumBy.ACCESSIBILITY_ID, "Mi Nueva Opción")

# Agrega el método de navegación
def go_to_nueva_pantalla(self):
    """Navega a la nueva pantalla."""
    from pages.nombre_pantalla_page import NombrePantallaPage
    self.wait_and_click(self._MI_NUEVA_OPCION)
    return NombrePantallaPage(self.driver)
```

---

## Paso 4 — Crear el escenario en `scenarios.py`

Agrega una función nueva al final de `scenarios.py`. Cada escenario recibe el `driver` y ejecuta el flujo completo:

```python
def scenario_mi_nuevo_caso(driver):
    """Descripción breve del escenario."""
    home = HomePage(driver)

    with allure.step("Navegar a App > Mi Nueva Opción"):
        nueva_pantalla = (
            home
            .go_to_app()
            .go_to_nueva_pantalla()
        )

    with allure.step("Realizar la acción principal"):
        nueva_pantalla.hacer_accion()

    with allure.step("Volver y verificar pantalla anterior"):
        pantalla_anterior = nueva_pantalla.volver()
        assert pantalla_anterior.is_displayed(), "La pantalla anterior no está visible"
```

### Buenas prácticas para los pasos Allure

- Cada `with allure.step(...)` debe describir **qué hace el usuario**, no cómo lo hace el código
- Usa verbos de acción: "Navegar a", "Introducir", "Seleccionar", "Verificar"
- El último paso siempre debe ser una verificación con `assert`

---

## Paso 5 — Agregar el test en los archivos de prueba

### Para ejecución local — `test/test_appiumdemo.py`

```python
from scenarios import scenario_mi_nuevo_caso   # agregar al import existente

@allure.feature("AppiumDemo - Mi Feature")
@allure.story("Descripción del escenario")
@allure.tag("local")
def test_mi_nuevo_caso(driver):
    scenario_mi_nuevo_caso(driver)
```

### Para ejecución en Sauce Labs — `test/test_appiumdemo_saucelabs.py`

```python
from scenarios import scenario_mi_nuevo_caso   # agregar al import existente

@allure.feature("AppiumDemo - Mi Feature")
@allure.story("Descripción del escenario")
@allure.tag("saucelabs")
def test_mi_nuevo_caso_sl(driver_saucelabs):
    scenario_mi_nuevo_caso(driver_saucelabs)
```

> Nota: el test local usa el fixture `driver` y el de Sauce Labs usa `driver_saucelabs`. El escenario en `scenarios.py` es el mismo para ambos.

---

## Paso 6 — Verificar que todo funciona

```bash
# Activa el entorno virtual
venv\Scripts\activate

# Ejecuta solo el nuevo test en local
pytest test/test_appiumdemo.py::test_mi_nuevo_caso -v --alluredir=allure-results

# Ver el reporte
allure serve allure-results
```

---

## Resumen del flujo completo

```
1. Identificar elementos en Appium Inspector
        ↓
2. Crear pages/nombre_pantalla.py  (si la pantalla es nueva)
        ↓
3. Agregar método de navegación en el Page Object anterior
        ↓
4. Agregar función scenario_xxx() en scenarios.py
        ↓
5. Agregar test en test_appiumdemo.py  (local)
   Agregar test en test_appiumdemo_saucelabs.py  (Sauce Labs)
        ↓
6. Ejecutar y verificar con Allure
```

---

## Ejemplo completo — caso real de referencia

Para ver un ejemplo completo ya implementado, revisa:

- **Page Object**: `pages/invoke_search_page.py`
- **Escenario**: función `scenario_invoke_search_and_back_home` en `scenarios.py`
- **Test local**: `test_invoke_search_and_back_home` en `test/test_appiumdemo.py`
- **Test Sauce Labs**: `test_invoke_search_and_back_home_sl` en `test/test_appiumdemo_saucelabs.py`
