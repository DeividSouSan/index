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
    if not filename.endswith(".pdf"):
        return None

    # Remove extensão para processar
    name_without_ext = filename[:-4]

    # Padrão: [status] [origem] [autor?] titulo
    # Exemplo válidos:
    # [OK] [Arxiv] John Doe Machine Learning Basics.pdf
    # [NOK] [ResearchGate] Deep Learning.pdf
    pattern = r"^\[([^\]]+)\]\s+\[([^\]]+)\]\s+(.+)$"
    match = re.match(pattern, name_without_ext)

    if not match:
        return None

    status, origin, remainder = match.groups()

    # Validar e criar Status value object
    try:
        status_obj = Status(status)
    except ValueError:
        return None

    # Validar origem não está vazia
    origin = origin.strip()
    if not origin:
        return None

    # Tentar separar autor do título
    # Heurística: verificar se há um padrão de "Palavra Palavra Restante"
    # onde a primeira "Palavra" é um nome próprio (começa com maiúscula e é curto)
    # Se tiver 3+ palavras E a primeira for uma palavra "razoável" (1-20 caracteres),
    # assumir que é autor. Caso contrário, tudo é título.
    words = remainder.split()

    author = None
    title = remainder.strip()

    if len(words) >= 3:
        first_word = words[0]
        # Consideramos um autor válido se: tem 1-20 chars, começa com maiúscula
        if 1 <= len(first_word) <= 20 and first_word[0].isupper():
            author = first_word
            title = " ".join(words[1:])
    elif len(words) == 2:
        # Se houver exatamente 2 palavras, é só título
        title = remainder.strip()
    else:
        # Uma palavra é só título
        title = remainder.strip()

    if not title.strip():
        return None

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
