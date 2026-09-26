# PBS Spec-Driven Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrar o workflow de IA para a estrutura e os gates do `pbs-spec-driven`.

**Architecture:** `AGENTS.md` direciona a retomada para `.specs/STATE.md`. Cada feature terá uma pasta autocontida; `.agents/` preserva contexto, políticas, avaliações e governança. O marketplace é opt-in e os validadores permanecem pertencentes à skill instalada.

**Tech Stack:** Markdown, Git e `@peterson-benhame/agent-skills`.

**Spec:** `docs/superpowers/specs/2026-09-26-ai-assisted-development-workflow-design.md`

## Global Constraints

- Nunca executar ou enviar conteúdo do repositório analisado.
- Toda feature possui spec e critérios de aceite antes do código.
- MCP permanece opcional.
- Push depende de autorização explícita do usuário.

## Review Focus

- Uma retomada deve localizar a feature ativa sem carregar todas as specs.
- A instalação das skills ou o MCP não podem ser obrigatórios.
- F001 e F002 não podem perder referências históricas.
- O estado global deve informar um próximo passo verificável.
- Validadores devem vir da skill instalada, não de cópias no produto.

---

### Task 1: Estrutura de estado e migração das features

**Files:**
- Create: `.specs/STATE.md`
- Create: `.specs/features/f001-inventory/spec.md`
- Create: `.specs/features/f002-ai-workflow/{spec,tasks,validation}.md`
- Delete: `.specs/features/F001-inventory.md`, `.specs/features/F002-ai-workflow.md`

- [ ] Criar inspeção que exige `STATE.md`, as duas specs migradas e os artefatos operacionais da F002.
- [ ] Verificar falha contra a estrutura plana atual.
- [ ] Migrar as features e atualizar a evidência em `validation.md`.
- [ ] Commit: `docs: migrate feature state to pbs layout`.

### Task 2: Entrada do agente, políticas e avaliação

**Files:**
- Modify: `AGENTS.md`, `.agents/policies/quality.md`, `.agents/evals/scenarios.md`
- Modify: `.agents/governance/{decisions,changelog}.md`

- [ ] Criar inspeção que exige `STATE.md`, feature ativa e validação antes de conclusão.
- [ ] Verificar falha contra as instruções atuais.
- [ ] Atualizar entrada, política, cenários e governança.
- [ ] Registrar evidência em `validation.md`.
- [ ] Commit: `docs: add spec-driven agent workflow gates`.

### Task 3: Instalação local e auditoria de harness

**Files:**
- Modify: `.agents/skills/README.md`, `.specs/features/f002-ai-workflow/{tasks,validation}.md`

- [ ] Criar inspeção que exige as três skills, escopo local, MCP opcional e origem dos validadores.
- [ ] Verificar falha contra a documentação atual.
- [ ] Documentar instalação, execução, auditoria e limitações reais do ambiente.
- [ ] Commit: `docs: document local marketplace skill workflow`.

## Self-Review

- Task 1 cobre estrutura e estado; Task 2 cobre gates e avaliações; Task 3 cobre instalação e auditoria.
- `AGENTS.md` lê `STATE.md`, que aponta para a feature ativa.
- A mudança é documental: não modifica a execução do diagnóstico nem adiciona dependência de runtime.

## Execution Handoff

O usuário autorizou criação e publicação na branch. A execução nativa aplica as três tarefas e termina com revisão independente.
