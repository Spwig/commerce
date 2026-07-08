---
template_type: account_welcome
category: Enhanced E-commerce
---

# Email Template: account_welcome

## Subject
Willkommen bei {{ shop_name }}!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Willkommen! 👋
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Wir freuen uns, Sie zu unserem Community-Teil zu zählen
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personalized Greeting -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Hallo {{ customer_name }},
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Ihr Konto wurde erfolgreich erstellt. Sie können jetzt einkaufen!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="20px">
          Mitgliedschaftsvorteile
        </mj-text>

        {% for benefit in shop_benefits %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 0">
          <span style="color: {{ theme.color.success|default:'#10b981' }}; font-size: 18px;">✓</span> {{ benefit }}
        </mj-text>
        {% endfor %}
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-button
          href="{{ browse_products_url }}"
          background-color="{{ theme.color.primary|default:'#2563eb' }}"
          color="{{ theme.color.background|default:'#ffffff' }}"
          font-size="16px"
          font-weight="600"
          border-radius="6px"
          padding="14px 32px"
        >
          Einkaufen starten
        </mj-button>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button
          href="{{ account_url }}"
          background-color="{{ theme.color.text_muted|default:'#6b7280' }}"
          color="{{ theme.color.background|default:'#ffffff' }}"
          font-size="14px"
          border-radius="6px"
          padding="12px 24px"
        >
          Mein Konto verwalten
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Willkommen! 👋

Hallo {{ customer_name }},

Ihr Konto wurde erfolgreich erstellt. Sie können jetzt einkaufen!

Mitgliedschaftsvorteile:
{% for benefit in shop_benefits %}
✓ {{ benefit }}
{% endfor %}

Einkaufen starten: {{ browse_products_url }}
Mein Konto verwalten: {{ account_url }}

Benötigen Sie Hilfe?
E-Mail: {{ support_email }}
Telefon: {{ support_phone }}