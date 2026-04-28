import os
import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import Config

# ──────────────────────────────────────────────
# Fixture LOCAL (APPIUM_ENV=local)
# ──────────────────────────────────────────────
@pytest.fixture
def driver():
    """
    Driver para ejecución LOCAL.
    Conecta al servidor Appium en http://127.0.0.1:4723 con emulador Pixel_9.
    Requiere APPIUM_ENV=local en el archivo .env (o por defecto si no está definido).
    """
    os.environ.setdefault("APPIUM_ENV", "local")
    config = Config()
    drv = webdriver.Remote(
        command_executor=config.server_url,
        options=config.options
    )
    yield drv
    drv.quit()


# ──────────────────────────────────────────────
# Fixture SAUCE LABS (APPIUM_ENV=saucelabs)
# ──────────────────────────────────────────────
@pytest.fixture
def driver_saucelabs():
    """
    Driver para ejecución en SAUCE LABS (us-west-1).
    Requiere SAUCE_USERNAME y SAUCE_ACCESS_KEY en el archivo .env.
    """
    os.environ["APPIUM_ENV"] = "saucelabs"
    config = Config()
    drv = webdriver.Remote(
        command_executor=config.server_url,
        options=config.options
    )
    yield drv
    drv.quit()


# ──────────────────────────────────────────────
# Hook de captura de screenshot para Allure
# ──────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Adjunta screenshot al reporte Allure al finalizar cada test.
    - Test PASA  → screenshot como evidencia final.
    - Test FALLA → screenshot del estado de fallo.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        # Busca cualquiera de los dos fixtures de driver
        drv = item.funcargs.get("driver") or item.funcargs.get("driver_saucelabs")
        if drv is not None:
            try:
                screenshot = drv.get_screenshot_as_png()
                nombre = "screenshot_fallo" if report.failed else "screenshot_final"
                allure.attach(
                    screenshot,
                    name=nombre,
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
