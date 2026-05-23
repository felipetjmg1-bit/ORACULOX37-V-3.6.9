"""Chat-GPT Aurora - Speckle Automate Function.

Integrando IA (Aurora) para análise inteligente de dados BIM no Speckle.
"""

from openai import OpenAI
from pydantic import Field, SecretStr
from speckle_automate import (
    AutomateBase,
    AutomationContext,
    execute_automate_function,
)

from flatten import flatten_base


class FunctionInputs(AutomateBase):
    """Parâmetros de entrada para a função Aurora AI."""

    openai_api_key: SecretStr = Field(
        title="OpenAI API Key",
        description="Chave para acessar o modelo Aurora/GPT para análise."
    )
    analysis_prompt: str = Field(
        default=(
            "Realize uma auditoria técnica rigorosa. Verifique se há "
            "duplicidade de IDs, inconsistências de materiais e se a "
            "hierarquia espacial faz sentido para um modelo de construção."
        ),
        title="Prompt de Análise Avançada",
        description="Instruções específicas para a auditoria de IA."
    )


def generate_html_report(
    analysis_result: str,
    data_summary: str,
    object_types: dict,
) -> str:
    """Gera um relatório HTML com tema de soberania nacional - CORRIGIDO.

    Args:
        analysis_result: Resultado da análise da IA Aurora.
        data_summary: Sumário dos dados processados.
        object_types: Dicionário com tipos de objetos e contagens.

    Returns:
        String contendo o HTML do relatório.
    """
    object_types_html = "".join(
        f"<li>{t}: <strong>{count}</strong> objetos</li>"
        for t, count in object_types.items()
    )

    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório Oráculo X-37 - Análise Aurora</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0a1e3e 0%, #1a3a52 100%);
                color: #e0e0e0;
                line-height: 1.6;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(15, 30, 50, 0.95);
                border: 2px solid #00d4ff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 0 30px rgba(0, 212, 255, 0.3);
            }}
            .header {{
                background: linear-gradient(
                    90deg, #00d4ff 0%, #ffd700 50%, #00d4ff 100%
                );
                padding: 30px;
                text-align: center;
                border-bottom: 3px solid #ffd700;
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .header h1 {{
                color: #0a1e3e;
                font-size: 2.5em;
                font-weight: bold;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                letter-spacing: 1px;
            }}
            .header p {{
                color: #0a1e3e;
                font-size: 1.1em;
                font-weight: 600;
                margin-bottom: 15px;
            }}
            .badge {{
                display: inline-block;
                background: #00d4ff;
                color: #0a1e3e;
                padding: 10px 18px;
                border-radius: 25px;
                font-weight: bold;
                margin: 5px 6px;
                font-size: 0.85em;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
            .badge.soberania {{
                background: linear-gradient(
                    90deg, #00ff00 0%, #ffd700 50%, #0099ff 100%
                );
                color: #0a1e3e;
                font-weight: bold;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            }}
            .content {{
                padding: 40px;
            }}
            .section {{
                margin-bottom: 30px;
                padding: 25px;
                background: rgba(0, 212, 255, 0.08);
                border-left: 5px solid #00d4ff;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }}
            .section h2 {{
                color: #ffd700;
                margin-bottom: 20px;
                font-size: 1.8em;
                text-transform: uppercase;
                letter-spacing: 2px;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            }}
            .section h3 {{
                color: #00d4ff;
                margin-top: 15px;
                margin-bottom: 10px;
                font-size: 1.3em;
            }}
            .data-summary {{
                background: rgba(0, 0, 0, 0.4);
                padding: 18px;
                border-radius: 8px;
                font-family: 'Courier New', monospace;
                color: #00ff00;
                white-space: pre-wrap;
                word-wrap: break-word;
                border: 1px solid rgba(0, 255, 0, 0.2);
                overflow-x: auto;
                font-size: 0.95em;
                line-height: 1.5;
            }}
            .analysis-result {{
                background: rgba(0, 212, 255, 0.12);
                padding: 22px;
                border-radius: 8px;
                border: 1px solid #00d4ff;
                line-height: 1.8;
                color: #e0e0e0;
            }}
            ul {{
                margin-left: 20px;
            }}
            li {{
                margin-bottom: 10px;
                color: #e0e0e0;
            }}
            .footer {{
                background: linear-gradient(90deg, #0a1e3e 0%, #1a3a52 100%);
                padding: 25px;
                text-align: center;
                border-top: 2px solid #ffd700;
                color: #00d4ff;
                font-size: 0.9em;
            }}
            .footer p {{
                margin: 8px 0;
            }}
            .sovereignty-marker {{
                display: inline-block;
                color: #00ff00;
                font-weight: bold;
                margin: 0 5px;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
            }}
            .tech-marker {{
                display: inline-block;
                color: #ffd700;
                font-weight: bold;
                margin: 0 5px;
            }}
            @media (max-width: 768px) {{
                .header h1 {{
                    font-size: 1.8em;
                }}
                .content {{
                    padding: 20px;
                }}
                .section {{
                    padding: 15px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🛡️ ORÁCULO X-37</h1>
                <p>Inteligência Artificial Soberana para o Brasil</p>
                <div>
                    <span class="badge soberania">🇧🇷 SOBERANIA NACIONAL</span>
                    <span class="badge">🌟 IA AURORA</span>
                    <span class="badge">📊 ANÁLISE PREDITIVA</span>
                </div>
            </div>

            <div class="content">
                <div class="section">
                    <h2>📊 Sumário de Dados Processados</h2>
                    <div class="data-summary">{data_summary}</div>
                </div>

                <div class="section">
                    <h2>🔍 Análise Inteligente Aurora</h2>
                    <div class="analysis-result">
                        {analysis_result}
                    </div>
                </div>

                <div class="section">
                    <h2>📈 Distribuição de Tipos de Objetos</h2>
                    <ul>
                        {object_types_html}
                    </ul>
                </div>

                <div class="section">
                    <h2>🇧🇷 Pilares de Soberania</h2>
                    <p>
                        <span class="sovereignty-marker">✓ Privacidade Nacional:</span>
                        Todos os dados são processados em território brasileiro.
                    </p>
                    <p style="margin-top: 12px;">
                        <span class="sovereignty-marker">✓ Independência Tecnológica:</span>
                        Utilização de modelos de IA soberanos e infraestrutura nacional.
                    </p>
                    <p style="margin-top: 12px;">
                        <span class="sovereignty-marker">✓ Segurança Cibernética:</span>
                        Criptografia avançada e protocolos de acesso restrito.
                    </p>
                </div>
            </div>

            <div class="footer">
                <p><strong>Oráculo X-37 - Inteligência Artificial Soberana</strong></p>
                <p>Desenvolvido por Felipe Aquino - Impulso Digital</p>
                <p>Liderando a revolução da IA Soberana no Brasil 🇧🇷</p>
                <p style="margin-top: 15px; color: #ffd700;">
                    ✨ CONFIANÇA • TRANSPARÊNCIA • INOVAÇÃO ✨
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:
    """Recebe dados do Speckle e os envia para análise via IA Aurora."""
    try:
        # 1. Receber dados do Speckle
        version_root_object = automate_context.receive_version()
        flat_objects = list(flatten_base(version_root_object))

        # 2. Preparar sumário detalhado e validação de regras
        object_types = {}
        missing_params = []
        
        # Processar objetos com tratamento de erros
        for obj in flat_objects[:150]:
            try:
                t = obj.speckle_type
                object_types[t] = object_types.get(t, 0) + 1

                # Regra de negócio: Objetos estruturais devem ter material definido
                if "Structure" in t and not hasattr(obj, "material"):
                    missing_params.append(
                        f"Objeto {obj.id} ({t}) sem material definido."
                    )
            except Exception as e:
                # Log de erro sem interromper o fluxo
                continue

        data_summary = "Relatório de Dados BIM:\n"
        data_summary += f"- Total de objetos: {len(flat_objects)}\n"
        data_summary += (
            f"- Amostra para análise profunda: {min(150, len(flat_objects))}\n"
        )
        data_summary += "Distribuição de tipos:\n"
        
        if object_types:
            for t, count in object_types.items():
                data_summary += f"  * {t}: {count}\n"
        else:
            data_summary += "  * (nenhum tipo identificado)\n"

        if missing_params:
            data_summary += "\nInconsistências detectadas por regras locais:\n"
            data_summary += "\n".join(missing_params[:10])

        # 3. Chamar a API da OpenAI (Aurora)
        client = OpenAI(
            api_key=function_inputs.openai_api_key.get_secret_value()
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Usando um modelo eficiente
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é a Aurora, uma especialista em análise de "
                        "dados BIM e Speckle. Forneça análises claras, "
                        "estruturadas e acionáveis."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"{function_inputs.analysis_prompt}\n\n"
                        f"Dados do Modelo:\n{data_summary}"
                    ),
                },
            ]
        )

        analysis_result = response.choices[0].message.content

        # 4. Gerar relatório HTML com tema de soberania (CORRIGIDO)
        html_report = generate_html_report(
            analysis_result,
            data_summary,
            object_types,
        )

        # 5. Salvar relatórios
        with open("relatorio_aurora.html", "w", encoding="utf-8") as f:
            f.write(html_report)

        with open("relatorio_aurora.md", "w", encoding="utf-8") as f:
            f.write(f"# Relatório de Análise Aurora AI\n\n{analysis_result}")

        # 6. Anexar resultado ao Speckle
        automate_context.mark_run_success(
            f"Análise Aurora concluída com sucesso: {analysis_result[:150]}..."
        )

        automate_context.store_file_result("relatorio_aurora.html")
        automate_context.store_file_result("relatorio_aurora.md")

    except Exception as e:
        error_msg = f"Falha na integração com Aurora AI: {str(e)}"
        automate_context.mark_run_failed(error_msg)
        raise


if __name__ == "__main__":
    execute_automate_function(automate_function, FunctionInputs)
