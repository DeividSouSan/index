from pathlib import Path
from typing import List

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, DataTable, TabbedContent, TabPane, Static
from textual.screen import ModalScreen

from index_tui.domain.models.article import Article
from index_tui.services.file_service import FileService
from index_tui.services.config_service import ConfigService
from index_tui.ui.screens.confirmation import ConfirmationModal
from index_tui.ui.screens.settings import SettingsModal
from index_tui.ui.screens.edit_article import EditArticleModal


class IndexApp(App):
    """Aplicação principal do Index."""

    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("q", "quit", "Sair"),
        ("r", "refresh", "Atualizar"),
        ("s", "settings", "Configurar"),
        ("e", "edit_article", "Editar"),
        ("delete", "delete_article", "Excluir"),
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

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Chamado quando o usuário pressiona Enter em uma linha da tabela."""
        path_str = event.row_key.value
        if path_str:
            self.action_open_file(Path(path_str))

    def action_open_file(self, path: Path) -> None:
        """Abre o arquivo PDF selecionado."""
        try:
            self.file_service.open_article(path)
            self.notify(f"Abrindo: {path.name}", title="Sucesso")
        except Exception as e:
            self.notify(
                f"Não foi possível abrir o arquivo: {e}", 
                severity="error", 
                title="Erro de IO"
            )

    def action_delete_article(self) -> None:
        """Ação disparada ao pressionar Delete para excluir um artigo."""
        # Tenta pegar a tabela que está com o foco atual
        table = self.query("DataTable:focus").first()
        if not table or table.cursor_row < 0:
            return

        # Forma correta de pegar a chave da linha no Textual 0.x
        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        path = Path(row_key.value)

        def check_confirmation(confirmed: bool) -> None:
            if confirmed:
                try:
                    self.file_service.trash_article(path)
                    self.notify(f"Enviado para a lixeira: {path.name}")
                    self.action_refresh()
                except Exception as e:
                    self.notify(f"Erro ao excluir: {e}", severity="error", title="Erro")

        self.push_screen(
            ConfirmationModal(f"Deseja enviar este arquivo para a lixeira?\n\n{path.name}"),
            check_confirmation
        )

    def action_settings(self) -> None:
        """Ação disparada ao pressionar 'S' para configurar o diretório."""
        config = self.config_service.load_config()
        current_dir = str(config.target_directory or "")

        def update_settings(new_dir: str | None) -> None:
            if new_dir:
                path = Path(new_dir)
                if path.is_dir():
                    from index_tui.domain.models.appconfig import AppConfig
                    new_config = AppConfig(target_directory=path)
                    self.config_service.save_config(new_config)
                    self.notify(f"Diretório atualizado: {path.name}", title="Sucesso")
                    self.action_refresh()
                else:
                    self.notify(
                        "O caminho informado não é um diretório válido.", 
                        severity="error", 
                        title="Erro"
                    )

        self.push_screen(SettingsModal(current_dir), update_settings)

    def action_edit_article(self) -> None:
        """Ação disparada ao pressionar 'E' para editar um artigo."""
        table = self.query("DataTable:focus").first()
        if not table or table.cursor_row < 0:
            return

        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        path = Path(row_key.value)
        
        # Encontrar o artigo correspondente na lista atual
        article = next((a for a in self.articles if a.path == path), None)
        if not article:
            return

        def update_metadata(data: dict | None) -> None:
            if data:
                try:
                    # Atualiza o objeto em memória para gerar o novo nome
                    article.status = data["status"]
                    article.origin = data["origin"]
                    article.author = data["author"]
                    article.title = data["title"]
                    
                    self.file_service.rename_article(article)
                    self.notify("Artigo atualizado com sucesso!", title="Edição")
                    self.action_refresh()
                except Exception as e:
                    self.notify(f"Erro ao salvar: {e}", severity="error", title="Erro")

        self.push_screen(EditArticleModal(article), update_metadata)
