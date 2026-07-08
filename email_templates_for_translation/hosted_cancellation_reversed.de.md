---
template_type: hosted_cancellation_reversed
category: License
---

# Email Template: hosted_cancellation_reversed

## Subject
Stornierung rückgängig gemacht - {{ store_name }}

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
          Stornierung rückgängig gemacht
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
          Ihre Stornierungsanfrage für <strong>{{ store_name }}</strong> wurde rückgängig gemacht. Ihre <strong>{{ plan_name }}</strong>-Abonnement wird weiterhin normal fortgesetzt – keine Aktion ist von Ihrer Seite erforderlich.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Subscription Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Abonnement-Details
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Nächster Zahlungstermin: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Ihr Store funktioniert weiterhin normal. Die Abrechnung wird am oben genannten Datum wieder aufgenommen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% if admin_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}
    {% endif %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Stornierung rückgängig gemacht - {{ store_name }}

Hi there,

Ihre Stornierungsanfrage für {{ store_name }} wurde rückgängig gemacht. Ihr {{ plan_name }}-Abonnement wird weiterhin normal fortgesetzt — keine Aktion ist von Ihrer Seite erforderlich.

Abonnement-Details:
- Plan: {{ plan_name }}
- Nächster Zahlungstermin: {{ next_billing_date }}

Ihr Store funktioniert weiterhin normal. Die Abrechnung wird am oben genannten Datum wieder aufgenommen.

{% if admin_url %}Go to Your Store: {{ admin_url }}

{% endif %}Need help? Contact {{ support_email }}