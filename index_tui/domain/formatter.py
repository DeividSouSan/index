"""Formatter para reconstruir nomes de arquivo a partir de metadados."""

from index_tui.domain.models.article import Article


def format_filename(article: Article) -> str:
    """
    Reconstrói nome de arquivo a partir dos metadados do Article.

    Formato:
    - [Status] [Origem] [Autor] Título.pdf  (com autor)
    - [Status] [Origem] Título.pdf          (sem autor)

    Args:
        article: Objeto Article com os metadados

    Returns:
        Nome de arquivo formatado
    """
    if not article.is_valid():
        raise ValueError("Artigo inválido para formatação.")

    parts = [f"[{article.status}]", f"[{article.origin}]"]

    if article.author:
        parts.append(f"[{article.author}]")

    parts.append(article.title)

    return " ".join(parts) + ".pdf"
