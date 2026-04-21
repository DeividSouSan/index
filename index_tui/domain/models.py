"""Modelos base do dominio para as proximas milestones."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Article:
    """Representa um artigo PDF com metadados extraidos do nome."""

    status: str
    origin: str
    author: str | None
    title: str
    path: Path


@dataclass(slots=True)
class AppConfig:
    """Representa a configuracao global da aplicacao."""

    target_directory: Path | None = None
