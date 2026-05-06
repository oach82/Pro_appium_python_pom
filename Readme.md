# Appium Python — POM + Sauce Labs

Suite de automatización móvil Android con Appium y Python, estructurada bajo el patrón **Page Object Model (POM)** con soporte para ejecución local y en **Sauce Labs**.

---

## Tecnologías

| Herramienta | Uso |
|---|---|
| Python 3.10+ | Lenguaje base |
| Appium 2.x | Servidor de automatización móvil |
| UIAutomator2 | Driver Android |
| pytest | Framework de pruebas |
| allure-pytest | Reportes con evidencia visual |
| hypothesis | Property-based testing |
| python-dotenv | Gestión de credenciales via `.env` |
| Sauce Labs | Ejecución en la nube (us-west-1) |

---

## Estructura del proyecto (POM)

```
proyecto/
│
├── pages/                        # Capa de Page Objects
│   ├── __init__.py
│   ├── base_page.py              # Clase base con utilidades de espera
│   ├── home_page.py              # Pantalla principal de ApiDemos
│   ├── app_page.py               # Submenú App
│   ├── search_page.py            # Submenú Search
│   ├── invoke_search_page.py     # Pantalla Invoke Search
│   ├── fragment_page.py          # Submenú Fragment
│   └── nesting_tabs_page.py      # Pantalla Nesting Tabs
│
├── test/                          # Capa de pruebas
│   ├── test_appiumdemo.py         # Tests para ejecución LOCAL
│   ├── test_appiumdemo_saucelabs.py # Tests para ejecución SAUCE LABS
│   ├── test_config_properties.py  # Property-based tests de Config
│   └── scenarios.py               # Escenarios compartidos entre entornos
│
├── apps/
│   └── ApiDemos-debug.apk        # APK bajo prueba
│
├── config.py                     # Clase Config (local / saucelabs)
├── conftest.py                   # Fixtures driver y driver_saucelabs
├── scenarios.py                  # Lógica de escenarios reutilizable
├── pytest.ini                    # Configuración de pytest y marks
├── .env                          # Credenciales (NO subir al repo)
├── .env.example                  # Plantilla de variables de entorno
├── requirements.txt              # Dependencias Python
└── Readme.md
```

### Responsabilidades por capa

- **`pages/`** — encapsula localizadores e interacciones de UI. Los tests nunca acceden directamente a elementos.
- **`config.py`** — decide el entorno (local o Sauce Labs) y construye las capabilities del driver.
- **`conftest.py`** — provee los fixtures `driver` (local) y `driver_saucelabs`.
- **`scenarios.py`** — contiene la lógica de cada escenario, reutilizable en ambos entornos.
- **`test/`** — orquesta los escenarios y declara aserciones.

---

## Prerrequisitos

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd <nombre-del-proyecto>
```

### 2. Crear y activar entorno virtual Python

```bash
# Crear el entorno virtual
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Mac/Linux
source venv/bin/activate
```

> Sabrás que está activo cuando el prompt muestre `(venv)` al inicio.

### 3. Instalar dependencias del proyecto

```bash
pip install -r requirements.txt
```

### 4. Validar instalación

```bash
python --version
pytest --version
appium --version
```

### Appium (Node.js requerido)

```bash
npm install -g appium
appium driver install uiautomator2
appium -v
```

### Android SDK

1. Instala Android Studio desde https://developer.android.com/studio
2. En **SDK Manager** activa:
   - Android SDK Build-Tools
   - Android SDK Platform-Tools
   - Android SDK Command-line Tools (latest)
3. Configura variables de entorno:

```
ANDROID_HOME = C:\Users\USUARIO\AppData\Local\Android\Sdk

Path (agregar):
  %ANDROID_HOME%\platform-tools
  %ANDROID_HOME%\emulator
  %ANDROID_HOME%\cmdline-tools\latest\bin
```

4. Valida:

```bash
adb devices
emulator -list-avds
```

---

## Configuración del archivo `.env`

Copia `.env.example` como `.env` y completa los valores:

```bash
copy .env.example .env
```

Contenido del `.env`:

```env
# Entorno: local | saucelabs
APPIUM_ENV=local

# Solo necesario cuando APPIUM_ENV=saucelabs
SAUCE_USERNAME=tu_usuario
SAUCE_ACCESS_KEY=tu_access_key
```

> **Importante:** nunca subas `.env` al repositorio. Agrega `.env` a tu `.gitignore`.

---

## Ejecución de pruebas

> Asegúrate de tener el entorno virtual activado antes de correr cualquier comando:
> ```bash
> # Windows
> venv\Scripts\activate
> # Mac/Linux
> source venv/bin/activate
> ```

### Local

Requisitos previos:
- Emulador `Pixel_9` corriendo: `emulator -avd Pixel_9`
- Servidor Appium corriendo: `appium`

```bash
# Asegúrate que .env tiene APPIUM_ENV=local
pytest test/test_appiumdemo.py -v --alluredir=allure-results
```

### Sauce Labs

Requisitos previos:
- APK subido al storage de Sauce Labs
- Credenciales en `.env`

```bash
# Cambia en .env: APPIUM_ENV=saucelabs y completa SAUCE_USERNAME y SAUCE_ACCESS_KEY
pytest test/test_appiumdemo_saucelabs.py -v --alluredir=allure-results
```

### Property-based tests (sin driver)

```bash
pytest test/test_config_properties.py -v
```

### Todos los tests

```bash
pytest -v --alluredir=allure-results
```

---

## Reporte Allure

```bash
allure serve allure-results
```

Abre el navegador automáticamente con:
- Pasos de cada test
- Screenshot al finalizar cada test
- Screenshot del estado en caso de fallo
- Duración y estado por escenario

---

## Ver resultados en Sauce Labs

1. Entra a https://app.saucelabs.com
2. Ve a **Automated → Test Results**
3. Filtra por build: `appium-pom-saucelabs`
4. Cada sesión incluye video grabado, logs de Appium y screenshots

---

## Agregar un nuevo escenario

1. Si involucra una pantalla nueva, crea `pages/nueva_pantalla.py` heredando de `BasePage`
2. Agrega la función del escenario en `scenarios.py`
3. Llama el escenario desde `test/test_apidemos.py` (local) y `test/test_apidemos_saucelabs.py` (Sauce Labs)

---

## Buenas prácticas POM

- Los localizadores viven **solo** en el Page Object correspondiente
- Los Page Objects exponen **métodos de acción**, no elementos crudos
- Los métodos de navegación retornan el Page Object de la pantalla destino (encadenamiento)
- Las esperas son **internas** al Page Object — los tests no usan `WebDriverWait` directamente
- Usa `ACCESSIBILITY_ID` cuando sea posible, `ID` como segunda opción
