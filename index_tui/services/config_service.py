import json
from pathlib import Path

from index_tui.domain.models.appconfig import AppConfig


class ConfigService:
    """Serviço para gestão da persistência das configurações do usuário."""

    def __init__(self, config_path: Path | None = None):
        """
        Inicializa o serviço com um caminho específico ou o padrão do sistema.
        Padrão: ~/.config/index/config.json
        """
        self.config_path = config_path or (Path.home() / ".config" / "index" / "config.json")

    def load_config(self) -> AppConfig:
        """
        Carrega a configuração do disco.
        Retorna uma AppConfig vazia se o arquivo não existir ou estiver corrompido.
        """
        if not self.config_path.exists():
            return AppConfig()

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                target = data.get("target_directory")
                return AppConfig(target_directory=Path(target) if target else None)
        except (json.JSONDecodeError, OSError, TypeError):
            # Em caso de erro de leitura ou JSON inválido, retorna padrão seguro
            return AppConfig()

    def save_config(self, config: AppConfig) -> None:
        """
        Salva a configuração no disco, criando os diretórios necessários.
        """
        try:
            # Garante que o diretório pai existe (~/.config/index)
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            data = {
                "target_directory": str(config.target_directory) if config.target_directory else None
            }

            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except OSError:
            # TODO: No futuro, podemos propagar isso para a UI mostrar um alerta
            pass
