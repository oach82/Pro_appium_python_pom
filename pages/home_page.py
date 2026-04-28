from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object de la pantalla principal de ApiDemos."""

    _ACCESSIBILITY = (AppiumBy.ACCESSIBILITY_ID, "Accessibility")
    _APP = (AppiumBy.ACCESSIBILITY_ID, "App")

    def is_displayed(self) -> bool:
        """Verifica que la pantalla Home está visible."""
        return self.is_element_present(self._ACCESSIBILITY)

    def go_to_app(self):
        """Navega al submenú App y retorna AppPage."""
        from pages.app_page import AppPage
        self.wait_and_click(self._APP)
        return AppPage(self.driver)
