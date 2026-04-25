from index_tui.domain.models.article import Article
import pytest
from pathlib import Path
from index_tui.services.file_service import FileService
from index_tui.domain.value_objects import Status

@pytest.fixture
def file_service():
    return FileService()

def test_list_articles_returns_empty_list_for_empty_directory(tmp_path, file_service):
    articles = file_service.list_articles(tmp_path)
    assert articles == []

def test_list_articles_filters_only_pdf_files(tmp_path, file_service):
    (tmp_path / "valid.pdf").touch()
    (tmp_path / "invalid.txt").touch()
    (tmp_path / "image.png").touch()
    
    articles = file_service.list_articles(tmp_path)
    
    assert len(articles) == 1
    assert articles[0].path.name == "valid.pdf"

def test_list_articles_parses_valid_filenames_correctly(tmp_path, file_service):
    # [Status] [Origem] [Autor] Título.pdf
    filename = "[OK] [IEEE] [Jane] My Paper.pdf"
    (tmp_path / filename).touch()
    
    articles = file_service.list_articles(tmp_path)
    
    assert len(articles) == 1
    article = articles[0]
    assert article.status == Status("OK")
    assert article.origin == "IEEE"
    assert article.author == "Jane"
    assert article.title == "My Paper"
    assert article.is_valid() is True

def test_list_articles_handles_uncategorized_pdfs(tmp_path, file_service):
    # Arquivo PDF que não segue o contrato
    filename = "Random Article Without Brackets.pdf"
    (tmp_path / filename).touch()
    
    articles = file_service.list_articles(tmp_path)
    
    assert len(articles) == 1
    article = articles[0]
    assert article.status == Status("NOK")
    assert article.origin == "Uncategorized"
    assert article.title == "Random Article Without Brackets"
    assert article.path.name == filename

def test_list_articles_is_case_insensitive_for_extension(tmp_path, file_service):
    (tmp_path / "upper.PDF").touch()
    articles = file_service.list_articles(tmp_path)
    assert len(articles) == 1

def test_rename_article_success(tmp_path, file_service):
    # Setup
    old_path = tmp_path / "old.pdf"
    old_path.touch()
    
    article = Article(
        status=Status("OK"),
        origin="ACM",
        author="Bob",
        title="New Title",
        path=old_path
    )
    
    new_path = file_service.rename_article(article)
    
    assert not old_path.exists()
    assert new_path.exists()
    assert new_path.name == "[OK] [ACM] [Bob] New Title.pdf"
    assert article.path == new_path

def test_rename_article_raises_error_if_destination_exists(tmp_path, file_service):
    old_path = tmp_path / "old.pdf"
    old_path.touch()
    
    dest_name = "[OK] [ACM] [Bob] Existing.pdf"
    (tmp_path / dest_name).touch()
    
    article = Article(Status("OK"), "ACM", "Bob", "Existing", old_path)
    
    with pytest.raises(FileExistsError):
        file_service.rename_article(article)

def test_trash_article_success(tmp_path, file_service, monkeypatch):
    # Setup
    path = tmp_path / "to_delete.pdf"
    path.touch()
    
    # Mock send2trash
    called_with = None
    def mock_send2trash(p):
        nonlocal called_with
        called_with = p
    
    monkeypatch.setattr("index_tui.services.file_service.send2trash", mock_send2trash)
    
    file_service.trash_article(path)
    assert called_with == path

def test_trash_article_raises_error_if_not_found(tmp_path, file_service):
    path = tmp_path / "non_existent.pdf"
    
    with pytest.raises(FileNotFoundError):
        file_service.trash_article(path)

def test_open_article_success(tmp_path, file_service, monkeypatch):
    # Setup
    path = tmp_path / "study.pdf"
    path.touch()
    
    # Mock subprocess.run
    called_command = None
    def mock_run(args, **kwargs):
        nonlocal called_command
        called_command = args
    
    monkeypatch.setattr("subprocess.run", mock_run)
    
    file_service.open_article(path)
    assert called_command == ["xdg-open", str(path)]

def test_open_article_raises_error_if_not_found(tmp_path, file_service):
    path = tmp_path / "missing.pdf"
    
    with pytest.raises(FileNotFoundError):
        file_service.open_article(path)

def test_list_articles_non_existent_directory(tmp_path, file_service):
    non_existent = tmp_path / "ghost_dir"
    articles = file_service.list_articles(non_existent)
    assert articles == []

def test_rename_article_no_op_if_name_is_same(tmp_path, file_service):
    path = tmp_path / "[OK] [Origin] Title.pdf"
    path.touch()
    article = Article(Status("OK"), "Origin", None, "Title", path)
    
    new_path = file_service.rename_article(article)
    assert new_path == path

def test_rename_article_raises_error_if_source_not_found(tmp_path, file_service):
    path = tmp_path / "gone.pdf"
    article = Article(Status("OK"), "Origin", None, "Title", path)
    
    with pytest.raises(FileNotFoundError):
        file_service.rename_article(article)
