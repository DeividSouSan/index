"""Testes unitários para models appconfig.py"""

from pathlib import Path
from index_tui.domain.models.appconfig import AppConfig


class TestAppConfig:
    """Testes para a classe AppConfig"""

    def test_app_config_creation(self, tmp_path):
        _ = AppConfig(target_directory=tmp_path)

    def test_is_valid_with_none_directory(self):
        """Deve retornar False com target_directory None"""

        config = AppConfig(target_directory=None)
        assert not config.is_valid()

    def test_is_valid_with_nonexistent_directory(self):
        """Deve retornar False com diretório inexistente"""

        config = AppConfig(target_directory=Path("/nonexistent/path"))
        assert not config.is_valid()

    def test_is_valid_with_file_path(self, tmp_path):
        """Deve retornar False quando target_directory é um arquivo"""

        file_path = tmp_path / "file.txt"
        file_path.write_text("test")

        config = AppConfig(target_directory=file_path)
        assert not config.is_valid()
