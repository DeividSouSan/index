import subprocess
from pathlib import Path
from typing import List

from send2trash import send2trash

from index_tui.domain.models.article import Article
from index_tui.domain.value_objects import Status
from index_tui.services.formatter import format_filename
from index_tui.services.parser import parse_filename


class FileService:
    """Serviço responsável pelas operações de sistema de arquivos."""

    def list_articles(self, directory: Path) -> List[Article]:
        """
        Escaneia um diretório e retorna uma lista de Artigos encontrados.
        Apenas arquivos .pdf são considerados.
        """
        articles: List[Article] = []

        if not directory.exists() or not directory.is_dir():
            return articles

        for path in directory.iterdir():
            if not path.is_file() or path.suffix.lower() != ".pdf":
                continue

            article = parse_filename(path.name, file_path=path)

            if article is None:
                # Lógica para arquivos Uncategorized
                article = Article(
                    status=Status("NOK"),
                    origin="Uncategorized",
                    author=None,
                    title=path.stem,
                    path=path,
                )

            articles.append(article)

        # Ordenação básica por título para consistência na UI
        articles.sort(key=lambda x: x.title.lower())
        return articles

    def rename_article(self, article: Article) -> Path:
        """
        Renomeia fisicamente o arquivo no disco com base nos metadados do Article.
        Atualiza o atributo article.path em caso de sucesso.

        Raises:
            FileNotFoundError: Se o arquivo original não existir.
            FileExistsError: Se o arquivo de destino já existir.
            PermissionError: Se não houver permissão para renomear.
        """
        if not article.path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {article.path}")

        new_name = format_filename(article)
        new_path = article.path.parent / new_name

        # Se o nome não mudou, não faz nada
        if new_path == article.path:
            return new_path

        if new_path.exists():
            raise FileExistsError(f"O arquivo de destino já existe: {new_path}")

        article.path.rename(new_path)
        article.path = new_path
        return new_path

    def trash_article(self, path: Path) -> None:
        """
        Move o arquivo para a lixeira do sistema de forma segura.

        Raises:
            FileNotFoundError: Se o arquivo não existir.
            OSError: Se houver falha ao mover para a lixeira.
        """
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        send2trash(path)

    def open_article(self, path: Path) -> None:
        """
        Abre o arquivo usando o visualizador padrão do sistema (xdg-open).

        Raises:
            FileNotFoundError: Se o arquivo não existir.
            OSError: Se houver falha ao executar o comando de abertura.
        """
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        # xdg-open é o padrão para Linux.
        # Em uma versão futura, poderíamos detectar o SO para usar 'open' ou 'start'.
        subprocess.run(["xdg-open", str(path)], check=True)
