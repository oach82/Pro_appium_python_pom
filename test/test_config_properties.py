"""
Pruebas basadas en propiedades para la clase Config.
Validan la lógica pura de configuración sin necesidad de un servidor Appium real.

Nota: hypothesis @given no es compatible con fixtures de pytest como monkeypatch.
Se usa unittest.mock.patch para aislar variables de entorno dentro de cada prueba.
"""
import os
import pytest
from unittest.mock import patch
from hypothesis import given, settings
from hypothesis import strategies as st

from config import Config


def _env_for_mode(mode: str, has_username: bool = True, has_key: bool = True) -> dict:
    """Construye el diccionario de variables de entorno para un modo dado."""
    env = {"APPIUM_ENV": mode}
    if mode == "saucelabs":
        if has_username:
            env["SAUCE_USERNAME"] = "test_user"
        if has_key:
            env["SAUCE_ACCESS_KEY"] = "test_key"
    return env


# ──────────────────────────────────────────────
# Propiedad 1: Capabilities comunes en cualquier modo válido
# Feature: appium-pom-saucelabs, Property 1: capabilities comunes presentes en cualquier modo válido
# Valida: Requisito 2.8
# ──────────────────────────────────────────────
@given(st.sampled_from(["local", "saucelabs"]))
@settings(max_examples=100)
def test_common_capabilities_present(mode):
    """Para cualquier modo válido, las capabilities comunes deben estar presentes."""
    env = _env_for_mode(mode)
    with patch.dict(os.environ, env, clear=False):
        # Limpiar credenciales si no aplican
        for key in ["SAUCE_USERNAME", "SAUCE_ACCESS_KEY"]:
            if key not in env:
                os.environ.pop(key, None)
        config = Config()

    opts = config.options
    assert opts.platform_name == "Android"
    assert opts.automation_name.lower() == "uiautomator2"
    assert opts.app_package == "io.appium.android.apis"
    assert opts.app_activity == ".ApiDemos"
    assert opts.no_reset is False


# ──────────────────────────────────────────────
# Propiedad 2: Modo correcto según APPIUM_ENV
# Feature: appium-pom-saucelabs, Property 2: modo correcto según APPIUM_ENV
# Valida: Requisito 2.1
# ──────────────────────────────────────────────
@given(st.sampled_from(["local", "saucelabs"]))
@settings(max_examples=100)
def test_mode_matches_env(mode):
    """Config().mode debe coincidir con el valor de APPIUM_ENV."""
    env = _env_for_mode(mode)
    with patch.dict(os.environ, env, clear=False):
        for key in ["SAUCE_USERNAME", "SAUCE_ACCESS_KEY"]:
            if key not in env:
                os.environ.pop(key, None)
        config = Config()

    assert config.mode == mode


# ──────────────────────────────────────────────
# Propiedad 3: ValueError ante credenciales faltantes en modo SauceLabs
# Feature: appium-pom-saucelabs, Property 3: ValueError ante credenciales faltantes en modo SauceLabs
# Valida: Requisito 2.5
# ──────────────────────────────────────────────
@given(st.booleans(), st.booleans())
@settings(max_examples=100)
def test_missing_credentials_raises(has_username, has_key):
    """Si falta alguna credencial en modo saucelabs, debe lanzar ValueError."""
    env = {"APPIUM_ENV": "saucelabs"}
    if has_username:
        env["SAUCE_USERNAME"] = "test_user"
    if has_key:
        env["SAUCE_ACCESS_KEY"] = "test_key"

    # Construir entorno limpio: solo las vars que queremos
    base_env = {k: v for k, v in os.environ.items()
                if k not in ("APPIUM_ENV", "SAUCE_USERNAME", "SAUCE_ACCESS_KEY")}
    base_env.update(env)

    with patch.dict(os.environ, base_env, clear=True):
        if has_username and has_key:
            # Ambas presentes → no debe lanzar
            config = Config()
            assert config.mode == "saucelabs"
        else:
            # Al menos una falta → debe lanzar ValueError
            with pytest.raises(ValueError):
                Config()
