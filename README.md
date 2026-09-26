# Code Diagnostics Core

Ferramenta local para inventariar repositórios e produzir diagnósticos técnicos rastreáveis.

## Desenvolvimento

```bash
python -m pip install --group dev
python -m pytest
```

## Inventário local

```bash
diagnostics analyze --repo /caminho/repositorio --output /caminho/diagnosticos
```

Cada execução cria `<output>/<run-id>/inventory.json`. O comando não executa o código analisado nem lê conteúdos de arquivos nesta fase.

| Código | Significado |
| --- | --- |
| 0 | Inventário .NET concluído |
| 1 | Erro operacional |
| 2 | Argumento ou caminho inválido |
| 3 | Análise parcial ou sem `.csproj` elegível |
