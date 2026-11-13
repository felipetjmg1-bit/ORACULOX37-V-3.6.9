"""Oráculo X-37: exploratory BIM checks for Speckle Automate.

The local rules report simple counts only. They are not a structural
engineering assessment, compliance certification, risk model, or XAI system.
"""

import logging
import re
from html import escape
from pathlib import Path

from openai import OpenAI
from pydantic import Field, SecretStr
from speckle_automate import (
    AutomateBase,
    AutomationContext,
    execute_automate_function,
)

from audit import AuditResult, audit_objects, format_audit_summary
from flatten import flatten_base

logger = logging.getLogger(__name__)


class FunctionInputs(AutomateBase):
    """Optional external commentary settings for the Speckle function."""

    openai_api_key: SecretStr | None = Field(
        default=None,
        title="OpenAI API Key (optional)",
        description=(
            "Optional. If provided, aggregate object-type counts and the prompt "
            "are sent to OpenAI for non-authoritative commentary."
        ),
    )
    analysis_prompt: str = Field(
        default=(
            "Summarize the aggregate BIM object counts below. Do not infer "
            "structural safety, regulatory compliance, causal relationships, "
            "or risk scores. Clearly state that the result is not an "
            "engineering assessment."
        ),
        title="Optional commentary prompt",
        description="Instructions for the optional external text commentary.",
    )


def _metric_values(result: AuditResult) -> dict[str, int | str]:
    """Return labels and observed counts for presentation in the report."""
    material_count: int | str = (
        result.structural_objects_without_material
        if result.structural_objects
        else "not assessed"
    )
    return {
        "Objects traversed": result.total_objects,
        "Object types found": len(result.object_types),
        "Structural objects (name heuristic)": result.structural_objects,
        "Structural objects without material": material_count,
        "Objects without ID": result.objects_without_id,
        "Extra occurrences of duplicate IDs": result.duplicate_id_occurrences,
        "Distinct duplicate ID values": result.distinct_duplicate_ids,
    }


def generate_html_report(
    analysis_result: str,
    data_summary: str,
    object_types: dict[str, int],
    audit_metrics: dict[str, int | str],
) -> str:
    """Render an HTML report with all dynamic text escaped as plain text."""
    type_rows = "".join(
        "<tr><td>"
        + escape(str(type_name), quote=True)
        + "</td><td>"
        + escape(str(count), quote=True)
        + "</td></tr>"
        for type_name, count in sorted(object_types.items())
    )
    metric_rows = "".join(
        "<li><strong>"
        + escape(str(label), quote=True)
        + ":</strong> "
        + escape(str(value), quote=True)
        + "</li>"
        for label, value in audit_metrics.items()
    )

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Oráculo X-37 — Relatório exploratório BIM</title>
  <style>
    :root {{ color-scheme: light; font-family: system-ui, sans-serif; }}
    body {{ margin: 0; padding: 2rem 1rem; background: #f3f6fb; color: #17243a; }}
    main {{ max-width: 980px; margin: auto; padding: 2rem; background: #fff;
            border: 1px solid #d8e0ea; border-radius: 14px; }}
    h1, h2 {{ color: #123b67; }}
    .notice {{ padding: 1rem; background: #fff4d6; border-left: 4px solid #d89400; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; background: #f5f7fa;
          padding: 1rem; border-radius: 8px; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ text-align: left; padding: .65rem; border-bottom: 1px solid #d8e0ea; }}
    footer {{ margin-top: 2rem; color: #52647a; font-size: .9rem; }}
  </style>
</head>
<body>
  <main>
    <h1>Oráculo X-37 — relatório exploratório BIM</h1>
    <p class="notice"><strong>Limitação:</strong> este relatório contém verificações
    heurísticas e contagens. Não certifica conformidade, segurança estrutural,
    risco, nem fornece uma avaliação de engenharia ou explicabilidade de modelo.
    </p>
    <h2>Resumo observado</h2>
    <pre>{escape(data_summary, quote=True)}</pre>
    <h2>Contagens da auditoria local</h2>
    <ul>{metric_rows}</ul>
    <h2>Distribuição por tipo</h2>
    <table><thead><tr><th>Tipo</th><th>Quantidade</th></tr></thead>
    <tbody>{type_rows}</tbody></table>
    <h2>Comentário externo opcional</h2>
    <pre>{escape(analysis_result, quote=True)}</pre>
    <footer>Impulso Digital — protótipo experimental. Revise os dados e as regras
    antes de qualquer uso operacional.</footer>
  </main>
</body>
</html>
"""


def _optional_external_commentary(
    api_key: SecretStr | None,
    prompt: str,
    data_summary: str,
) -> str:
    """Request optional commentary using aggregate data, never raw BIM objects."""
    if api_key is None or not api_key.get_secret_value().strip():
        return (
            "Comentário externo não solicitado. Este relatório contém apenas "
            "contagens e verificações heurísticas locais."
        )

    try:
        client = OpenAI(api_key=api_key.get_secret_value(), timeout=30.0)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Summarize only the aggregate counts supplied by the user. "
                        "Do not claim to perform structural calculations, certify "
                        "regulatory compliance, estimate risk, or provide XAI. "
                        "State that this text is non-authoritative commentary."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"{prompt.strip()}\n\nAggregate audit summary:\n{data_summary}"
                    ),
                },
            ],
            max_tokens=300,
            temperature=0.2,
        )
        content = response.choices[0].message.content
        if content and content.strip():
            return (
                "Comentário gerado por OpenAI (não é validação técnica):\n\n"
                + content.strip()
            )
        return "OpenAI não retornou comentário. Consulte apenas as contagens locais."
    except Exception as error:
        return (
            "Comentário externo indisponível ("
            f"{type(error).__name__}). O relatório contém apenas as verificações "
            "determinísticas locais."
        )


def _mark_failed(context: AutomationContext, message: str) -> None:
    """Try to mark the Speckle run as failed without hiding the original error."""
    try:
        context.mark_run_failed(message)
    except Exception:
        pass


def _markdown_code_block(text: str) -> str:
    """Wrap untrusted text in a fence longer than any backtick run in it."""
    longest_run = max((len(run) for run in re.findall(r"`+", text)), default=0)
    fence = "`" * max(3, longest_run + 1)
    return f"{fence}text\n{text}\n{fence}"


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:
    """Run simple local checks and store reports in the Speckle Automation run."""
    try:
        version_root_object = automate_context.receive_version()
        if version_root_object is None:
            raise ValueError("Speckle did not provide a model version object.")

        objects = list(flatten_base(version_root_object))
        if not objects:
            raise ValueError(
                "The received model version contains no traversable objects."
            )

        result = audit_objects(objects)
        data_summary = format_audit_summary(result)
        commentary = _optional_external_commentary(
            getattr(function_inputs, "openai_api_key", None),
            getattr(function_inputs, "analysis_prompt", "") or "",
            data_summary,
        )
        metrics = _metric_values(result)
        html_report = generate_html_report(
            commentary,
            data_summary,
            result.object_types,
            metrics,
        )
        markdown_report = (
            "# Oráculo X-37 — relatório exploratório BIM\n\n"
            "> Protótipo heurístico; não é avaliação de engenharia, certificação de "
            "conformidade, cálculo estrutural, modelo de risco ou explicabilidade "
            "de modelo.\n\n"
            "## Resumo observado\n\n"
            f"{_markdown_code_block(data_summary)}\n\n"
            "## Comentário externo opcional\n\n"
            f"{_markdown_code_block(commentary)}\n"
        )

        html_path = Path("relatorio_aurora.html")
        markdown_path = Path("relatorio_aurora.md")
        html_path.write_text(html_report, encoding="utf-8")
        markdown_path.write_text(markdown_report, encoding="utf-8")
        automate_context.store_file_result(str(html_path))
        automate_context.store_file_result(str(markdown_path))
        automate_context.mark_run_success(
            f"Verificações heurísticas concluídas para {result.total_objects} objetos."
        )
    except Exception as error:
        logger.error("BIM audit did not complete (%s).", type(error).__name__)
        _mark_failed(
            automate_context,
            f"Auditoria não concluída ({type(error).__name__}); "
            "consulte os logs da automação.",
        )


if __name__ == "__main__":
    execute_automate_function(automate_function, FunctionInputs)
