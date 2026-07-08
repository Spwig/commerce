---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
Ihr Spwig-Lizenzschlüssel - Bestellung #{{ order_number }}

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
          Vielen Dank für Ihren Kauf!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Bestellung #{{ order_number }}
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
          Ihr Kauf von <strong>{{ product_name }}</strong> ist abgeschlossen. Unten finden Sie Ihren Lizenzschlüssel und Setup-Token, um zu beginnen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Bestellübersicht
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Produkt: {{ product_name }}{% if includes_pos %} (beinhaltet POS){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Betrag: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Bestellnummer: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          IHR LIZENZSCHLÜsSEL
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Speichern Sie diesen Schlüssel - Sie benötigen ihn zur Neuanmeldung
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          IHR SETUP-TOKEN
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Verwenden Sie diesen Token während der Installation, um Ihren Store zu aktivieren
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Loslegen
        </mj-text>
        <mj-text font-size="14px">
          1. Folgen Sie unserem Setup-Leitfaden, um Spwig auf Ihrem Server zu installieren
        </mj-text>
        <mj-text font-size="14px">
          2. Geben Sie Ihren Setup-Token ein, wenn Sie aufgefordert werden
        </mj-text>
        <mj-text font-size="14px">
          3. Ihr Store wird automatisch aktiviert
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Erstellen Sie Ihr Konto
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          Legen Sie ein Passwort an, um Ihre Lizenzen zu verwalten, Downloads zu erhalten und Updates zu erhalten.
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          Wichtig:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Bewahren Sie diese E-Mail sicher auf - sie enthält Ihren Lizenzschlüssel und Setup-Token für spätere Verwendung. Teilen Sie diese Zugangsdaten nicht mit anderen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Vielen Dank für Ihren Kauf!

Bestellung #{{ order_number }}

Hallo {{ customer_name }},

Ihr Kauf von {{ product_name }} ist abgeschlossen. Unten finden Sie Ihren Lizenzschlüssel und Setup-Token, um zu beginnen.

Bestellübersicht:
- Produkt: {{ product_name }}{% if includes_pos %} (beinhaltet POS){% endif %}
- Betrag: {{ price }}
- Bestellnummer: {{ order_number }}

IHR LIZENZSCHLÜsSEL:
{{ license_key }}
Speichern Sie diesen Schlüssel - Sie benötigen ihn zur Neuanmeldung.

IHR SETUP-TOKEN:
{{ setup_token }}
Verwenden Sie diesen Token während der Installation, um Ihren Store zu aktivieren.

Loslegen:
1. Folgen Sie unserem Setup-Leitfaden, um Spwig auf Ihrem Server zu installieren
2. Geben Sie Ihren Setup-Token ein, wenn Sie aufgefordert werden
3. Ihr Store wird automatisch aktiviert

View Setup Guide: {{ setup_url }}
{% if activation_url %}
Erstellen Sie Ihr Konto:
Legen Sie ein Passwort an, um Ihre Lizenzen zu verwalten, Downloads zu erhalten und Updates zu erhalten.
{{ activation_url }}
{% endif %}
Wichtig:
Bewahren Sie diese E-Mail sicher auf - sie enthält Ihren Lizenzschlüssel und Setup-Token für spätere Verwendung. Teilen Sie diese Zugangsdaten nicht mit anderen.

Need help? Contact {{ support_email }}