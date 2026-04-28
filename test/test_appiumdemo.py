"""
Tests de UI para ApiDemos — entorno LOCAL.
Requiere: servidor Appium corriendo en http://127.0.0.1:4723 y emulador Pixel_9 activo.

Ejecutar:
    pytest test/test_apidemos.py -v --alluredir=allure-results
"""
import allure
import pytest
from scenarios import scenario_invoke_search_and_back_home, scenario_select_checks_and_back

pytestmark = pytest.mark.local


@allure.feature("ApiDemos - Búsqueda")
@allure.story("Invoke Search y volver al Home")
@allure.tag("local")
def test_invoke_search_and_back_home(driver):
    scenario_invoke_search_and_back_home(driver)


@allure.feature("ApiDemos - Fragment")
@allure.story("Seleccionar checkboxes en Nesting Tabs y volver a Fragment")
@allure.tag("local")
def test_select_checks_and_back(driver):
    scenario_select_checks_and_back(driver)
