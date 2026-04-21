"""Entrypoint da aplicacao Index."""

from index_tui.ui.app import IndexApp


def main() -> None:
    """Inicializa e executa a aplicacao TUI."""
    app = IndexApp()
    app.run()


if __name__ == "__main__":
    main()
