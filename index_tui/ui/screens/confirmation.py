from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class ConfirmationModal(ModalScreen[bool]):
    """Um modal simples para confirmação de ações (Sim/Não)."""

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        with Grid(id="confirmation-grid"):
            yield Label(self.message, id="confirmation-label")
            yield Button("Cancelar", variant="primary", id="cancel")
            yield Button("Confirmar", variant="error", id="confirm")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            self.dismiss(True)
        else:
            self.dismiss(False)
