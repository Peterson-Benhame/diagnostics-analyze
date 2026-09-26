# F002 — Workflow de Desenvolvimento Assistido por IA

## Objetivo

Fazer com que qualquer sessão do Codex no VS Code consiga entender o produto, respeitar limites de segurança e continuar uma feature sem depender de contexto informal do chat.

## Resultado esperado

Antes de alterar código, o agente encontra as regras do projeto, a spec da feature e os critérios de validação. Ao concluir, deixa testes, decisões e o estado da feature atualizados.

## Escopo

- `AGENTS.md` como entrada obrigatória para agentes.
- Contexto versionado: produto, arquitetura e glossário.
- Políticas de segurança e qualidade.
- Estado global em `.specs/STATE.md` e artefatos de cada feature em diretórios próprios.
- Cenários de avaliação em `.agents/evals/`.
- Registro de decisões em `.agents/governance/`.
- Instalação local de skills compatíveis com Codex.

## Fora do escopo

- LLM em tempo de execução do produto.
- MCP obrigatório para executar o MVP.
- Agentes autônomos que executam código do repositório analisado.
- Banco vetorial, memória automática e sincronização externa.

## Estrutura

```text
AGENTS.md
.agents/
  context/{product,architecture,glossary}.md
  policies/{security,quality}.md
  evals/scenarios.md
  governance/{decisions,changelog}.md
.specs/
  STATE.md
  features/<feature>/
    spec.md
    context.md             # somente quando a feature exigir descoberta adicional
    design.md              # somente quando houver decisão de arquitetura
    tasks.md
    validation.md
```

## Fluxo obrigatório

1. Na retomada, ler `AGENTS.md`, `.specs/STATE.md` e apenas os artefatos da feature ativa.
2. **Specify:** registrar objetivo, critérios de aceite, escopo e limites em `spec.md` antes do código.
3. **Design:** registrar decisões, alternativas e riscos em `design.md` quando a mudança não for trivial.
4. **Tasks:** quebrar o trabalho em tarefas pequenas, com validação, em `tasks.md`.
5. **Execute:** implementar por TDD; cada tarefa concluída recebe validação e commit atômico.
6. Um Verifier independente revisa os critérios de aceite e as evidências antes de declarar a feature concluída.
7. Registrar decisões que mudem arquitetura, política ou contrato e atualizar `STATE.md`.
8. Só fazer push após autorização explícita do usuário e verificação explícita.

## Adoção do marketplace

O workflow segue `pbs-spec-driven`: Specify → Design → Tasks → Execute e um Verifier independente no fechamento. `harness-eval` avalia periodicamente `AGENTS.md`, regras e skills. As skills são instaladas no escopo local do projeto; MCP continua opcional.

O projeto declara a instalação local, reproduzível e opt-in das skills `pbs-spec-driven`, `harness-eval` e `security-best-practices`. Os validadores fornecidos pela skill são executados a partir da instalação da própria skill; não são copiados para scripts do produto. A ausência dessas skills não autoriza ignorar o workflow: o `AGENTS.md` mantém as regras equivalentes em texto.

## Migração dos artefatos atuais

- `.specs/features/F001-inventory.md` passa a `.specs/features/f001-inventory/spec.md`.
- `.specs/features/F002-ai-workflow.md` passa a `.specs/features/f002-ai-workflow/spec.md`.
- `tasks.md` e `validation.md` são criados por feature a partir deste workflow; `context.md` e `design.md` são criados somente quando necessários.
- `STATE.md` registra a feature ativa, o estágio, o último commit validado e o próximo passo. Ele é a fonte de retomada, não um histórico detalhado.
- `AGENTS.md` passa a encaminhar agentes para `STATE.md` e proíbe carregar indiscriminadamente todas as specs.

## Políticas essenciais

- Nunca executar, compilar, restaurar dependências ou enviar conteúdo do repositório que está sendo diagnosticado.
- Nunca ler `.env`, certificados, connection strings, `appsettings*.json` ou arquivos de credenciais para a F001.
- Evidência deve apontar caminho relativo, intervalo de linhas e hash; presença textual não prova defeito.
- Testes novos devem falhar antes da implementação.
- Achados inconclusivos não podem ser apresentados como violação confirmada.

## Avaliações iniciais

| Cenário | Resultado esperado |
| --- | --- |
| Feature sem spec | agente cria/solicita spec antes de alterar código |
| Caminho fora da raiz | agente rejeita a leitura |
| Teste falhando | agente não declara conclusão |
| Evidência não verificável | achado é rejeitado ou inconclusivo |

## Critérios de aceite

1. Um novo clone possui instrução de entrada para Codex.
2. Produto, arquitetura, glossário, políticas e specs estão separados.
3. F001 é referenciada como baseline do MVP.
4. Todo cenário inicial possui resultado esperado verificável.
5. Nenhuma regra autoriza executar código do repositório analisado.
6. O workflow funciona somente com arquivos versionados; MCP permanece opcional.
7. Um novo clone pode instalar as skills do marketplace e seguir o ciclo Specify → Design → Tasks → Execute.
8. O repositório contém `STATE.md` e uma estrutura por feature compatível com o validador do `pbs-spec-driven`.
9. O fechamento de uma feature exige evidência de validação e revisão independente.
