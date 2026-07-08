---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
Abonnement bestätigt - {{ store_name }}

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
          Abonnement bestätigt!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Willkommen bei Spwig
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
          Vielen Dank für Ihr Abonnement! Ihr <strong>{{ plan_name }}</strong> Plan für <strong>{{ store_name }}</strong> wurde bestätigt.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Plan Details
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Billing Interval: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Amount: {{ currency }}{{ amount }}{% if intro_period %} (introductory rate){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          Ihr Einführungspreis gilt für {{ intro_period }}. Danach wird Ihr Plan zu {{ currency }}{{ full_amount }}/{{ billing_interval }} erneuert.
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          Ihr Geschäft wird jetzt eingerichtet und Sie erhalten eine weitere E-Mail, sobald es bereit ist.
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          Nächster Zahlungstermin: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Abonnement bestätigt!

Hi {{ name|default:'there' }},

Vielen Dank für Ihr Abonnement! Ihr {{ plan_name }} Plan für {{ store_name }} wurde bestätigt.

Plan Details:
- Plan: {{ plan_name }}
- Billing Interval: {{ billing_interval }}
- Amount: {{ currency }}{{ amount }}{% if intro_period %} (introductory rate){% endif %}
{% if intro_period %}
Dies ist Ihr Einführungspreis für {{ intro_period }}. Danach wird Ihr Plan zu {{ currency }}{{ full_amount }}/{{ billing_interval }} erneuert.
{% endif %}
Ihr Geschäft wird jetzt eingerichtet und Sie erhalten eine weitere E-Mail, sobald es bereit ist.

Nächster Zahlungstermin: {{ next_billing_date }}

Benötigen Sie Hilfe? Kontaktieren Sie {{ support_email }}