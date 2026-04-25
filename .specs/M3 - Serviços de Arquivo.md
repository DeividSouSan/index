# M3 - Serviços de Arquivo

## Objetivo
Construir a camada de integração com filesystem e sistema operacional para operações principais do Index.

## Escopo
- Implementar varredura do diretório alvo e leitura de PDFs.
- Implementar renomeação física de arquivos com tratamento de falhas.
- Implementar abertura de PDF via xdg-open.
- Implementar exclusão segura com send2trash.

## Critérios de aceite
1. O serviço retorna listas de artigos válidos e Uncategorized.
2. A renomeação aplica metadados no nome do arquivo sem inconsistência.
3. A abertura de artigo via Enter dispara xdg-open corretamente.
4. A exclusão via Del envia para lixeira e não usa rm direto.
5. Falhas de permissão ou arquivo inexistente retornam mensagem tratável pela UI.

## Entregáveis
- Serviços de listagem, renomeação, abertura e lixeira.
- Contratos de retorno de erro para consumo da interface.
- Testes unitários e de integração dos serviços.

## Status
Concluída.

## Validação de aceite
- [x] O serviço retorna listas de artigos válidos e Uncategorized.
- [x] A renomeação aplica metadados no nome do arquivo sem inconsistência.
- [x] A abertura de artigo via Enter dispara xdg-open corretamente.
- [x] A exclusão via Del envia para lixeira e não usa rm direto.
- [x] Falhas de permissão ou arquivo inexistente retornam mensagem tratável pela UI.

