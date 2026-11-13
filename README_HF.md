---
language:
  - pt
license: apache-2.0
tags:
  - bim
  - speckle
  - heuristic-rules
  - prototype
---

# Oráculo X-37 — função exploratória para Speckle Automate

Este repositório contém software Python experimental para percorrer objetos BIM recebidos pelo Speckle Automate, contar tipos e aplicar verificações heurísticas simples de presença de IDs e da propriedade `material`. Os resultados são publicados como relatórios HTML e Markdown.

## Escopo

O projeto **não contém um modelo de machine learning nem pesos treinados**. Não há benchmark ou métrica de precisão validada. O código não calcula estruturas, não estima risco, não certifica conformidade e não implementa explicabilidade de modelos. A chamada opcional à OpenAI fornece apenas comentário textual sobre contagens agregadas; não é validação técnica.

## Uso de dados

Sem `openaiApiKey`, nenhuma solicitação à OpenAI é feita. Quando a chave é informada, o código envia o prompt e contagens agregadas por tipo; não envia objetos individuais nem IDs pelo resumo. Nomes de tipos e prompts podem ser confidenciais e precisam de revisão antes do uso.

Para instalação, configuração, comandos e limitações, consulte o [README principal](README.md). O projeto está licenciado sob Apache-2.0.
