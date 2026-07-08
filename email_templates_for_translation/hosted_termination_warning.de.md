---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
Wichtig: Datenlöschung in 7 Tagen - {{ store_name }}

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
          Datenlöschungshinweis
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
          Ihr Geschäft <strong>{{ store_name }}</strong> und alle damit verbundenen Daten werden am <strong>{{ termination_date }}</strong> dauerhaft gelöscht. Diese Aktion kann nicht rückgängig gemacht werden.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Was Sie tun können
        </mj-text>
        <mj-text font-size="14px">
          Wenn Sie Ihre Daten behalten möchten, exportieren Sie sie bitte vor diesem Datum oder reaktivieren Sie Ihr Abonnement, um die Löschung zu verhindern.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Abonnement reaktivieren" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Datenlöschungshinweis - {{ store_name }}

Hi {{ name|default:'there' }},

Ihr Geschäft {{ store_name }} und alle damit verbundenen Daten werden am {{ termination_date }} dauerhaft gelöscht. Diese Aktion kann nicht rückgängig gemacht werden.

Was Sie tun können:
Wenn Sie Ihre Daten behalten möchten, exportieren Sie sie bitte vor diesem Datum oder reaktivieren Sie Ihr Abonnement, um die Löschung zu verhindern.

Abonnement reaktivieren: https://spwig.com/account

Benötigen Sie Hilfe? Kontaktieren Sie {{ support_email }}