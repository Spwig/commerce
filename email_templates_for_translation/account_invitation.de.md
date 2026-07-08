---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
Erstellen Sie Ihr Konto bei {{ site_name }}

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
          Sie sind eingeladen!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Erstellen Sie Ihr Konto bei {{ site_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hallo {{ customer_name }},
        </mj-text>
        <mj-text>
          Wir haben bemerkt, dass Sie bisher als Gast bei uns einkaufen. Erstellen Sie ein vollständiges Konto, um Vorteile wie die Verfolgung von Bestellungen, einen schnelleren Checkout und exklusive Angebote zu nutzen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Ihre Einkaufsgeschichte
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Gesamte Bestellungen: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Gesamter Aufwand: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Warum ein Konto erstellen?
        </mj-text>
        <mj-text font-size="14px">
          - Verfolgen Sie Ihre Bestellungen und sehen Sie Ihre Bestellhistorie
        </mj-text>
        <mj-text font-size="14px">
          - Schnellerer Checkout mit gespeicherten Details
        </mj-text>
        <mj-text font-size="14px">
          - Verwalten Sie Ihre Adressen und Präferenzen
        </mj-text>
        <mj-text font-size="14px">
          - Zugang zu exklusiven Angeboten und Promotionen
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Dieser Link ermöglicht es Ihnen, ein Passwort für Ihr Konto festzulegen. Ihre vorhandene Bestellhistorie bleibt erhalten.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Sie sind eingeladen, Ihr Konto zu erstellen!

Hallo {{ customer_name }},

Wir haben bemerkt, dass Sie bisher als Gast bei uns einkaufen. Erstellen Sie ein vollständiges Konto, um Vorteile wie die Verfolgung von Bestellungen, einen schnelleren Checkout und exklusive Angebote zu nutzen.

Ihre Einkaufsgeschichte:
- Gesamte Bestellungen: {{ total_orders }}
- Gesamter Aufwand: {{ total_spent }}

Warum ein Konto erstellen?
- Verfolgen Sie Ihre Bestellungen und sehen Sie Ihre Bestellhistorie
- Schnellerer Checkout mit gespeicherten Details
- Verwalten Sie Ihre Adressen und Präferenzen
- Zugang zu exklusiven Angeboten und Promotionen

Erstellen Sie Ihr Konto: {{ activation_url }}

Dieser Link ermöglicht es Ihnen, ein Passwort für Ihr Konto festzulegen. Ihre vorhandene Bestellhistorie bleibt erhalten.

Benötigen Sie Hilfe? Kontaktieren Sie {{ support_email }}