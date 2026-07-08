---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
Stornierung bestätigt - {{ store_name }}

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
          Stornierung bestätigt
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
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Ihre <strong>{{ plan_name }}</strong> Abonnement wurde storniert.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Was als Nächstes passiert
        </mj-text>
        <mj-text font-size="14px">
          Sie haben weiterhin vollen Zugriff bis <strong>{{ access_until_date }}</strong>.
        </mj-text>
        <mj-text font-size="14px">
          Danach wird Ihre Store-Daten für 30 Tage bis <strong>{{ termination_date }}</strong> gespeichert.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Wenn Sie Ihre Daten vor Ablauf des Zugriffs exportieren möchten, können Sie dies in Ihrem Admin-Panel tun. Geändert? Sie können Ihr Abonnement jederzeit wieder aktivieren.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Abonnement wieder aktivieren" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Stornierung bestätigt - {{ store_name }}

Hi {{ name|default:'there' }},

Ihr {{ plan_name }} Abonnement wurde storniert.

Was als Nächstes passiert:
- Sie haben weiterhin vollen Zugriff bis {{ access_until_date }}.
- Danach wird Ihre Store-Daten für 30 Tage bis {{ termination_date }} gespeichert.

Wenn Sie Ihre Daten vor Ablauf des Zugriffs exportieren möchten, können Sie dies in Ihrem Admin-Panel tun. Geändert? Sie können Ihr Abonnement jederzeit wieder aktivieren.

Abonnement wieder aktivieren: https://spwig.com/account

Benötigen Sie Hilfe? Kontaktieren Sie {{ support_email }}