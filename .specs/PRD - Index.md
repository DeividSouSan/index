# **Product Requirements Document (PRD): Index**

## **1\. Visão Geral do Produto**

O **Index** é um aplicativo de terminal (Text User Interface) voltado para ambientes Linux. Seu objetivo é atuar como um organizador visual e rápido para bibliotecas de artigos salvos localmente em formato PDF. O sistema adota uma arquitetura onde o sistema de arquivos atua como banco de dados ("File System as Database"), utilizando um contrato rígido de nomenclatura para extrair e gerenciar metadados de leitura (status, origem, autor e título).

## **2\. Contrato de Dados (Nomenclatura de Arquivos)**

A espinha dorsal da aplicação é o padrão de nomenclatura dos arquivos PDF. O parser da aplicação deverá extrair metadados com base nestes formatos canônicos:

* `[Status] [Origem] [Autor] Título do Artigo.pdf`
* `[Status] [Origem] Título do Artigo.pdf` (quando autor estiver ausente)

Regras de validação:

* **Status:** Campo fixo no MVP. Valores aceitos: `OK` e `NOK`.
* **Origem:** Campo livre (qualquer texto não vazio entre colchetes).
* **Autor:** Opcional. Se ausente, o bloco `[Autor]` é omitido.
* **Título:** Obrigatório. Pode conter espaços e caracteres especiais.
* **Extensão:** Apenas `.pdf`.

Regex de referência para implementação:

`^\[(OK|NOK)\]\s+\[(.+?)\](?:\s+\[(.+?)\])?\s+(.+)\.pdf$`

## **3\. Arquitetura Visual (Interface)**

A interface será focada em teclado, rápida e reativa, dividida nas seguintes sessões:

* **Sistema de Abas:**
  * **Aba Principal:** Exibe os artigos que seguem estritamente o contrato de dados.
  * **Aba "Uncategorized":** Exibe arquivos PDF presentes no diretório alvo que não dão *match* com a regex do contrato. Eles não disparam erros, apenas são isolados.
* **Layout Principal:** O centro da interface será um DataTable interativo exibindo as colunas: Status, Origem, Autor e Título.
* **Navegação:** Totalmente guiada por teclado (setas para navegação de linhas, troca de foco por atalhos).
* **Modais:** Ações de edição ou configuração sobreporão a tela com janela flutuante centralizada.

## **4\. Requisitos Funcionais e Ações Mapeadas**

| Ação | Gatilho (Teclado) | Comportamento Esperado |
| :---- | :---- | :---- |
| **Abrir Artigo** | Enter | Executa o leitor de PDF padrão do Linux (via xdg-open) para o arquivo selecionado. |
| **Editar Metadados** | E | Abre um modal contendo formulários para Título, Status, Origem e Autor. Ao salvar, a aplicação renomeia o arquivo físico refletindo os novos dados sem quebrar o contrato. |
| **Excluir Artigo** | Del | Move o arquivo para a lixeira do SO, prevenindo exclusão acidental. Não realiza rm direto. |
| **Atualizar Lista** | R | Recarrega manualmente os arquivos do diretório alvo. |
| **Abrir Configurações** | S | Permite remapear o diretório alvo a qualquer momento. |

## **5\. Ciclo de Vida e Configuração de Estado**

A aplicação manterá a persistência de configuração sem depender de variáveis de ambiente do shell pai.

1. **Primeira Execução:** A aplicação não exibirá artigos. Solicitará ao usuário, via modal ou prompt interno no TUI, o caminho do diretório alvo.
2. **Persistência:** O diretório selecionado será salvo localmente em um arquivo JSON de configuração dotfile (Ex: `~/.config/index/config.json`).
3. **Tratamento de Estado Vazio:** Se o diretório estiver configurado mas não houver PDFs válidos, a interface exibirá centralizado o feedback visual: *"Nenhum artigo .pdf encontrado."*
4. **Edição de Caminho:** O usuário pode abrir as configurações para remapear o diretório sem reiniciar a aplicação.
5. **Atualização de Estado:** No MVP, a atualização da listagem é manual por atalho e automática apenas após ações internas (editar, excluir, alterar configuração). Não haverá watcher de filesystem em tempo real no MVP.

## **6\. Escopo do MVP**

Inclui:

* Parser do contrato com classificação entre Principal e Uncategorized.
* Listagem em DataTable com navegação por teclado.
* Ações Enter, E, Del, R e S.
* Persistência de configuração em `~/.config/index/config.json`.

Não inclui no MVP:

* Watcher automático de alterações externas no diretório.
* Pipeline de release/CI completo.
* Polimentos avançados de UX fora do fluxo principal.

## **7\. Stack Tecnológica Definida**

* **Linguagem:** Python 3.10+ (devido à maturidade em scripting para Linux e bibliotecas de TUI).
* **Framework UI:** Textual (responsável por componentes reativos, tabelas, abas, captura de teclado e modais).
* **Gerenciamento de Arquivos:**
  * os / pathlib: parsing, leitura de diretórios e renomeação.
  * send2trash: envio seguro de arquivos para a lixeira do sistema.
* **Integração de SO:** subprocess (chamada nativa do xdg-open).