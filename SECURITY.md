# Segurança

O Oráculo X-37 é um protótipo experimental. O repositório não possui certificação de segurança, não promete prazo de correção e não deve ser considerado adequado para dados confidenciais ou uso operacional sem avaliação independente.

## Como reportar uma vulnerabilidade

Não publique credenciais, dados BIM confidenciais ou detalhes exploráveis em uma issue pública. Se o recurso de **private vulnerability reporting** estiver habilitado na aba **Security** deste repositório, use-o para enviar o relato. Caso não esteja disponível, entre em contato com o mantenedor pelo [perfil GitHub](https://github.com/felipetjmg1-bit) antes de divulgar publicamente.

Inclua, quando possível, a versão/commit afetado, passos mínimos de reprodução e o impacto observado. Remova tokens, chaves e dados de clientes do material enviado.

## Segredos e dados externos

Use entradas secretas do Speckle Automate para credenciais. Não faça commit de tokens, chaves de API ou dados de projetos. Quando uma chave OpenAI é configurada, o código envia o prompt e um resumo agregado por tipo; revise nomes de tipos e prompts para evitar transmitir informação confidencial.
