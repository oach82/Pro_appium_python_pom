from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class InvokeSearchPage(BasePage):
    """Page Object de la pantalla Invoke Search."""

    _QUERY_INPUT = (AppiumBy.ID, "io.appium.android.apis:id/txt_query_prefill")

    def is_displayed(self) -> bool:
        """Verifica que el campo de consulta está visible."""
        return self.is_element_present(self._QUERY_INPUT)

    def enter_query(self, text: str) -> "InvokeSearchPage":
        """Limpia el campo e introduce el texto dado."""
        field = self.wait_for_element(self._QUERY_INPUT)
        field.clear()
        field.send_keys(text)
        return self

    def go_back(self):
        """Vuelve a la pantalla Search y retorna SearchPage."""
        from pages.search_page import SearchPage
        self.driver.back()
        return SearchPage(self.driver)
