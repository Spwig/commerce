---
template_type: password_reset
category: Authentication
---

# Email Template: password_reset

## Subject
Solicitação de Redefinição de Senha

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Solicitação de Redefinição de Senha
        </mj-text>
        <mj-text>
          Nós recebemos uma solicitação para redefinir sua senha. Clique no botão abaixo para redefini-la.
        </mj-text>
        <mj-button href="{{ reset_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Redefinir Senha
        </mj-button>
        <mj-text color="#666666" font-size="12px">
          Se você não solicitou isso, pode ignorar este e-mail com segurança.
        </mj-text>
        <mj-text color="#666666" font-size="12px">
          Este link expirará em {{ expiry_hours }} horas.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Solicitação de Redefinição de Senha

Nós recebemos uma solicitação para redefinir sua senha. Clique no link abaixo para redefini-la.

{{ reset_url }}

Se você não solicitou isso, pode ignorar este e-mail com segurança.
Este link expirará em {{ expiry_hours }} horas.