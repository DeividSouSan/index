from pathlib import Path
from typing import List

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, DataTable, TabbedContent, TabPane, Static

from index_tui.domain.models.article import Article
from index_tui.services.file_service import FileService
from index_tui.services.config_service import ConfigService


class IndexApp(App):
    """Aplicação principal do Index."""

    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("r", "refresh", "Atualizar (Refresh)"),
    ]

    def __init__(
        self, 
        file_service: FileService | None = None, 
        config_service: ConfigService | None = None
    ):
        super().__init__()
        self.file_service = file_service or FileService()
        self.config_service = config_service or ConfigService()
        self.articles: List[Article] = []

    def compose(self) -> ComposeResult:
        """Cria o layout da aplicação."""
        yield Header(show_clock=True)
        
        with Container(id="main-container"):
            yield Static("Nenhum artigo .pdf encontrado no diretório selecionado.", id="empty-state")
            with TabbedContent():
                with TabPane("Principal", id="tab-main"):
                    yield DataTable(id="table-main")
                with TabPane("Uncategorized", id="tab-uncategorized"):
                    yield DataTable(id="table-uncategorized")
        
        yield Footer()

    async def on_mount(self) -> None:
        """Configurações iniciais ao montar o app."""
        # Configurar colunas das tabelas
        for table_id in ["table-main", "table-uncategorized"]:
            table = self.query_one(f"#{table_id}", DataTable)
            table.add_columns("S", "Origem", "Autor", "Título")
            table.cursor_type = "row"
            table.zebra_striping = True
        
        # Carregar dados iniciais
        await self.load_data()

    async def load_data(self) -> None:
        """Carrega a configuração e os artigos do disco."""
        config = self.config_service.load_config()
        
        if not config.is_valid():
            self.notify(
                "Diretório não configurado! Use a M4 para configurar ou aguarde a interface de setup.", 
                severity="warning",
                title="Configuração Ausente"
            )
            return

        # Busca artigos no diretório configurado
        self.articles = self.file_service.list_articles(config.target_directory)
        self.update_tables()

    def update_tables(self) -> None:
        """Atualiza o conteúdo das DataTables com os artigos carregados."""
        main_table = self.query_one("#table-main", DataTable)
        uncategorized_table = self.query_one("#table-uncategorized", DataTable)
        empty_state = self.query_one("#empty-state", Static)
        
        main_table.clear()
        uncategorized_table.clear()
        
        if not self.articles:
            empty_state.display = True
            main_table.display = False
            uncategorized_table.display = False
            return
        
        empty_state.display = False
        main_table.display = True
        uncategorized_table.display = True
        
        for article in self.articles:
            # Estilização básica usando marcação Rich
            status_color = "green" if article.status.is_ok() else "red"
            row = (
                f"[{status_color}]{article.status}[/]",
                article.origin,
                article.author or "-",
                article.title
            )
            
            # Critério de separação: arquivos NOK ou marcados como Uncategorized vão para a segunda aba
            if not article.is_valid() or article.origin == "Uncategorized":
                uncategorized_table.add_row(*row, key=str(article.path))
            else:
                main_table.add_row(*row, key=str(article.path))

    def action_refresh(self) -> None:
        """Ação para atualizar a listagem (R)."""
        self.run_worker(self.load_data(), thread=True)
        self.notify("Biblioteca atualizada!", title="Refresh")
