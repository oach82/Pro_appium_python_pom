from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class NestingTabsPage(BasePage):
    """Page Object de la pantalla Nesting Tabs con checkboxes."""

    _CHECK1 = (AppiumBy.ID, "io.appium.android.apis:id/menu1")
    _CHECK2 = (AppiumBy.ID, "io.appium.android.apis:id/menu2")

    def is_displayed(self) -> bool:
        """Verifica que el checkbox 1 está visible."""
        return self.is_element_present(self._CHECK1)

    def select_check1_if_unchecked(self) -> "NestingTabsPage":
        """Selecciona el checkbox 1 si no está marcado."""
        check = self.wait_for_element(self._CHECK1)
        if not check.is_selected():
            check.click()
        return self

    def select_check2_if_unchecked(self) -> "NestingTabsPage":
        """Selecciona el checkbox 2 si no está marcado."""
        check = self.wait_for_element(self._CHECK2)
        if not check.is_selected():
            check.click()
        return self

    def go_back(self):
        """Vuelve un nivel y retorna FragmentPage."""
        from pages.fragment_page import FragmentPage
        self.driver.back()
        return FragmentPage(self.driver)
