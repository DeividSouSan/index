import json
import pytest
from pathlib import Path
from index_tui.services.config_service import ConfigService
from index_tui.domain.models.appconfig import AppConfig

@pytest.fixture
def config_file(tmp_path):
    return tmp_path / "config.json"

@pytest.fixture
def service(config_file):
    return ConfigService(config_path=config_file)

def test_load_config_returns_empty_config_when_file_not_found(service):
    config = service.load_config()
    assert isinstance(config, AppConfig)
    assert config.target_directory is None

def test_save_config_creates_directories_and_file(service, config_file, tmp_path):
    deep_path = tmp_path / "subdir" / "index" / "config.json"
    service = ConfigService(config_path=deep_path)
    
    target = Path("/tmp/articles")
    config = AppConfig(target_directory=target)
    
    service.save_config(config)
    
    assert deep_path.exists()
    with open(deep_path, "r") as f:
        data = json.load(f)
        assert data["target_directory"] == str(target)

def test_load_config_restores_data_correctly(service, config_file):
    target = Path("/home/user/books")
    data = {"target_directory": str(target)}
    config_file.write_text(json.dumps(data))
    
    config = service.load_config()
    assert config.target_directory == target

def test_load_config_handles_invalid_json_gracefully(service, config_file):
    config_file.write_text("{ invalid json ...")
    
    config = service.load_config()
    assert config.target_directory is None

def test_save_and_load_roundtrip(service):
    target = Path("/path/to/sync")
    original_config = AppConfig(target_directory=target)
    
    service.save_config(original_config)
    loaded_config = service.load_config()
    
    assert loaded_config.target_directory == original_config.target_directory

def test_save_config_handles_permission_error_gracefully(service, monkeypatch):
    from unittest.mock import mock_open
    
    # Simular erro de sistema ao tentar abrir o arquivo para escrita
    def mock_open_error(*args, **kwargs):
        raise PermissionError("Acesso negado")
        
    monkeypatch.setattr("builtins.open", mock_open_error)
    
    config = AppConfig(target_directory=Path("/tmp"))
    # Não deve estourar exceção, apenas capturar conforme o código atual
    service.save_config(config)
