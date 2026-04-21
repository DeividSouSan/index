"""Aplicacao TUI principal da M1."""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header, Static

from index_tui.services.health import app_bootstrap_message


class IndexApp(App[None]):
    """Aplicacao principal do Index para fase de fundacao."""

    TITLE = "Index"
    SUB_TITLE = "Milestone 1 - Fundacao"
    BINDINGS = [("q", "quit", "Sair")]

    CSS = """
    Screen {
        align: center middle;
    }

    #welcome {
        content-align: center middle;
        width: 70%;
        min-width: 52;
        padding: 1 2;
        border: round $accent;
    }
    """

    def compose(self) -> ComposeResult:
        """Monta a estrutura visual basica da aplicacao."""
        yield Header()
        yield Container(Static(app_bootstrap_message(), id="welcome"))
        yield Footer()
