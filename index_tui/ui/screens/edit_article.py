from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Input, RadioSet, RadioButton

from index_tui.domain.models.article import Article
from index_tui.domain.value_objects import Status


class EditArticleModal(ModalScreen[dict]):
    """Modal para editar metadados de um artigo."""

    def __init__(self, article: Article):
        super().__init__()
        self.article = article

    def compose(self) -> ComposeResult:
        with Grid(id="edit-article-grid"):
            yield Label("Editar Metadados", id="edit-title")
            
            yield Label("Status:", classes="field-label")
            with RadioSet(id="status-radio"):
                yield RadioButton("OK", value=self.article.status.is_ok(), id="status-ok-btn")
                yield RadioButton("NOK", value=self.article.status.is_nok(), id="status-nok-btn")
            
            yield Label("Origem:", classes="field-label")
            yield Input(
                value=self.article.origin, 
                placeholder="Ex: IEEE, Arxiv...", 
                id="origin-input"
            )
            
            yield Label("Autor (opcional):", classes="field-label")
            yield Input(
                value=self.article.author or "", 
                placeholder="Nome do autor...", 
                id="author-input"
            )
            
            yield Label("Título:", classes="field-label")
            yield Input(
                value=self.article.title, 
                placeholder="Título do artigo...", 
                id="title-input"
            )
            
            yield Button("Cancelar", variant="primary", id="cancel")
            yield Button("Salvar", variant="success", id="save")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            status_val = "OK" if self.query_one("#status-ok-btn", RadioButton).value else "NOK"
            self.dismiss({
                "status": Status(status_val),
                "origin": self.query_one("#origin-input", Input).value.strip(),
                "author": self.query_one("#author-input", Input).value.strip() or None,
                "title": self.query_one("#title-input", Input).value.strip()
            })
        else:
            self.dismiss(None)
