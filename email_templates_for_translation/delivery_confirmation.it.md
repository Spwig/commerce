---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
Ordine consegnato - Ordine #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          Ordine consegnato
        </mj-text>
        <mj-text>
          Il tuo ordine #{{ order_number }} è stato consegnato!
        </mj-text>
        <mj-text>
          Speriamo che ti piaccia il tuo acquisto. Se hai domande o preoccupazioni, non esitare a contattarci.
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Visualizza ordine
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ordine consegnato

Il tuo ordine #{{ order_number }} è stato consegnato!

Speriamo che ti piaccia il tuo acquisto. Se hai domande o preoccupazioni, non esitare a contattarci.

Visualizza ordine: {{ order_url }}

