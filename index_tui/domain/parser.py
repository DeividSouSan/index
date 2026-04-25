"""Parser para extrair metadados de nomes de arquivo PDF."""

import re
from pathlib import Path

from index_tui.domain.models.article import Article
from index_tui.domain.value_objects import Status


def parse_filename(filename: str, file_path: Path | None = None) -> Article | None:
    """
    Extrai metadados de um nome de arquivo seguindo o padrão:
    - [Status] [Origem] [Autor] Título.pdf
    - [Status] [Origem] Título.pdf

    Args:
        filename: Nome do arquivo a fazer parsing
        file_path: Caminho completo do arquivo (opcional)

    Returns:
        Article se o parsing for bem-sucedido, None caso contrário
    """
    pattern = r"^\[([^\]\s]+)\]\s+\[([^\]\s]+)\](?:\s+\[([^\]\s]+)\])?\s+(.+)\.pdf$"
    match = re.match(pattern, filename, re.IGNORECASE)

    if not match:
        return None

    status, origin, author, title = match.groups()

    try:
        status_obj = Status(status)
    except ValueError:
        return None

    title = title.strip()

    # Construir objeto Article
    path = file_path or Path(filename)
    article = Article(
        status=status_obj,
        origin=origin,
        author=author,
        title=title,
        path=path,
    )

    # Validar contra regras fechadas
    if not article.is_valid():
        return None

    return article
