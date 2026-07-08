---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 Alerta di riduzione dei prezzi: {{ product_name }} ora è scontato del {{ discount_percentage }}%!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 Alerta di riduzione dei prezzi!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          Risparmia {{ discount_percentage }}% sul tuo prodotto della lista dei desideri
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Grande notizia, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Un prodotto nella tua lista dei desideri è appena diminuito di prezzo! Non perdere questa opportunità di risparmiare.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Era: <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              Ora: {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              Risparmi {{ savings_amount }} ({{ discount_percentage }}% DI SCONTO)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Acquista adesso & risparmia {{ discount_percentage }}%
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>Tempo limitato:</strong> Questo sconto non durerà per sempre. I prezzi potrebbero tornare a salire in qualsiasi momento!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Rimuovi dalla lista dei desideri: <a href="{{ remove_wishlist_url }}">Clicca qui</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 ALERT DI RIDUZIONE DEI PREZZI!
Risparmia {{ discount_percentage }}% sul tuo prodotto della lista dei desideri

Grande notizia, {{ customer_name }}!

Un prodotto nella tua lista dei desideri è appena diminuito di prezzo! Non perdere questa opportunità di risparmiare.

{{ product_name }}
Era: {{ original_price }}
NOW: {{ new_price }}
SAVE {{ savings_amount }} ({{ discount_percentage }}% DI SCONTO)

Acquista adesso & risparmia {{ discount_percentage }}%: {{ product_url }}

⏰ TEMPO LIMITATO: Questo sconto non durerà per sempre. I prezzi potrebbero tornare a salire in qualsiasi momento!

Rimuovi dalla lista dei desideri: {{ remove_wishlist_url }}