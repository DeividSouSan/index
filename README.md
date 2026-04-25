# 📚 Index

**Index** é um organizador de artigos e documentos PDF elegante para o terminal. Ele utiliza uma interface TUI (Text User Interface) moderna para ajudar você a manter sua biblioteca limpa, categorizada e acessível.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Textual](https://img.shields.io/badge/ui-Textual-orange.svg)

## ✨ Funcionalidades

- 📂 **Organização Automática**: Detecta metadados (Status, Origem, Autor, Título) diretamente do nome do arquivo.
- 🛠️ **Edição Rápida**: Modifique metadados e renomeie arquivos fisicamente no disco sem sair do terminal.
- 🔍 **Filtro Inteligente**: Separação automática entre artigos validados e arquivos "Uncategorized".
- 🚀 **Navegação Turbo**: Auto-complete de caminhos com `TAB` e preview visual de diretórios.
- 🗑️ **Segurança**: Integração com a lixeira do sistema (`send2trash`) para evitar perdas acidentais.

## 🚀 Instalação Rápida

O Index é construído com [uv](https://github.com/astral-sh/uv). Para instalar o comando `index` globalmente em sua máquina:

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/index.git
cd index

# Instale como uma ferramenta global
uv tool install .
```

## ⌨️ Atalhos de Teclado

| Tecla | Ação |
| :--- | :--- |
| `Enter` | Abre o PDF no visualizador padrão do sistema |
| `E` | Edita os metadados do artigo (Status, Autor, etc) |
| `Del` | Move o arquivo para a lixeira (com confirmação) |
| `S` | Configura o diretório alvo da biblioteca |
| `R` | Atualiza a listagem de arquivos |
| `Q` | Sai do aplicativo |

## 🛠️ Desenvolvimento e Contribuição

Se você deseja contribuir para o projeto:

1.  Faça o setup do ambiente de desenvolvimento:
    ```bash
    uv sync --all-groups
    ```
2.  Rode os testes para garantir a integridade:
    ```bash
    uv run pytest --cov=index_tui
    ```
3.  Crie uma branch para sua funcionalidade e abra um Pull Request.

---

> **Nota**: O Index é um projeto de verdade, mas também é um experimento de codificação agêntica.
