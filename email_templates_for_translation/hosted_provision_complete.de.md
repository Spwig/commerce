---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
Ihr Geschäft ist bereit - {{ store_name }}

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
          Ihr Geschäft ist online!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} ist für Sie bereit
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hallo {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Große Nachricht! Ihr Spwig-Geschäft <strong>{{ store_name }}</strong> wurde eingerichtet und ist jetzt online. Sie können sofort mit der Einrichtung Ihrer Produkte, Markenidentität und Zahlungsmethoden beginnen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Ihre Geschäftsdetails
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Geschäft-URL: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Admin-Panel: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Region: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Schnellstart
        </mj-text>
        <mj-text font-size="14px">
          1. Melden Sie sich mit der E-Mail-Adresse und dem Passwort, das Sie während des Checkouts festgelegt haben, in Ihrem Admin-Panel an
        </mj-text>
        <mj-text font-size="14px">
          2. Fügen Sie Ihr Geschäftslogo und Ihre Markenidentität unter Design > Theme-Einstellungen hinzu
        </mj-text>
        <mj-text font-size="14px">
          3. Fügen Sie Ihre ersten Produkte unter Katalog > Produkte hinzu
        </mj-text>
        <mj-text font-size="14px">
          4. Richten Sie einen Zahlungsdienstleister unter Einstellungen > Zahlungsdienstleister ein
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Zum Admin-Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Ihr Geschäft ist online!

{{ store_name }} ist für Sie bereit.

Hallo {{ name|default:'there' }},

Große Nachricht! Ihr Spwig-Geschäft {{ store_name }} wurde eingerichtet und ist jetzt online. Sie können sofort mit der Einrichtung Ihrer Produkte, Markenidentität und Zahlungsmethoden beginnen.

Ihre Geschäftsdetails:
- Geschäft-URL: {{ store_url }}
- Admin-Panel: {{ admin_url }}
- Region: {{ region }}

Schnellstart:
1. Melden Sie sich mit der E-Mail-Adresse und dem Passwort, das Sie während des Checkouts festgelegt haben, in Ihrem Admin-Panel an
2. Fügen Sie Ihr Geschäftslogo und Ihre Markenidentität unter Design > Theme-Einstellungen hinzu
3. Fügen Sie Ihre ersten Produkte unter Katalog > Produkte hinzu
4. Richten Sie einen Zahlungsdienstleister unter Einstellungen > Zahlungsdienstleister ein

Zum Admin-Panel: {{ admin_url }}

Brauchen Sie Hilfe? Kontaktieren Sie {{ support_email }}