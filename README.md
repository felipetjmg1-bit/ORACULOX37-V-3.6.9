# 🌌 Chat-GPT Aurora: Inteligência Artificial para Speckle Automate

O **Chat-GPT Aurora** é uma função para o **Speckle Automate** que integra o poder dos modelos de linguagem de grande porte (LLMs) da OpenAI para realizar análises inteligentes, auditorias e otimizações em modelos BIM diretamente no ecossistema Speckle.

## 🚀 Funcionalidades

- **Análise Semântica**: Interpreta a estrutura do modelo e identifica inconsistências lógicas.
- **Auditoria Automatizada**: Verifica se os tipos de objetos e parâmetros estão de acordo com as diretrizes do projeto.
- **Relatórios em Markdown**: Gera relatórios detalhados anexados diretamente à versão do modelo no Speckle.
- **Flexibilidade de Prompt**: Permite que o usuário defina o foco da análise (ex.: "Verifique a consistência estrutural" ou "Sugira melhorias de eficiência energética").

## 🛠️ Como Funciona

A função extrai os metadados dos objetos BIM via Speckle SDK, resume a estrutura do modelo e utiliza a API da OpenAI (Aurora) para processar esses dados. O resultado é devolvido ao usuário como um status de execução e um arquivo de relatório persistente.

## 📋 Pré-requisitos

- Conta no [Speckle](https://speckle.xyz/)
- Chave de API da [OpenAI](https://platform.openai.com/)
- Projeto configurado no Speckle Automate

## ⚙️ Configuração de Entrada

Ao configurar esta função no Speckle Automate, você precisará fornecer:

| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `openai_api_key` | Secret | Sua chave secreta da API OpenAI. |
| `analysis_prompt` | String | Instruções específicas para a IA Aurora. |

## 📦 Instalação e Desenvolvimento Local

Se você deseja modificar ou testar a função localmente:

1. Clone o repositório:
   ```bash
   git clone https://github.com/felipetjmg1-bit/Chat-gpt-aurora-.git
   ```

2. Instale as dependências:
   ```bash
   pip install .
   ```

3. Execute os testes:
   ```bash
   pytest
   ```

## 📄 Licença

Este projeto está licenciado sob a licença **Apache-2.0**.

---

**Desenvolvido para levar a Inteligência Artificial ao coração do BIM com Speckle.**
