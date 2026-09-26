# F002 — Workflow de desenvolvimento assistido por IA

## Objetivo

Permitir que uma nova sessão do Codex continue uma feature com contexto, regras, tarefas e evidências versionados.

## Documentos relacionados

- Design: `docs/superpowers/specs/2026-09-26-ai-assisted-development-workflow-design.md`
- Plano de execução: `docs/superpowers/plans/2026-09-26-pbs-spec-driven-workflow.md`

## Critérios de aceite

1. `AGENTS.md` encaminha a retomada para `.specs/STATE.md`.
2. Cada feature possui `spec.md`, `tasks.md` e `validation.md` quando está em execução.
3. O fluxo aplica Specify → Design → Tasks → Execute e revisão independente.
4. Skills do marketplace são locais e opcionais; MCP continua opcional.
5. O workflow não permite executar nem enviar conteúdo do repositório diagnosticado.

## Limites

Esta feature não adiciona LLM em runtime, MCP obrigatório, banco vetorial ou execução autônoma do repositório analisado.
