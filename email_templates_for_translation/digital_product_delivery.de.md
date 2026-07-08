---
template_type: digital_product_delivery
category: Digital Products
---

# Email Template: digital_product_delivery

## Subject
Ihr digitales Produkt ist bereit - Bestellung #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Ihr digitales Produkt ist bereit!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ customer_name }},
        </mj-text>
        <mj-text>
          Vielen Dank für Ihren Kauf! Ihr digitales Produkt ist jetzt zum Herunterladen bereit.
        </mj-text>
        <mj-text font-weight="bold">
          Bestellung #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Product Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Version: {{ product_version }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Dateigröße: {{ file_size }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Jetzt herunterladen
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Important Information -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          <strong>Wichtige Informationen:</strong>
        </mj-text>
        {% if download_limit %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Sie können dieses Produkt {{ download_limit }} Mal herunterladen
        </mj-text>
        {% endif %}
        {% if expiration_days %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Der Download-Link läuft in {{ expiration_days }} Tagen ab
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Bewahren Sie diese E-Mail für spätere Zwecke auf
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Benötigen Sie Hilfe? Kontaktieren Sie unser Support-Team unter {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ihr digitales Produkt ist bereit!

Hi {{ customer_name }},

Vielen Dank für Ihren Kauf! Ihr digitales Produkt ist jetzt zum Herunterladen bereit.

Bestellung #{{ order_number }}

Produkt: {{ product_name }}
Version: {{ product_version }}
Dateigröße: {{ file_size }}

Laden Sie Ihr Produkt hier herunter:
{{ download_url }}

Wichtige Informationen:
{% if download_limit %}• Sie können dieses Produkt {{ download_limit }} Mal herunterladen
{% endif %}{% if expiration_days %}• Der Download-Link läuft in {{ expiration_days }} Tagen ab
{% endif %}• Bewahren Sie diese E-Mail für spätere Zwecke auf

Benötigen Sie Hilfe? Kontaktieren Sie unser Support-Team unter {{ support_email }}