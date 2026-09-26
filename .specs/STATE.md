# Estado do projeto

## Feature ativa

- ID: F002 — Workflow de desenvolvimento assistido por IA
- Diretório: `.specs/features/f002-ai-workflow/`
- Estágio: Verify (bloqueado pela falha de baseline da F001)
- Último commit validado: `c46abe3` — achados da revisão independente corrigidos
- Próximo passo: corrigir a ordenação limitada da F001; a instalação local das skills pode ser repetida quando o catálogo do marketplace estiver acessível.

## Pendência conhecida

- F001 possui uma falha de baseline em `test_scan_stops_once_the_entry_limit_is_reached`; ela não é alterada pela F002.

`STATE.md` é a fonte de retomada. O histórico de decisões fica em `.agents/governance/`.
