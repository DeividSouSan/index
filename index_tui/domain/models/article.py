"""Modelo Article base do dominio"""

from dataclasses import dataclass
from pathlib import Path

from index_tui.domain.value_objects import Status


@dataclass(slots=True)
class Article:
    """Representa um artigo PDF com metadados extraidos do nome."""

    status: Status
    origin: str
    author: str | None
    title: str
    path: Path

    def is_valid(self) -> bool:
        """Verifica se o artigo está em formato válido."""

        IS_STATUS_VALID = isinstance(self.status, Status)
        IS_ORIGIN_EMPTY = bool(self.origin.strip())
        IS_TITLE_EMPTY = bool(self.title.strip())
        IS_EXT_PDF = self.path.suffix.lower() == ".pdf"

        return all([IS_STATUS_VALID, IS_ORIGIN_EMPTY, IS_TITLE_EMPTY, IS_EXT_PDF])

    def __str__(self) -> str:
        """Representação textual do artigo."""
        author_part = f"[{self.author}]" if self.author else ""
        return f"[{self.status}] [{self.origin}] {author_part} {self.title}"
