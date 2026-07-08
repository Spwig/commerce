---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
Ihr Software-Lizenzschlüssel - Bestellung #{{ order_number }}

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
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Ihr Lizenzschlüssel ist bereit
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hallo {{ customer_name }},
        </mj-text>
        <mj-text>
          Vielen Dank für den Kauf von {{ product_name }}! Hier ist Ihr Lizenzschlüssel zur Aktivierung.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          IHR LIZENZSCHLÜSSEL
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Klicken Sie, um ihn zu kopieren, oder schreiben Sie ihn sorgfältig auf
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          Lizenzdetails:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Produkt: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Version: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Lizenztyp: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Max. Aktivierungen: {{ max_activations }} Gerät(e)
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Gültigkeit: Lifetime License
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Gültig bis: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Wie aktiviere ich:
        </mj-text>
        <mj-text font-size="14px">
          1. Laden Sie die Software herunter und installieren Sie sie
        </mj-text>
        <mj-text font-size="14px">
          2. Öffnen Sie die Anwendung
        </mj-text>
        <mj-text font-size="14px">
          3. Geben Sie Ihren Lizenzschlüssel ein, wenn Sie aufgefordert werden
        </mj-text>
        <mj-text font-size="14px">
          4. Klicken Sie auf "Aktivieren", um den Vorgang abzuschließen
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Software herunterladen
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ Wichtig:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Bewahren Sie diese E-Mail sicher auf – Sie benötigen den Lizenzschlüssel für eine Neuanmeldung
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Teilen Sie Ihren Lizenzschlüssel nicht mit anderen
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Sie können Geräte über Ihr Konto-Dashboard deaktivieren
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Benötigen Sie Hilfe bei der Aktivierung? Kontaktieren Sie {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ihr Lizenzschlüssel ist bereit

Hallo {{ customer_name }},

Vielen Dank für den Kauf von {{ product_name }}! Hier ist Ihr Lizenzschlüssel zur Aktivierung.

IHR LIZENZSCHLÜSSEL:
{{ license_key }}

Lizenzdetails:
• Produkt: {{ product_name }}
• Version: {{ product_version }}
• Lizenztyp: {{ license_type }}
• Max. Aktivierungen: {{ max_activations }} Gerät(e)
{% if is_lifetime %}• Gültigkeit: Lifetime License{% else %}• Gültig bis: {{ expiration_date }}{% endif %}

Wie aktiviere ich:
1. Laden Sie die Software herunter und installieren Sie sie
2. Öffnen Sie die Anwendung
3. Geben Sie Ihren Lizenzschlüssel ein, wenn Sie aufgefordert werden
4. Klicken Sie auf "Aktivieren", um den Vorgang abzuschließen

{% if download_url %}Software herunterladen: {{ download_url }}

{% endif %}Wichtig:
• Bewahren Sie diese E-Mail sicher auf – Sie benötigen den Lizenzschlüssel für eine Neuanmeldung
• Teilen Sie Ihren Lizenzschlüssel nicht mit anderen
• Sie können Geräte über Ihr Konto-Dashboard deaktivieren

Benötigen Sie Hilfe bei der Aktivierung? Kontaktieren Sie {{ support_email }}