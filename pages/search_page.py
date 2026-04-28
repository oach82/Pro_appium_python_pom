from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class SearchPage(BasePage):
    """Page Object del submenú Search."""

    _INVOKE_SEARCH = (AppiumBy.ACCESSIBILITY_ID, "Invoke Search")

    def is_displayed(self) -> bool:
        """Verifica que la pantalla Search está visible."""
        return self.is_element_present(self._INVOKE_SEARCH)

    def go_to_invoke_search(self):
        """Navega a Invoke Search y retorna InvokeSearchPage."""
        from pages.invoke_search_page import InvokeSearchPage
        self.wait_and_click(self._INVOKE_SEARCH)
        return InvokeSearchPage(self.driver)
