---
template_type: hosted_terminated
category: License
---

# Email Template: hosted_terminated

## Subject
Geschäft entfernt - {{ store_name }}

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
    <mj-section background-color="#374151" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Geschäft entfernt
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
          Ihr Geschäft <strong>{{ store_name }}</strong> wurde dauerhaft entfernt.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Data Backup Info -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Datensicherung
        </mj-text>
        <mj-text font-size="14px">
          Eine Sicherung Ihrer Daten wird 90 Tage lang nach Anfrage bereitgestellt. Kontaktieren Sie <strong>support@spwig.com</strong>, wenn Sie eine Datensicherung benötigen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Thank You -->
    <mj-section>
      <mj-column>
        <mj-text>
          Vielen Dank, dass Sie ein Spwig-Kunde sind. Wir hoffen, Sie bald wiederzusehen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Geschäft entfernt - {{ store_name }}

Hi {{ name|default:'there' }},

Ihr Geschäft {{ store_name }} wurde dauerhaft entfernt.

Datensicherung:
Eine Sicherung Ihrer Daten wird 90 Tage lang nach Anfrage bereitgestellt. Kontaktieren Sie support@spwig.com, wenn Sie eine Datensicherung benötigen.

Vielen Dank, dass Sie ein Spwig-Kunde sind. Wir hoffen, Sie bald wiederzusehen.

Benötigen Sie Hilfe? Kontaktieren Sie {{ support_email }}