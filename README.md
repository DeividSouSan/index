# Index

Index e um aplicativo TUI para organizacao de artigos PDF em Linux.

## Requisitos

- Python 3.10+
- UV instalado

## Setup rapido

1. Instalar dependencias:

```bash
uv sync --all-groups
```

2. Executar a aplicacao:

```bash
uv run index
```

Tambem e possivel executar com:

```bash
uv run python -m index_tui
```

## Estrutura inicial

- `index_tui/domain`: modelos e regras de dominio
- `index_tui/services`: servicos de integracao e casos de uso
- `index_tui/ui`: componentes de interface Textual
