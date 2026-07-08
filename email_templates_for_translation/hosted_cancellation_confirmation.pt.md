---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
Cancelamento Confirmado - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Cancelamento Confirmado
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Olá {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Sua assinatura <strong>{{ plan_name }}</strong> foi cancelada.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          O Que Acontece em Seguida
        </mj-text>
        <mj-text font-size="14px">
          Você continuará com acesso completo até <strong>{{ access_until_date }}</strong>.
        </mj-text>
        <mj-text font-size="14px">
          Após esse período, os dados do seu loja serão preservados por 30 dias até <strong>{{ termination_date }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Se quiser exportar seus dados antes do término do acesso, você pode fazê-lo a partir do seu painel de administração. Mudou de ideia? Você pode reativar sua assinatura a qualquer momento.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivar Assinatura" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Cancelamento Confirmado - {{ store_name }}

Olá {{ name|default:'there' }},

Sua {{ plan_name }} subscription foi cancelada.

O Que Acontece em Seguida:
- Você continuará com acesso completo até {{ access_until_date }}.
- Após esse período, os dados do seu loja serão preservados por 30 dias até {{ termination_date }}.

Se quiser exportar seus dados antes do término do acesso, você pode fazê-lo a partir do seu painel de administração. Mudou de ideia? Você pode reativar sua assinatura a qualquer momento.

Reactivar Assinatura: https://spwig.com/account

Precisa de ajuda? Entre em contato com {{ support_email }}