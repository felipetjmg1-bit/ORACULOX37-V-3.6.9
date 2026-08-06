"""Run unit and integration tests for Oráculo X-37 XAI."""

import unittest
from unittest.mock import MagicMock
from pydantic import SecretStr
from main import FunctionInputs, automate_function, generate_html_report


class TestOraculoX37(unittest.TestCase):
    """Suíte de testes automatizados para o Oráculo X-37 XAI."""

    def test_function_inputs_validation(self):
        """Valida se a criação de inputs do Speckle Automate funciona corretamente."""
        inputs = FunctionInputs(
            openai_api_key=SecretStr("sk-test-key-12345"),
            analysis_prompt="Auditoria de teste para validação de XAI."
        )
        self.assertEqual(inputs.openai_api_key.get_secret_value(), "sk-test-key-12345")
        self.assertIn("XAI", inputs.analysis_prompt)

    def test_html_report_generation(self):
        """Verifica se o relatório HTML é gerado contendo os marcadores de Soberania e XAI."""
        analysis_text = "Análise simulada com sucesso pelo motor Aurora."
        summary = "Total de objetos: 100"
        obj_types = {"Beam": 50, "Column": 50}
        metrics = {"Conformidade": 95.5}

        html = generate_html_report(analysis_text, summary, obj_types, metrics)
        self.assertIn("ORÁCULO X-37 (XAI)", html)
        self.assertIn("Soberana", html)
        self.assertIn("Beam", html)

    def test_automate_function_fallback(self):
        """Testa a execução da função de automação com mock de contexto para garantir robustez offline."""
        mock_context = MagicMock()
        mock_context.receive_version.side_effect = Exception("No server connection")

        inputs = FunctionInputs(
            openai_api_key=SecretStr("sk-test-key-12345"),
            analysis_prompt="Teste offline"
        )

        # Não deve lançar exceção devido ao fallback robusto
        try:
            automate_function(mock_context, inputs)
            success = True
        except Exception:
            success = False

        self.assertTrue(success)


if __name__ == "__main__":
    unittest.main()
