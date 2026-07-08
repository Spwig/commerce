---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
Benvenuto nuovamente! {{ store_name }} è attiva di nuovo

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Benvenuto nuovamente!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} è attiva di nuovo
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Ciao,
        </mj-text>
        <mj-text>
          Buone notizie! Il tuo negozio <strong>{{ store_name }}</strong> è stato riacceso. La tua sottoscrizione <strong>{{ plan_name }}</strong> è ora attiva e il tuo negozio sta tornando online.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Dettagli del riacquisto
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Piano: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Pagamento effettuato: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Data successivo addebito: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          Il tuo negozio sta tornando online ora. Potrebbe richiedere alcuni minuti per ripristinare completamente tutto. Una volta online, il tuo negozio sarà accessibile a {{ store_url }}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Vai al tuo negozio" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Benvenuto nuovamente! {{ store_name }} è attiva di nuovo

Ciao,

Buone notizie! Il tuo negozio {{ store_name }} è stato riacceso. La tua sottoscrizione {{ plan_name }} è ora attiva e il tuo negozio sta tornando online.

Dettagli del riacquisto:
- Piano: {{ plan_name }}
- Pagamento effettuato: {{ currency }}{{ amount }}
- Data successivo addebito: {{ next_billing_date }}

Il tuo negozio sta tornando online ora. Potrebbe richiedere alcuni minuti per ripristinare completamente tutto. Una volta online, il tuo negozio sarà accessibile a {{ store_url }}.

Vai al tuo negozio: {{ admin_url }}

Hai bisogno di aiuto? Contatta {{ support_email }}