from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class FragmentPage(BasePage):
    """Page Object del submenú Fragment."""

    _NESTING_TABS = (AppiumBy.ACCESSIBILITY_ID, "Nesting Tabs")

    def is_displayed(self) -> bool:
        """Verifica que la pantalla Fragment está visible."""
        return self.is_element_present(self._NESTING_TABS)

    def go_to_nesting_tabs(self):
        """Navega a Nesting Tabs y retorna NestingTabsPage."""
        from pages.nesting_tabs_page import NestingTabsPage
        self.wait_and_click(self._NESTING_TABS)
        return NestingTabsPage(self.driver)
