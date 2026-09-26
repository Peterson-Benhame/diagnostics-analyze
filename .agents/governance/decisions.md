# Decisões

Registre decisões que alterem contratos, políticas, arquitetura ou escopo.

Formato: data, contexto, decisão, motivo e consequência.

## 2026-09-26 — Estrutura de workflow

- Contexto: o workflow inicial possuía specs planas e não tinha um ponto único de retomada.
- Decisão: adotar `pbs-spec-driven` com `.specs/STATE.md` e diretórios por feature.
- Motivo: reduzir contexto informal e tornar cada etapa verificável em uma nova sessão.
- Consequência: toda feature em execução mantém `spec.md`, `tasks.md` e `validation.md`.
