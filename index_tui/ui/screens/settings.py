import os
from pathlib import Path
from textual import events
from textual.app import ComposeResult
from textual.containers import Grid, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Input


class SettingsModal(ModalScreen[str]):
    """Modal avançado para configurar o diretório com auto-complete e feedback visual."""

    def __init__(self, current_dir: str):
        super().__init__()
        self.current_dir = current_dir

    def compose(self) -> ComposeResult:
        with Grid(id="settings-grid"):
            yield Label("Configurar Diretório Alvo", id="settings-title")
            
            with Vertical(id="input-container"):
                yield Label("Caminho (use TAB para completar):", id="input-hint")
                yield Input(
                    value=self.current_dir, 
                    placeholder="Ex: ~/Downloads ou /home/user/docs", 
                    id="dir-input"
                )
                yield Label("", id="path-preview")
            
            yield Button("Cancelar", variant="primary", id="cancel")
            yield Button("Salvar", variant="success", id="save")

    def on_mount(self) -> None:
        self.update_preview(self.current_dir)
        self.query_one("#dir-input").focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Atualiza o feedback visual conforme o usuário digita."""
        self.update_preview(event.value)

    def update_preview(self, value: str) -> None:
        """Resolve o caminho e mostra o preview absoluto."""
        preview = self.query_one("#path-preview", Label)
        try:
            path = self.get_clean_path(value)
            
            if path.is_dir():
                preview.update(f"✔️ [green]Diretório válido:[/]\n{path}")
                preview.remove_class("invalid-path")
            else:
                preview.update(f"❌ [red]Caminho inválido ou não encontrado:[/]\n{path}")
                preview.add_class("invalid-path")
        except Exception:
            preview.update("⚠️ [yellow]Caminho malformado[/]")

    def on_key(self, event: events.Key) -> None:
        """Implementa o auto-complete ao apertar TAB."""
        if event.key == "tab":
            input_widget = self.query_one("#dir-input", Input)
            current_val = input_widget.value
            
            completed = self.attempt_autocomplete(current_val)
            if completed:
                input_widget.value = completed
                # Move o cursor para o final
                input_widget.cursor_position = len(completed)
                
            event.prevent_default()
            event.stop()

    def attempt_autocomplete(self, current_path_str: str) -> str | None:
        """Lógica de autocomplete para diretórios retornando caminhos absolutos."""
        try:
            # Trabalhamos sempre com o caminho resolvido para evitar ambiguidades
            p = self.get_clean_path(current_path_str)
            
            if p.exists() and p.is_dir():
                search_dir = p
                prefix = ""
            else:
                search_dir = p.parent
                prefix = p.name.lower()

            if not search_dir.exists():
                return None

            matches = [
                d for d in search_dir.iterdir() 
                if d.is_dir() and d.name.lower().startswith(prefix)
            ]

            if not matches:
                return None

            # Retorna o primeiro match absoluto como string
            return str(matches[0].absolute())

        except Exception:
            return None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            raw_value = self.query_one("#dir-input", Input).value
            clean_path = self.get_clean_path(raw_value)
            self.dismiss(str(clean_path))
        else:
            self.dismiss(None)

    def get_clean_path(self, value: str) -> Path:
        """Limpa aspas, escapes e resolve ~/ para retornar um Path absoluto."""
        clean = value.strip().strip("'").strip('"').replace("\\ ", " ")
        return Path(clean).expanduser().resolve()
