---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
Confirme seu cadastro em {{ store_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Confirme seu cadastro
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Obrigado por se cadastrar para receber notícias da {{ store_name }}! Confirme seu endereço de e-mail para começar a receber nossas atualizações e ofertas.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Confirmar cadastro
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Não conseguiu clicar no botão? Cole e cole este link no seu navegador:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Por que confirmar?</strong><br/>
          Confirmar seu e-mail nos ajuda a garantir que você realmente deseja nossas atualizações e mantém sua caixa de entrada livre de spam.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Não se cadastrou? Você pode ignorar este e-mail com segurança.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Confirme seu cadastro em {{ store_name }}

Obrigado por se cadastrar para receber notícias da {{ store_name }}! Confirme seu endereço de e-mail para começar a receber nossas atualizações e ofertas:

{{ confirmation_url }}

Confirmar seu e-mail nos ajuda a garantir que você realmente deseja nossas atualizações e mantém sua caixa de entrada livre de spam.

Não se cadastrou? Você pode ignorar este e-mail com segurança.