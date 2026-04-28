"""
Tests de UI para ApiDemos — entorno SAUCE LABS.
Requiere variables de entorno: SAUCE_USERNAME y SAUCE_ACCESS_KEY.

Ejecutar:
    set SAUCE_USERNAME=tu_usuario
    set SAUCE_ACCESS_KEY=tu_clave
    pytest test/test_apidemos_saucelabs.py -v --alluredir=allure-results
"""
import allure
import pytest
from scenarios import scenario_invoke_search_and_back_home, scenario_select_checks_and_back

pytestmark = pytest.mark.saucelabs


@allure.feature("AppiumDemos - Búsqueda")
@allure.story("Invoke Search y volver al Home")
@allure.tag("saucelabs")
def test_invoke_search_and_back_home_sl(driver_saucelabs):
    scenario_invoke_search_and_back_home(driver_saucelabs)


@allure.feature("AppiumDemos - Fragment")
@allure.story("Seleccionar checkboxes en Nesting Tabs y volver a Fragment")
@allure.tag("saucelabs")
def test_select_checks_and_back_sl(driver_saucelabs):
    scenario_select_checks_and_back(driver_saucelabs)
