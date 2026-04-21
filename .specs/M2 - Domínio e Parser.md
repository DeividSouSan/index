# M2 - Domínio e Parser

## Objetivo
Implementar o núcleo de dados e o parser do contrato de arquivos PDF com validação determinística.

## Escopo
- Criar modelos de domínio para Artigo e Configuração.
- Implementar parser para os formatos canônicos:
  - [Status] [Origem] [Autor] Título do Artigo.pdf
  - [Status] [Origem] Título do Artigo.pdf
- Implementar formatter para reconstruir nome de arquivo a partir dos metadados.
- Classificar arquivos em válidos e Uncategorized sem quebrar execução.

## Regras fechadas
- Status fixo no MVP: OK e NOK.
- Origem livre (texto não vazio).
- Autor opcional.
- Extensão aceita: .pdf.

## Critérios de aceite
1. O parser identifica corretamente arquivos válidos e inválidos.
2. Arquivos inválidos são encaminhados para Uncategorized sem erro fatal.
3. O formatter gera nomes compatíveis com o contrato.
4. Casos de borda (autor ausente, acentos, espaços) estão cobertos em testes.

## Entregáveis
- Modelos de domínio.
- Parser e formatter do contrato.
- Testes unitários do núcleo de parsing.
