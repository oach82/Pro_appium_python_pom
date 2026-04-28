from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Clase base para todos los Page Objects. Centraliza la lógica de espera."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10)

    def wait_and_click(self, locator: tuple, timeout: int = 10) -> None:
        """Espera a que el elemento sea clickeable y hace click."""
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()

    def wait_for_element(self, locator: tuple, timeout: int = 10):
        """Espera a que el elemento esté presente y lo retorna."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def is_element_present(self, locator: tuple, timeout: int = 5) -> bool:
        """Retorna True si el elemento aparece antes del timeout."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except Exception:
            return False
