# M6 - Ações do Usuário

## Objetivo
Concluir os fluxos interativos principais orientados a teclado para operação diária do Index.

## Escopo
- Enter: abrir artigo selecionado.
- E: abrir modal de edição de metadados.
- Del: confirmar exclusão e enviar para lixeira.
- S: abrir configurações e alterar diretório alvo.
- Recarregar listagem após ações internas que mudam o estado.

## Critérios de aceite
1. Enter abre o PDF selecionado corretamente.
2. E permite editar Status, Origem, Autor e Título com persistência via rename.
3. Del move item para lixeira e remove da lista atual após refresh interno.
4. S abre configurações e altera diretório em runtime.
5. Erros operacionais são apresentados com feedback claro ao usuário.

## Entregáveis
- Modais de edição e confirmação.
- Mapeamento completo de atalhos definidos no PRD.
- Fluxo funcional ponta a ponta dentro da TUI.

## Status
Concluída.

## Validação de aceite
- [x] Enter abre o PDF selecionado usando o visualizador padrão do sistema.
- [x] 'E' abre modal de edição e aplica renomeação física no disco com sucesso.
- [x] 'Del' solicita confirmação e move o arquivo para a lixeira via `send2trash`.
- [x] 'S' permite alterar o diretório de trabalho e recarrega a biblioteca instantaneamente.
- [x] Notificações flutuantes confirmam o sucesso ou erro de cada operação.

