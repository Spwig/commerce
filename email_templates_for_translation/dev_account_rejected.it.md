---
template_type: dev_account_rejected
category: Developer Portal
---

# Email Template: dev_account_rejected

## Subject
Aggiornamento sulla tua candidatura per lo Spwig Developer Program

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
          Aggiornamento sulla candidatura
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Aggiornamento sulla tua candidatura per lo Spwig Developer Program
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Ciao {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          Grazie per il tuo interesse al programma per sviluppatori Spwig. Dopo una revisione attenta, non possiamo approvare la tua candidatura in questo momento.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reason Section (if provided) -->
    {% if rejection_reason %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          Motivo:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.error|default:'#ef4444' }}">
          {{ rejection_reason }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Support Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Se hai domande o ritieni che questo sia stato fatto per errore, contattaci a <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }}; text-decoration: none;">{{ support_email }}</a>.
        </mj-text>
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
          Domande? Contatta il supporto per sviluppatori
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ciao {{ developer_name }},

Grazie per il tuo interesse al programma per sviluppatori Spwig. Dopo una revisione attenta, non possiamo approvare la tua candidatura in questo momento.

{% if rejection_reason %}Motivo: {{ rejection_reason }}{% endif %}

Se hai domande o ritieni che questo sia stato fatto per errore, contattaci a {{ support_email }}.

---
Spwig Developer Portal