---
template_type: hosted_payment_failed
category: License
---

# Email Template: hosted_payment_failed

## Subject
Pagamento fallito - {{ store_name }}

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
    <mj-section background-color="#d97706" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Problema di pagamento
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Azione richiesta per {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Ciao {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Non possiamo processare il pagamento per <strong>{{ plan_name }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Dettagli del pagamento
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Importo: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Piano: {{ plan_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          {{ retry_info }}. Per evitare interruzioni del servizio, aggiorna il metodo di pagamento.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Aggiorna il metodo di pagamento" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Problema di pagamento - {{ store_name }}

Ciao {{ name|default:'there' }},

Non possiamo processare il pagamento per {{ plan_name }}.

Dettagli del pagamento:
- Importo: {{ currency }}{{ amount }}
- Piano: {{ plan_name }}

{{ retry_info }}. Per evitare interruzioni del servizio, aggiorna il metodo di pagamento.

Aggiorna il metodo di pagamento: https://spwig.com/account

Hai bisogno di aiuto? Contatta {{ support_email }}