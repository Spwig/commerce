---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
Geschäft gesperrt - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Account gesperrt
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
          Ihr Geschäft <strong>{{ store_name }}</strong> wurde aufgrund von unbezahlten Rechnungen gesperrt.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Was dies bedeutet
        </mj-text>
        <mj-text font-size="14px">
          Ihr Geschäft ist nun im Nur-Lesemodus – Kunden können stöbern, aber Bestellungen sind deaktiviert. Ihre Daten sind sicher und werden 30 Tage lang gespeichert.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          Um den vollen Zugriff wiederherzustellen, aktualisieren Sie bitte Ihre Zahlungsmethode und begleichen Sie den ausstehenden Betrag.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Geschäft reaktivieren" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Geschäft gesperrt - {{ store_name }}

Hi {{ name|default:'there' }},

Ihr Geschäft {{ store_name }} wurde aufgrund von unbezahlten Rechnungen gesperrt.

Was dies bedeutet:
Ihr Geschäft ist nun im Nur-Lesemodus – Kunden können stöbern, aber Bestellungen sind deaktiviert. Ihre Daten sind sicher und werden 30 Tage lang gespeichert.

Um den vollen Zugriff wiederherzustellen, aktualisieren Sie bitte Ihre Zahlungsmethode und begleichen Sie den ausstehenden Betrag.

Geschäft reaktivieren: https://spwig.com/account

Benötigen Sie Hilfe? Kontaktieren Sie {{ support_email }}