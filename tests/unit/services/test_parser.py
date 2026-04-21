"""Testes do parser de nomes de arquivo."""

from pathlib import Path

from index_tui.services.parser import parse_filename
from index_tui.services.formatter import format_filename


class TestParserValid:
    """Testes de parsing com arquivos válidos."""

    def test_parse_with_author(self):
        """Deve fazer parsing de arquivo com autor (3+ palavras, primeira começa maiúscula)."""
        filename = "[OK] [Arxiv] John Smith Machine Learning.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert str(article.status) == "OK"
        assert article.origin == "Arxiv"
        assert article.author == "John"
        assert article.title == "Smith Machine Learning"

    def test_parse_without_author(self):
        """Deve fazer parsing de arquivo sem autor."""
        filename = "[OK] [ResearchGate] Deep Learning.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert str(article.status) == "OK"
        assert article.origin == "ResearchGate"
        assert article.author is None
        assert article.title == "Deep Learning"

    def test_parse_nok_status(self):
        """Deve aceitar status NOK."""
        filename = "[NOK] [Local] Some Paper.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert str(article.status) == "NOK"

    def test_parse_with_accents(self):
        """Deve lidar corretamente com acentos."""
        filename = "[OK] [Arxiv] João Silva Análise Estatística.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert article.author == "João"
        assert "Análise" in article.title

    def test_parse_with_multiple_spaces(self):
        """Deve detectar autor em titulo de 3+ palavras que começa com maiúscula."""
        filename = "[OK] [Arxiv] Title With Spaces.pdf"
        article = parse_filename(filename)

        assert article is not None
        # "Title" começa com maiúscula e tem 5 caracteres, é considerado autor válido
        assert article.author == "Title"
        assert article.title == "With Spaces"

    def test_parse_with_file_path(self):
        """Deve aceitar caminho completo do arquivo."""
        path = Path("/home/user/papers/test.pdf")
        article = parse_filename("[OK] [Arxiv] Paper.pdf", file_path=path)

        assert article is not None
        assert article.path == path

    def test_parse_numeric_title_no_author(self):
        """Deve considerar números como título (não autor válido)."""
        filename = "[OK] [IEEE] 2024 Conference Proceedings.pdf"
        article = parse_filename(filename)

        assert article is not None
        # "2024" começa com número, não é autor válido
        assert article.author is None
        assert "2024" in article.title

    def test_parse_lowercase_first_word_no_author(self):
        """Primeira palavra em minúsculo não é considerada autor."""
        filename = "[OK] [Arxiv] the quick fox jumps.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert article.author is None
        assert article.title == "the quick fox jumps"


class TestParserInvalid:
    """Testes de parsing com arquivos inválidos."""

    def test_parse_wrong_extension(self):
        """Deve rejeitar extensão não .pdf."""
        filename = "[OK] [Arxiv] Paper.txt"
        article = parse_filename(filename)

        assert article is None

    def test_parse_invalid_status(self):
        """Deve rejeitar status fora do conjunto válido."""
        filename = "[PENDING] [Arxiv] Paper.pdf"
        article = parse_filename(filename)

        assert article is None

    def test_parse_missing_brackets(self):
        """Deve rejeitar formato sem colchetes."""
        filename = "OK Arxiv Paper.pdf"
        article = parse_filename(filename)

        assert article is None

    def test_parse_empty_status(self):
        """Deve rejeitar status vazio."""
        filename = "[] [Arxiv] Paper.pdf"
        article = parse_filename(filename)

        assert article is None

    def test_parse_empty_origin(self):
        """Deve rejeitar origem vazia."""
        filename = "[OK] [] Paper.pdf"
        article = parse_filename(filename)

        assert article is None

    def test_parse_empty_title(self):
        """Deve rejeitar título vazio."""
        filename = "[OK] [Arxiv] "
        article = parse_filename(filename)

        assert article is None

    def test_parse_malformed_brackets(self):
        """Deve rejeitar brackets mal formados."""
        filename = "[OK [Arxiv] Paper.pdf"
        article = parse_filename(filename)

        assert article is None

    def test_parse_case_sensitive_status(self):
        """Deve ser case-sensitive para status."""
        # Status deve ser "OK" ou "NOK", não "ok" ou "Ok"
        filename = "[ok] [Arxiv] Paper.pdf"
        article = parse_filename(filename)

        assert article is None


class TestParserRoundtrip:
    """Testes de roundtrip: parse -> format -> parse."""

    def test_roundtrip_with_author(self):
        """Deve ser idempotente para arquivo com autor."""
        original = "[OK] [Arxiv] John Deep Learning.pdf"
        article1 = parse_filename(original)

        assert article1 is not None

        formatted = format_filename(article1)
        article2 = parse_filename(formatted)

        assert article2 is not None
        assert article1.status == article2.status
        assert article1.origin == article2.origin
        assert article1.title == article2.title

    def test_roundtrip_without_author(self):
        """Deve ser idempotente para arquivo sem autor."""
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


class TestParserEdgeCases:
    """Testes de casos extremos."""

    def test_parse_very_long_title(self):
        """Deve lidar com título muito longo."""
        long_title = "A" * 500
        filename = f"[OK] [Arxiv] {long_title}.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert article.title == long_title

    def test_parse_special_characters_in_title(self):
        """Deve lidar com caracteres especiais no título."""
        filename = "[OK] [Arxiv] Paper A Guide to Advanced Deep Learning.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert "Advanced" in article.title
        assert ":" not in article.title  # : não está no título neste caso

    def test_parse_one_word_title(self):
        """Deve aceitar título de uma palavra."""
        filename = "[OK] [Arxiv] Relativity.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert article.title == "Relativity"

    def test_parse_single_word_author_only(self):
        """Deve fazer parsing quando há apenas 2 palavras (status, origem, título)."""
        filename = "[OK] [Arxiv] Title.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert article.author is None
        assert article.title == "Title"

    def test_parse_author_uppercase_followed_by_lowercase(self):
        """Deve detectar autor quando primeira palavra é capitalized e tem 3+ palavras."""
        filename = "[OK] [Arxiv] Smith et al experimental data.pdf"
        article = parse_filename(filename)

        assert article is not None
        assert article.author == "Smith"
        assert "et al experimental data" == article.title
