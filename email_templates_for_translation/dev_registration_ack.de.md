---
template_type: dev_registration_ack
category: Developer Portal
---

# Email Template: dev_registration_ack

## Subject
Wir haben Ihre Entwickleranmeldung erhalten, {{ developer_name }}

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
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Anmeldung erhalten!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Wir prüfen Ihre Entwickleranmeldung
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Hallo {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          Vielen Dank, dass Sie sich für das Spwig Developer Program beworben haben. Wir haben Ihre Bewerbung erhalten und unser Team wird sie bald prüfen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          Was kommt als nächstes?
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> Unser Team prüft Ihre Bewerbung (typischerweise 2-3 Werktagen)
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> Sie erhalten eine E-Mail mit unserer Entscheidung
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>3.</strong> Nach Genehmigung erhalten Sie vollen Zugriff auf das Entwickler-Dashboard
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ portal_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Entwickler-Portal ansehen
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Spwig Developer Portal</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Fragen? Kontaktieren Sie den Entwickler-Unterstützung
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Hallo {{ developer_name }},

Vielen Dank, dass Sie sich für das Spwig Developer Program beworben haben. Wir haben Ihre Bewerbung erhalten und unser Team wird sie bald prüfen.

Was kommt als nächstes?
1. Unser Team prüft Ihre Bewerbung (typischerweise 2-3 Werktagen)
2. Sie erhalten eine E-Mail mit unserer Entscheidung
3. Nach Genehmigung erhalten Sie vollen Zugriff auf das Entwickler-Dashboard

Entwickler-Portal ansehen: {{ portal_url }}

---
Spwig Developer Portal