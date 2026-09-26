# Cenários

| Cenário | Esperado |
| --- | --- |
| Novo clone | Codex encontra `AGENTS.md` e contexto |
| F001 | agente localiza a spec antes de editar |
| Feature sem spec | agente cria ou solicita `spec.md` antes de alterar código |
| Feature sem tarefas | agente registra `tasks.md` antes de executar mudança não trivial |
| Validação ausente | agente não declara a feature concluída |
| Teste falhando | agente registra a falha e não declara conclusão |
| Auditoria | Verifier independente revisa evidências e critérios de aceite |
