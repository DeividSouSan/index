"""Testes do parser de nomes de arquivo."""

from pathlib import Path

from index_tui.services.formatter import format_filename
from index_tui.services.parser import parse_filename


class TestParserValid:
    """Testes de parsing com arquivos válidos."""

    def test_parse_with_explicit_author_block(self):
        """Deve fazer parsing quando autor está entre colchetes."""
        filename = "[OK] [Arxiv] [John] Deep Learning.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert str(article.status) == "OK"
        assert article.origin == "Arxiv"
        assert article.author == "John"
        assert article.title == "Deep Learning"

    def test_parse_without_author(self):
        """Deve fazer parsing de arquivo sem autor."""
        filename = "[NOK] [ResearchGate] Deep Learning.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert str(article.status) == "NOK"
        assert article.origin == "ResearchGate"
        assert article.author is None
        assert article.title == "Deep Learning"

    def test_parse_with_file_path(self):
        """Deve aceitar caminho completo do arquivo."""
        path = Path("/home/user/papers/test.pdf")
        article = parse_filename("[OK] [Arxiv] Paper.pdf", file_path=path)

        assert article is not None
        assert article.path == path

    def test_parse_title_with_accents_and_symbols(self):
        """Deve aceitar título livre com espaços e pontuação."""
        filename = "[OK] [Anthropic] Claude is dangerous?.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert article.author is None
        assert article.title == "Claude is dangerous?"

    def test_parse_one_word_title(self):
        """Deve aceitar título de uma palavra."""
        filename = "[OK] [Arxiv] Relativity.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert article.title == "Relativity"


class TestParserInvalid:
    """Testes de parsing com arquivos inválidos."""

    def test_parse_wrong_extension(self):
        """Deve rejeitar extensão não .pdf."""
        filename = "[OK] [Arxiv] Paper.txt"
        assert parse_filename(filename) is None

    def test_parse_invalid_status(self):
        """Deve rejeitar status fora do conjunto válido."""
        filename = "[PENDING] [Arxiv] Paper.pdf"
        assert parse_filename(filename) is None

    def test_parse_missing_brackets(self):
        """Deve rejeitar formato sem colchetes."""
        filename = "OK Arxiv Paper.pdf"
        assert parse_filename(filename) is None

    def test_parse_origin_with_spaces(self):
        """Deve rejeitar origem com espaços."""
        filename = "[OK] [Origin Space] Title.pdf"
        assert parse_filename(filename) is None

    def test_parse_author_with_spaces(self):
        """Deve rejeitar autor com espaços."""
        filename = "[OK] [Arxiv] [John Smith] Title.pdf"
        assert parse_filename(filename) is None

    def test_parse_title_empty_without_author(self):
        """Deve rejeitar título vazio sem autor."""
        filename = "[OK] [Arxiv] .pdf"
        assert parse_filename(filename) is None

    def test_parse_title_empty_with_author(self):
        """Deve rejeitar título vazio com autor."""
        filename = "[OK] [Arxiv] [John] .pdf"
        assert parse_filename(filename) is None

    def test_parse_title_with_brackets(self):
        """Deve rejeitar título com colchetes."""
        filename = "[OK] [Arxiv] [John] [Title].pdf"
        assert parse_filename(filename) is None

    def test_parse_unbracketed_name_as_title(self):
        """Sem bloco de autor, o trecho final é sempre título."""
        filename = "[OK] [Arxiv] John Deep Learning.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert article.author is None
        assert article.title == "John Deep Learning"


class TestParserRoundtrip:
    """Testes de roundtrip: parse -> format -> parse."""

    def test_roundtrip_with_author(self):
        """Deve preservar campos no roundtrip com autor."""
        original = "[OK] [Arxiv] [John] Deep Learning.pdf"
        article1 = parse_filename(original)

        assert article1 is not None

        formatted = format_filename(article1)
        article2 = parse_filename(formatted)

        assert article2 is not None
        assert article1.status == article2.status
        assert article1.origin == article2.origin
        assert article1.author == article2.author
        assert article1.title == article2.title

    def test_roundtrip_without_author(self):
        """Deve preservar campos no roundtrip sem autor."""
        original = "[NOK] [ResearchGate] Deep Learning.pdf"
        article1 = parse_filename(original)

        assert article1 is not None

        formatted = format_filename(article1)
        article2 = parse_filename(formatted)

        assert article2 is not None
        assert article1.status == article2.status
        assert article1.origin == article2.origin
        assert article1.author is None
        assert article2.author is None
        assert article1.title == article2.title
