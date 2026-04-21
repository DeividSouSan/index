"""Testes basicos de bootstrap da M1."""

from index_tui.services.health import app_bootstrap_message


def test_bootstrap_message() -> None:
    assert "Index" in app_bootstrap_message()
