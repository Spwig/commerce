---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
Iscrizione confermata - {{ store_name }}

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
          Iscrizione confermata!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Benvenuto in Spwig
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
          Grazie per l'iscrizione! Il tuo piano <strong>{{ plan_name }}</strong> per <strong>{{ store_name }}</strong> è stato confermato.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Dettagli del piano
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Piano: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Intervallo di fatturazione: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Importo: {{ currency }}{{ amount }}{% if intro_period %} (tasso introduttivo){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          Il tuo tasso introduttivo è applicabile per {{ intro_period }}. Dopo di che, il tuo piano rinnoverà a {{ currency }}{{ full_amount }}/{{ billing_interval }}.
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          Il tuo negozio sta per essere configurato e riceverai un altro email quando sarà pronto.
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          Prossima data di fatturazione: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Iscrizione confermata!

Ciao {{ name|default:'there' }},

Grazie per l'iscrizione! Il tuo piano {{ plan_name }} per {{ store_name }} è stato confermato.

Dettagli del piano:
- Piano: {{ plan_name }}
- Intervallo di fatturazione: {{ billing_interval }}
- Importo: {{ currency }}{{ amount }}{% if intro_period %} (tasso introduttivo){% endif %}
{% if intro_period %}
Questo è il tuo tasso introduttivo per {{ intro_period }}. Dopo di che, il tuo piano rinnoverà a {{ currency }}{{ full_amount }}/{{ billing_interval }}.
{% endif %}
Il tuo negozio sta per essere configurato e riceverai un altro email quando sarà pronto.

Prossima data di fatturazione: {{ next_billing_date }}

Hai bisogno di aiuto? Contatta {{ support_email }}