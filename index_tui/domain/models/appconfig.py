from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AppConfig:
    """Representa a configuracao global da aplicacao."""

    target_directory: Path | None = None

    def is_valid(self) -> bool:
        """Verifica se a configuração é válida."""
        return self.target_directory is not None and self.target_directory.is_dir()
