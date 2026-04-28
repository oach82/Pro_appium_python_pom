from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class AppPage(BasePage):
    """Page Object del submenú App."""

    _SEARCH = (AppiumBy.ACCESSIBILITY_ID, "Search")
    _FRAGMENT = (AppiumBy.ACCESSIBILITY_ID, "Fragment")

    def is_displayed(self) -> bool:
        """Verifica que la pantalla App está visible."""
        return self.is_element_present(self._SEARCH)

    def go_to_search(self):
        """Navega al submenú Search y retorna SearchPage."""
        from pages.search_page import SearchPage
        self.wait_and_click(self._SEARCH)
        return SearchPage(self.driver)

    def go_to_fragment(self):
        """Navega al submenú Fragment y retorna FragmentPage."""
        from pages.fragment_page import FragmentPage
        self.wait_and_click(self._FRAGMENT)
        return FragmentPage(self.driver)
