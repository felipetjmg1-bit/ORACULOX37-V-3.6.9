"""Tests for deterministic BIM checks and report safety."""

from types import SimpleNamespace
from unittest.mock import Mock

from pydantic import SecretStr

import main
from audit import audit_objects, format_audit_summary
from flatten import flatten_base
from main import FunctionInputs, automate_function, generate_html_report


def test_flatten_base_handles_cycles_and_includes_root() -> None:
    """Ensure traversal includes the root and terminates on cycles."""
    root = SimpleNamespace(speckle_type="Root", elements=[])
    child = SimpleNamespace(speckle_type="Beam", elements=[root])
    root.elements.append(child)

    result = list(flatten_base(root))

    assert result == [root, child]


def test_flatten_base_handles_self_referential_collection() -> None:
    """Ensure a cyclic collection cannot cause an infinite traversal."""
    cyclic_elements = []
    cyclic_elements.append(cyclic_elements)
    root = SimpleNamespace(speckle_type="Root", elements=cyclic_elements)

    assert list(flatten_base(root)) == [root]


def test_audit_objects_reports_observed_counts_only() -> None:
    """Check that audit output contains actual counts and no raw IDs."""
    objects = [
        SimpleNamespace(
            speckle_type="Objects.BuiltElements.Beam", id="duplicate", material=""
        ),
        SimpleNamespace(
            speckle_type="Objects.BuiltElements.Column",
            id="duplicate",
            material={"name": "steel"},
        ),
        SimpleNamespace(speckle_type="Objects.BuiltElements.Wall", id=None),
        SimpleNamespace(speckle_type="Objects.Other", id="unique"),
    ]

    result = audit_objects(objects)
    summary = format_audit_summary(result)

    assert result.total_objects == 4
    assert result.structural_objects == 3
    assert result.structural_objects_without_material == 2
    assert result.objects_without_id == 1
    assert result.duplicate_id_occurrences == 1
    assert result.distinct_duplicate_ids == 1
    assert "duplicate" not in summary
    assert "conformidade" in summary
    assert "não verifica" in summary


def test_html_report_escapes_dynamic_content() -> None:
    """Ensure dynamic model fields cannot inject markup into the HTML report."""
    report = generate_html_report(
        "<script>alert('x')</script>",
        "<img src=x onerror=alert(1)>",
        {"<svg onload=alert(1)>": 1},
        {"<b>metric</b>": "<i>value</i>"},
    )

    assert "<script>alert" not in report
    assert "<img src=x" not in report
    assert "<svg onload" not in report
    assert "<b>metric</b>" not in report
    assert "&lt;script&gt;" in report
    assert "&lt;img" in report


def test_markdown_code_block_contains_embedded_fences() -> None:
    """Ensure embedded code fences remain inside the generated text block."""
    content = "```\n## injected heading\n```"

    block = main._markdown_code_block(content)

    assert block.startswith("````text\n")
    assert block.endswith("\n````")
    assert content in block


def test_optional_commentary_is_not_requested_without_key(monkeypatch) -> None:
    """Ensure no OpenAI client is constructed when a key is not configured."""
    openai_constructor = Mock(side_effect=AssertionError("OpenAI must not be called"))
    monkeypatch.setattr(main, "OpenAI", openai_constructor)

    commentary = main._optional_external_commentary(None, "prompt", "counts")

    assert "não solicitado" in commentary
    openai_constructor.assert_not_called()


def test_optional_commentary_failure_does_not_claim_analysis(monkeypatch) -> None:
    """Ensure an external API failure is clearly reported without fake findings."""
    openai_constructor = Mock(side_effect=RuntimeError("offline"))
    monkeypatch.setattr(main, "OpenAI", openai_constructor)

    commentary = main._optional_external_commentary(
        SecretStr("sk-test-key"), "prompt", "aggregate counts"
    )

    assert "indisponível" in commentary
    assert "RuntimeError" in commentary
    assert "risco baixo" not in commentary


def test_automation_stores_reports_for_received_model(monkeypatch, tmp_path) -> None:
    """Verify that received model data produces and stores both report formats."""
    monkeypatch.chdir(tmp_path)
    root = SimpleNamespace(
        speckle_type="Objects.Other.Root",
        id="root-id",
        elements=[
            SimpleNamespace(
                speckle_type="Objects.BuiltElements.Beam",
                id="beam-id",
                material=None,
            )
        ],
    )
    context = Mock()
    context.receive_version.return_value = root
    monkeypatch.setattr(
        main,
        "_optional_external_commentary",
        lambda api_key, prompt, summary: "Comentário não solicitado.",
    )

    automate_function(context, FunctionInputs())

    assert context.mark_run_success.call_count == 1
    assert context.mark_run_failed.call_count == 0
    assert context.store_file_result.call_count == 2
    html_report = (tmp_path / "relatorio_aurora.html").read_text(encoding="utf-8")
    markdown_report = (tmp_path / "relatorio_aurora.md").read_text(encoding="utf-8")
    assert "Objetos percorridos: 2" in html_report
    assert "Objetos sem ID preenchido: 0" in markdown_report
    assert "95.5%" not in html_report
    assert "Sistema OFFLINE" not in html_report


def test_automation_marks_missing_model_failed_without_fake_report(
    monkeypatch, tmp_path
) -> None:
    """Verify that missing model data fails the run and stores no fabricated report."""
    monkeypatch.chdir(tmp_path)
    context = Mock()
    context.receive_version.return_value = None

    automate_function(context, FunctionInputs())

    assert context.mark_run_failed.call_count == 1
    assert context.mark_run_success.call_count == 0
    context.store_file_result.assert_not_called()
    assert not (tmp_path / "relatorio_aurora.html").exists()


def test_function_inputs_accept_optional_key() -> None:
    """Verify the API key can be omitted or provided as a protected value."""
    inputs = FunctionInputs()
    assert inputs.openai_api_key is None

    configured = FunctionInputs(openai_api_key=SecretStr("sk-test-key"))
    assert configured.openai_api_key.get_secret_value() == "sk-test-key"

    from_schema = FunctionInputs.model_validate(
        {"openaiApiKey": "sk-test-key", "analysisPrompt": "summary only"}
    )
    assert from_schema.openai_api_key.get_secret_value() == "sk-test-key"
    assert from_schema.analysis_prompt == "summary only"
