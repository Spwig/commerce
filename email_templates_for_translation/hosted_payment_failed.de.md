---
template_type: hosted_payment_failed
category: License
---

# Email Template: hosted_payment_failed

## Subject
Zahlung fehlgeschlagen - {{ store_name }}

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
          Zahlungsproblem
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Aktion erforderlich für {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Wir konnten Ihre Zahlung für <strong>{{ plan_name }}</strong> nicht verarbeiten.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Zahlungsdetails
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Betrag: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          {{ retry_info }}. Um Unterbrechungen des Dienstes zu vermeiden, aktualisieren Sie bitte Ihre Zahlungsmethode.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Zahlungsmethode aktualisieren" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Zahlungsproblem - {{ store_name }}

Hi {{ name|default:'there' }},

Wir konnten Ihre Zahlung für {{ plan_name }} nicht verarbeiten.

Zahlungsdetails:
- Betrag: {{ currency }}{{ amount }}
- Plan: {{ plan_name }}

{{ retry_info }}. Um Unterbrechungen des Dienstes zu vermeiden, aktualisieren Sie bitte Ihre Zahlungsmethode.

Zahlungsmethode aktualisieren: https://spwig.com/account

Benötigen Sie Hilfe? Kontaktieren Sie {{ support_email }}