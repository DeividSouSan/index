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

        is_status_valid = isinstance(self.status, Status)
        has_origin = bool(self.origin.strip())
        has_title = bool(self.title.strip())
        is_pdf_extension = self.path.suffix.lower() == ".pdf"

        return all((is_status_valid, has_origin, has_title, is_pdf_extension))

    def __str__(self) -> str:
        """Representação textual do artigo."""
        parts = [f"[{self.status}]", f"[{self.origin}]"]

        if self.author:
            parts.append(f"[{self.author}]")

        parts.append(self.title)

        return " ".join(parts)
