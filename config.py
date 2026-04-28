import os
from dotenv import load_dotenv
from appium.options.android import UiAutomator2Options

# Carga automáticamente las variables del archivo .env en la raíz del proyecto
load_dotenv()

VALID_MODES = {"local", "saucelabs"}

LOCAL_SERVER_URL = "http://127.0.0.1:4723"
SAUCELABS_SERVER_URL = "https://ondemand.us-west-1.saucelabs.com/wd/hub"


class Config:
    """
    Clase de configuración que construye las opciones del driver de Appium
    y selecciona el entorno de ejecución según la variable APPIUM_ENV.
    Las credenciales se leen del archivo .env en la raíz del proyecto.
    """

    def __init__(self):
        mode = os.environ.get("APPIUM_ENV", "local")

        if mode not in VALID_MODES:
            raise ValueError(
                f"Modo no reconocido: '{mode}'. Usa 'local' o 'saucelabs'."
            )

        self.mode = mode

        if mode == "saucelabs":
            self.options = self._build_saucelabs_options()
            self.server_url = SAUCELABS_SERVER_URL
        else:
            self.options = self._build_local_options()
            self.server_url = LOCAL_SERVER_URL

    def _build_common_options(self) -> UiAutomator2Options:
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.automation_name = "UiAutomator2"
        options.app_package = "io.appium.android.apis"
        options.app_activity = ".ApiDemos"
        options.no_reset = False
        return options

    def _build_local_options(self) -> UiAutomator2Options:
        options = self._build_common_options()
        options.device_name = "Pixel_9"
        options.avd = "Pixel_9"
        options.avd_launch_timeout = 120000
        options.app = "apps/ApiDemos-debug.apk"
        options.load_capabilities({
            "appium:uiautomator2ServerLaunchTimeout": 60000,
            "appium:uiautomator2ServerInstallTimeout": 60000,
        })
        return options

    def _build_saucelabs_options(self) -> UiAutomator2Options:
        username = os.environ.get("SAUCE_USERNAME")
        access_key = os.environ.get("SAUCE_ACCESS_KEY")

        if not username:
            raise ValueError(
                "SAUCE_USERNAME no está definida. "
                "Configura la variable de entorno antes de ejecutar en modo saucelabs."
            )
        if not access_key:
            raise ValueError(
                "SAUCE_ACCESS_KEY no está definida. "
                "Configura la variable de entorno antes de ejecutar en modo saucelabs."
            )

        options = self._build_common_options()
        options.app = "sauce-storage:ApiDemos-debug.apk"
        options.load_capabilities({
            "sauce:options": {
                "username": username,
                "accessKey": access_key,
                "name": "ApiDemos - Appium POM",
                "build": "appium-pom-saucelabs",
            }
        })
        return options
