---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
Aktion erforderlich - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Suspension Warning
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Action required for {{ store_name }}
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
          Your payment for <strong>{{ plan_name }}</strong> is overdue. If not resolved by <strong>{{ grace_end_date }}</strong>, your store will be placed in read-only mode.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Was eine Sperrung bedeutet
        </mj-text>
        <mj-text font-size="14px">
          Wenn Ihr Geschäft gesperrt ist, bleibt es für Besucher sichtbar, aber Sie können keine Änderungen vornehmen. Neue Bestellungen werden pausiert, bis der ausstehende Betrag beglichen ist.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          Bitte aktualisieren Sie Ihre Zahlungsmethode, um Störungen in Ihrem Geschäft zu vermeiden.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Update Payment Method" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Sperrungswarnung - {{ store_name }}

Hi {{ name|default:'there' }},

Ihre Zahlung für {{ plan_name }} ist überfällig. Wenn dies bis {{ grace_end_date }} nicht behoben wird, wird Ihr Geschäft in den Lesemodus versetzt.

Was eine Sperrung bedeutet:
Wenn Ihr Geschäft gesperrt ist, bleibt es für Besucher sichtbar, aber Sie können keine Änderungen vornehmen. Neue Bestellungen werden pausiert, bis der ausstehende Betrag beglichen ist.

Bitte aktualisieren Sie Ihre Zahlungsmethode, um Störungen in Ihrem Geschäft zu vermeiden.

Zahlungsmethode aktualisieren: https://spwig.com/account

Benötigen Sie Hilfe? Kontaktieren Sie {{ support_email }}