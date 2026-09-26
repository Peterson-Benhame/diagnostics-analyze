# Code Diagnostics Core

## Retomada obrigatória

1. Leia `.specs/STATE.md`.
2. Leia `spec.md`, `tasks.md` e `validation.md` da **feature ativa** indicada no estado; leia também `context.md` e `design.md` quando existirem.
3. Leia somente o contexto e as políticas aplicáveis em `.agents/`.

Não carregue indiscriminadamente todas as features. Use o estado para decidir o que é relevante para a tarefa atual.

## Fluxo de trabalho

1. **Specify:** atualize a spec e os critérios de aceite antes de alterar código.
2. **Design:** registre decisões de arquitetura quando a mudança não for trivial.
3. **Tasks:** decomponha o trabalho em tarefas verificáveis.
4. **Execute:** use TDD, implementação mínima e commits atômicos.
5. **Verify:** atualize `validation.md`; um **Verifier independente** revisa evidências e critérios de aceite antes da conclusão.
6. Atualize `.specs/STATE.md`, decisões e changelog quando necessário.

Não declare uma feature concluída com validações pendentes ou testes falhando. Push exige autorização explícita do usuário.

Nunca execute, compile, restaure dependências ou envie conteúdo do repositório diagnosticado.
