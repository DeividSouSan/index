# **Product Requirements Document (PRD): Index**

## **1\. Visão Geral do Produto**

O **Index** é um aplicativo de terminal (Text User Interface) voltado para ambientes Linux. Seu objetivo é atuar como um organizador visual e rápido para bibliotecas de artigos salvos localmente em formato PDF. O sistema adota uma arquitetura onde o sistema de arquivos atua como banco de dados ("File System as Database"), utilizando um contrato rígido de nomenclatura para extrair e gerenciar metadados de leitura (status, origem, autor e título).

## **2\. Contrato de Dados (Nomenclatura de Arquivos)**

A espinha dorsal da aplicação é um **contrato determinístico e explícito** de nomenclatura de arquivos PDF. O parser extrai metadados com base em colchetes como delimitadores, sem heurísticas de interpretação.

### **Padrões Aceitos**

**Sem Autor (3 colchetes):**
```
[Status] [Origem] Título.pdf
```

**Com Autor (4 colchetes):**
```
[Status] [Origem] [Autor] Título.pdf
```

### **Especificação de Campos**

| Campo | Obrigatório | Restrições | Exemplos |
|-------|------------|-----------|----------|
| **Status** | ✅ Sim | Deve ser "OK" ou "NOK" (case-sensitive) | `[OK]`, `[NOK]` |
| **Origem** | ✅ Sim | **SEM espaços**, pode ter caracteres especiais | `[TabNews]`, `[Medium-BR]`, `[Dev.to]` |
| **Autor** | ❌ Opcional | **SEM espaços**, pode ter caracteres especiais | `[filipedeschamps]`, `[john_doe]`, `[MartinFowler]` |
| **Título** | ✅ Sim | **CAN ter espaços**, sem colchetes, não vazio | `Machine Learning Basics`, `Why TypeScript matters?` |
| **Extensão** | ✅ Sim | Apenas `.pdf` (case-insensitive) | `.pdf`, `.PDF` |

### **Exemplos Válidos**

* `[OK] [TabNews] [filipedeschamps] Teste.pdf`
* `[NOK] [Devto] [JorgeFerreira] Testando testes.pdf`
* `[OK] [MartinFowler] [MartinFowler] DDD.pdf`
* `[OK] [Anthropic] Claude is dangerous?.pdf` (sem autor)
* `[NOK] [Medium-BR] Learning Rust in 2024.pdf` (sem autor)

### **Exemplos Inválidos (Rejeitados)**

| Exemplo | Motivo |
|---------|--------|
| `[OK Anthropic] Teste.pdf` | Status não fecha colchete |
| `[OK] [Origin Space] [Author] Title.pdf` | Origem contém espaço |
| `[OK] [Origin] [Author Name] Title.pdf` | Autor contém espaço |
| `[NOK] [Autor] Titulo.pdf` | Falta segundo colchete (origem obrigatória) |
| `[NOK] [JournalDaFatec] [Valeria].pdf` | Título vazio |
| `[PENDING] [Origin] [Author] Title.pdf` | Status não é "OK" nem "NOK" |
| `[OK] [Origin] [Author] Title.doc` | Extensão não é `.pdf` |

### **Princípios de Design**

* **Determinístico:** Sem heurísticas ou interpretação. Colchetes definem explicitamente cada campo.
* **Sem Recuperação:** Qualquer desvio do contrato resulta em arquivo inválido (retorna `None`).
* **Responsabilidade do Usuário:** A nomeação correta é responsabilidade de quem cria/renomeia o arquivo.
* **Classificação Automática:** Arquivos inválidos são isolados na aba "Uncategorized" sem gerar erros.

### **Comportamento do Parser**

* **Entrada Válida:** Retorna objeto `Article` com metadados extraídos.
* **Entrada Inválida:** Retorna `None` (sem lançar exceção).
* **Extensão Não-.pdf:** Ignorado pelo parser (não processado).

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