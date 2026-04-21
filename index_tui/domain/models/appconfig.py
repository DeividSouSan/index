from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class AppConfig:
    """Representa a configuracao global da aplicacao."""

    target_directory: Path | None = None

    def is_valid(self) -> bool:
        """Verifica se a configuração é válida."""
        if self.target_directory is None:
            return False

        return self.target_directory.is_dir()
