---
template_type: hosted_interval_changed
category: License
---

# Email Template: hosted_interval_changed

## Subject
Aggiornamento Fatturazione - {{ store_name }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Aggiornamento Fatturazione
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
          Hi there,
        </mj-text>
        <mj-text>
          L'intervallo di fatturazione per il piano <strong>{{ plan_name }}</strong> su <strong>{{ store_name }}</strong> è stato aggiornato.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Billing Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Dettagli Fatturazione
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Piano: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Intervallo di Fatturazione Precedente: {{ old_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Nuovo Intervallo di Fatturazione: {{ new_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Data Prossima Fatturazione: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          La tua sottoscrizione rimane attiva. Puoi gestire le tue preferenze di fatturazione in qualsiasi momento dal tuo account.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Gestisci Sottoscrizione" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Aggiornamento Fatturazione - {{ store_name }}

Hi there,

L'intervallo di fatturazione per il piano {{ plan_name }} su {{ store_name }} è stato aggiornato.

Dettagli Fatturazione:
- Piano: {{ plan_name }}
- Intervallo di Fatturazione Precedente: {{ old_interval }}
- Nuovo Intervallo di Fatturazione: {{ new_interval }}
- Data Prossima Fatturazione: {{ next_billing_date }}

La tua sottoscrizione rimane attiva. Puoi gestire le tue preferenze di fatturazione in qualsiasi momento dal tuo account.

Gestisci Sottoscrizione: https://spwig.com/account

Need help? Contact {{ support_email }}