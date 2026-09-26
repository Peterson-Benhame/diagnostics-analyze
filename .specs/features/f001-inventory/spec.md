# F001 — Inventário seguro

## Objetivo

Inventariar um repositório local e identificar projetos .NET sem executar, compilar, restaurar dependências ou enviar o conteúdo analisado.

## Fonte de escopo

`PRD-001-diagnostico-tecnico-dotnet.md` é a fonte histórica detalhada da F001. Esse documento ainda não está versionado neste clone; antes de ampliar o escopo, recupere-o ou crie uma nova spec versionada que substitua explicitamente suas decisões.

## Critérios de aceite

1. A entrada aceita somente uma raiz de repositório segura.
2. Links simbólicos, redirects e caminhos fora da raiz são rejeitados.
3. A saída contém caminhos relativos e achados rastreáveis.
4. A varredura respeita limites configurados.

## Status

Implementação existente; há uma falha de baseline registrada em `.specs/STATE.md` para a ordenação quando o limite de entradas é alcançado.
