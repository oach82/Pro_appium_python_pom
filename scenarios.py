"""
Escenarios de prueba compartidos entre entornos local y Sauce Labs.
Cada función recibe un driver ya inicializado y ejecuta el flujo completo.
"""
import allure
from pages.home_page import HomePage


def scenario_invoke_search_and_back_home(driver):
    """Navega App → Search → Invoke Search, introduce texto y verifica Home."""
    home = HomePage(driver)

    with allure.step("Navegar a App > Search > Invoke Search"):
        invoke_search = (
            home
            .go_to_app()
            .go_to_search()
            .go_to_invoke_search()
        )

    with allure.step("Introducir texto en el campo de búsqueda"):
        invoke_search.enter_query("hola")

    with allure.step("Volver 3 niveles hasta Home"):
        driver.back()
        driver.back()
        driver.back()

    with allure.step("Verificar que la pantalla Home está visible"):
        assert home.is_displayed(), "La pantalla Home no está visible tras volver"


def scenario_select_checks_and_back(driver):
    """Navega App → Fragment → Nesting Tabs, selecciona checkboxes y verifica Fragment."""
    home = HomePage(driver)

    with allure.step("Navegar a App > Fragment"):
        fragment_page = (
            home
            .go_to_app()
            .go_to_fragment()
        )

    with allure.step("Navegar a Nesting Tabs y seleccionar ambos checkboxes"):
        nesting = fragment_page.go_to_nesting_tabs()
        nesting.select_check1_if_unchecked().select_check2_if_unchecked()

    with allure.step("Volver a Fragment"):
        returned_fragment = nesting.go_back()

    with allure.step("Verificar que la pantalla Fragment está visible"):
        assert returned_fragment.is_displayed(), "La pantalla Fragment no está visible tras volver"
