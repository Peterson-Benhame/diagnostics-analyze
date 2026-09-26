# Validação — F002

## Evidências

- 2026-09-26: `pytest tests/contract/test_ai_workflow_docs.py::test_spec_driven_feature_layout_has_active_feature_artifacts -q` aprovou a presença de `STATE.md` e dos artefatos obrigatórios da F002.
- 2026-09-26: `pytest tests/contract/test_ai_workflow_docs.py::test_agent_entrypoint_requires_state_active_feature_and_validation -q` aprovou as regras de retomada e conclusão em `AGENTS.md`.
- 2026-09-26: a inspeção da documentação local das skills foi aprovada pelo teste de contrato.
- 2026-09-26: a instalação foi tentada com `npx @peterson-benhame/agent-skills install -s pbs-spec-driven harness-eval security-best-practices`. O CLI foi baixado, mas o catálogo não pôde ser consultado por falha de rede/DNS (`EAI_AGAIN registry.npmjs.org` e `Failed to fetch registry`). Nenhuma skill foi marcada como instalada.
- Próximo passo: repetir a instalação em uma rede com acesso ao npm/CDN e executar os validadores fornecidos pelas skills.

## Revisão independente

- 2026-09-26: revisão independente do intervalo `301aeb5..87f934a` encontrou três ajustes importantes: preservar a fonte da F001, descobrir `context.md`/`design.md` quando existirem e tornar o teste de estado independente da F002 ativa.
- 2026-09-26: os ajustes foram aplicados por TDD. `pytest tests/contract/test_ai_workflow_docs.py -q` aprovou 5 testes de contrato.

## Limitação de baseline

Em 2026-09-26, `pytest -q` retornou 18 testes aprovados e 1 falhando: `test_scan_stops_once_the_entry_limit_is_reached`. A falha pertence à F001 e não é evidência de conclusão desta feature.
