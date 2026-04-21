"""Testes unitários para model article.py"""

import pytest
from index_tui.domain.models.article import Article
from index_tui.domain.value_objects import Status


class TestArticle:
    """Testes para a classe Article"""

    def test_is_valid_with_valid_article(self, tmp_path):
        """Deve retornar True para um artigo válido"""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("test")

        article = Article(
            status=Status("OK"),
            origin="Nature",
            author="Smith",
            title="Test Article",
            path=pdf_path,
        )

        assert article.is_valid()

    def test_is_valid_with_invalid_status(self, tmp_path):
        """Deve rejeitar status inválido na criação"""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("test")

        with pytest.raises(ValueError):
            Article(
                status=Status("INVALID"),
                origin="Nature",
                author="Smith",
                title="Test Article",
                path=pdf_path,
            )

    def test_is_valid_with_invalid_type_status(self, tmp_path):
        """Deve invalidar artigo quando status não é Status."""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("test")

        article = Article(
            status="OK",
            origin="Nature",
            author="Smith",
            title="Test Article",
            path=pdf_path,
        )

        assert not article.is_valid()

    def test_is_valid_with_empty_origin(self, tmp_path):
        """Deve retornar False com origin vazio"""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("test")

        article = Article(
            status=Status("OK"), origin="   ", author="Smith", title="Test Article", path=pdf_path
        )
        assert not article.is_valid()

    def test_is_valid_with_origin_with_spaces(self, tmp_path):
        """Deve retornar False com origin contendo espaços."""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("test")

        article = Article(
            status=Status("OK"),
            origin="My Origin",
            author="Smith",
            title="Test Article",
            path=pdf_path,
        )

        assert not article.is_valid()

    def test_is_valid_with_empty_title(self, tmp_path):
        """Deve retornar False com title vazio"""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("test")

        article = Article(
            status=Status("OK"), origin="Nature", author="Smith", title="   ", path=pdf_path
        )
        assert not article.is_valid()

    def test_is_valid_with_non_pdf_file(self, tmp_path):
        """Deve retornar False para arquivo que não é PDF"""
        txt_path = tmp_path / "test.txt"
        txt_path.write_text("test")

        article = Article(
            status=Status("OK"),
            origin="Nature",
            author="Smith",
            title="Test Article",
            path=txt_path,
        )
        assert not article.is_valid()

    def test_is_valid_with_none_author(self, tmp_path):
        """Deve retornar True mesmo com author None"""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("test")

        article = Article(
            status=Status("OK"), origin="Nature", author=None, title="Test Article", path=pdf_path
        )
        assert article.is_valid()

    def test_is_valid_with_author_with_spaces(self, tmp_path):
        """Deve retornar False com author contendo espaços."""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("test")

        article = Article(
            status=Status("OK"),
            origin="Nature",
            author="John Smith",
            title="Test Article",
            path=pdf_path,
        )

        assert not article.is_valid()

    def test_is_valid_with_nok_status(self, tmp_path):
        """Deve retornar True com status NOK"""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("test")

        article = Article(
            status=Status("NOK"), origin="Nature", author=None, title="Test Article", path=pdf_path
        )
        assert article.is_valid()

    def test_is_valid_with_title_with_brackets(self, tmp_path):
        """Deve retornar False quando título contém colchetes."""
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("test")

        article = Article(
            status=Status("OK"),
            origin="Nature",
            author=None,
            title="[Invalid] Title",
            path=pdf_path,
        )

        assert not article.is_valid()

    def test_str_with_valid_author(self, tmp_path):
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("test")

        article = Article(
            status=Status("OK"),
            origin="Nature",
            author="Smith",
            title="Test Article",
            path=pdf_path,
        )

        assert str(article) == "[OK] [Nature] [Smith] Test Article"

    def test_str_with_none_author(self, tmp_path):
        pdf_path = tmp_path / "test.pdf"
        pdf_path.write_text("test")

        article = Article(
            status=Status("OK"),
            origin="Nature",
            author=None,
            title="Test Article",
            path=pdf_path,
        )

        assert str(article) == "[OK] [Nature] Test Article"
