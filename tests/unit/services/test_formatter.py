"""Testes do formatter de nomes de arquivo."""

from pathlib import Path
import pytest
from index_tui.domain.models.article import Article
from index_tui.domain.value_objects import Status
from index_tui.services.formatter import format_filename
from index_tui.services.parser import parse_filename


class TestFormatterMethod:
    """Testes básicos de formatação."""

    def test_format_with_author(self):
        """Deve formatar corretamente artigo com autor."""
        article = Article(
            status=Status("OK"),
            origin="Arxiv",
            author="John",
            title="Deep Learning",
            path=Path("test.pdf"),
        )

        result = format_filename(article)

        assert result == "[OK] [Arxiv] [John] Deep Learning.pdf"

    def test_format_without_author(self):
        """Deve formatar corretamente artigo sem autor."""
        article = Article(
            status=Status("NOK"),
            origin="ResearchGate",
            author=None,
            title="Machine Learning",
            path=Path("test.pdf"),
        )

        result = format_filename(article)

        assert result == "[NOK] [ResearchGate] Machine Learning.pdf"

    def test_format_nok_status(self):
        """Deve respeitar status NOK."""
        article = Article(
            status=Status("NOK"),
            origin="Local",
            author=None,
            title="Paper",
            path=Path("test.pdf"),
        )

        result = format_filename(article)

        assert result.startswith("[NOK]")

    def test_format_with_accents(self):
        """Deve preservar acentos."""
        article = Article(
            status=Status("OK"),
            origin="Arxiv",
            author="João",
            title="Análise de Dados",
            path=Path("test.pdf"),
        )

        result = format_filename(article)

        assert "João" in result
        assert "Análise" in result


class TestFormatterCompatibilityWithParser:
    """Testes de compatibilidade com parser."""

    def test_formatted_is_parseable(self):
        """Formato gerado deve ser parseável."""
        article = Article(
            status=Status("OK"),
            origin="IEEE",
            author="Smith",
            title="Computer Vision",
            path=Path("test.pdf"),
        )

        formatted = format_filename(article)

        parsed = parse_filename(formatted)

        assert parsed is not None
        assert str(parsed.status) == str(article.status)
        assert parsed.origin == article.origin
        assert parsed.title == article.title

    def test_format_then_parse_preserves_metadata(self):
        """Dados devem ser preservados após format → parse."""
        article = Article(
            status=Status("OK"),
            origin="Arxiv",
            author="Alice",
            title="Quantum Computing Basics",
            path=Path("test.pdf"),
        )

        formatted = format_filename(article)
        reparsed = parse_filename(formatted)

        assert reparsed is not None
        assert str(reparsed.status) == "OK"
        assert reparsed.origin == "Arxiv"
        assert reparsed.title == "Quantum Computing Basics"

    def test_format_no_author_then_parse(self):
        """Formato sem autor deve permanecer sem autor após roundtrip."""
        article = Article(
            status=Status("OK"),
            origin="Local",
            author=None,
            title="My Paper",
            path=Path("test.pdf"),
        )

        formatted = format_filename(article)
        reparsed = parse_filename(formatted)

        assert reparsed is not None
        assert reparsed.author is None
        assert reparsed.title == "My Paper"


class TestFormatterEdgeCases:
    """Testes de casos extremos."""

    def test_format_long_title(self):
        """Deve formatar título muito longo."""
        long_title = "A" * 500
        article = Article(
            status=Status("OK"),
            origin="Arxiv",
            author=None,
            title=long_title,
            path=Path("test.pdf"),
        )

        result = format_filename(article)

        assert long_title in result
        assert result.endswith(".pdf")

    def test_format_special_characters(self):
        """Deve preservar caracteres especiais no título."""
        article = Article(
            status=Status("OK"),
            origin="Arxiv",
            author=None,
            title="Paper: The (Quick) & Dirty Guide",
            path=Path("test.pdf"),
        )

        result = format_filename(article)

        assert ":" in result
        assert "(" in result
        assert "&" in result

    def test_format_always_ends_with_pdf(self):
        """Resultado deve sempre terminar com .pdf."""
        article = Article(
            status=Status("OK"),
            origin="Source",
            author="Author",
            title="Title",
            path=Path("test.pdf"),
        )

        result = format_filename(article)

        assert result.endswith(".pdf")

    def test_format_author_empty_string(self):
        """Deve tratar string vazia de autor como None."""
        article = Article(
            status=Status("OK"),
            origin="Source",
            author="",  # String vazia, não None
            title="Title",
            path=Path("test.pdf"),
        )

        result = format_filename(article)

        # Comportamento: se author é string vazia (falsy), não deve incluir
        assert "[OK] [Source] Title.pdf" == result or "[OK] [Source]  Title.pdf" in result
