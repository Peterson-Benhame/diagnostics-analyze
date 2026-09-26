# Skills locais

No diretório raiz do projeto, instale as skills no escopo local do Codex:

```bash
npx @peterson-benhame/agent-skills install -s pbs-spec-driven harness-eval security-best-practices
```

Não use instalação global. MCP é opcional nesta fase.

## Uso no workflow

- `pbs-spec-driven`: conduz Specify → Design → Tasks → Execute e exige um Verifier independente no fechamento.
- `harness-eval`: audita periodicamente `AGENTS.md`, políticas, contexto, specs e skills instaladas.
- `security-best-practices`: complementa as políticas de segurança do repositório.

Os validadores pertencem às skills instaladas e **não são copiados** para scripts do produto. Se a instalação não estiver disponível no ambiente, siga as regras equivalentes em `AGENTS.md` e registre a limitação em `validation.md`; essa indisponibilidade **não bloqueia a conclusão** do workflow documentado.
