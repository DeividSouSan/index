# M4 - Configuração Persistente

## Objetivo
Implementar o ciclo de vida de configuração do diretório alvo com persistência local confiável.

## Escopo
- Criar leitura e escrita de config em ~/.config/index/config.json.
- Implementar fluxo de primeira execução pedindo diretório alvo.
- Permitir remapeamento do diretório em runtime pela interface.
- Tratar config ausente ou corrompida com recuperação segura.

## Critérios de aceite
1. Sem configuração prévia, o app solicita o diretório antes de listar arquivos.
2. Após salvar, a configuração persiste entre reinicializações.
3. O usuário consegue alterar o diretório sem reiniciar o app.
4. Configuração inválida não derruba o aplicativo e é recuperada.

## Entregáveis
- Módulo de persistência de configuração.
- Fluxo de primeira execução.
- Fluxo de remapeamento de diretório.
