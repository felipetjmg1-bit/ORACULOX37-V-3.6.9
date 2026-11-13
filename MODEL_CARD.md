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

# Oráculo X-37 — cartão de software

## O que é

Este repositório contém uma função Python experimental para Speckle Automate. O código percorre objetos BIM e produz contagens por tipo, além de regras simples para presença de IDs e da propriedade `material` em tipos identificados por uma heurística textual.

## Estágio de desenvolvimento

O Oráculo X-37 é um protótipo de nível inicial a intermediário, desenvolvido como parte do aprendizado aplicado do autor com Python e Speckle Automate. A função oferece comentário externo opcional pela API da OpenAI.

FastAPI, MCP e Gradio são estudados em experimentos separados e não são funcionalidades nem dependências deste repositório. O projeto não reivindica tecnologia proprietária disruptiva nem validação comercial consolidada.

## Não é um modelo de machine learning

O repositório não contém pesos de modelo, conjunto de treinamento, benchmark ou resultados de precisão validados. Não existe pontuação de conformidade de 95,5% ou outra métrica de desempenho publicada por este projeto. O comentário opcional gerado pela API da OpenAI é texto auxiliar, não uma previsão, explicação de modelo ou validação independente.

## Uso pretendido e limites

A ferramenta pode apoiar exploração e revisão preliminar de metadados. Ela não realiza cálculos estruturais, não interpreta integralmente propriedades BIM, não certifica conformidade e não deve embasar decisões de engenharia ou segurança sem validação independente.

A identificação de tipos estruturais usa apenas correspondência de palavras (`structure`, `beam`, `column`, `wall`). A verificação de material observa a propriedade `material`; essas regras são incompletas e podem produzir falsos positivos ou negativos.

## Dados e serviço externo

A função pode ser executada sem chave de OpenAI. Se uma chave for configurada, o código envia o prompt fornecido e um resumo agregado por tipo para a API externa. Objetos BIM individuais e IDs não são incluídos nesse resumo. Nomes de tipos e prompts ainda podem ser sensíveis e devem ser avaliados antes do envio.

## Avaliação

Os testes automatizados cobrem comportamento de funções, contagens e escape de conteúdo HTML com objetos sintéticos. Eles não demonstram desempenho em projetos BIM reais, segurança, conformidade normativa nem validade de engenharia.
