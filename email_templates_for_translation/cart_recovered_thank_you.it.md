---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
Grazie per l'ordine #{{ order_number }}! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Grazie per il tuo ordine!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Siamo felici che tu abbia completato l'acquisto! Il tuo ordine è stato confermato e lo stiamo preparando per la spedizione.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Riepilogo Ordine
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Numero Ordine:</strong> {{ order_number }}<br/>
              <strong>Data Ordine:</strong> {{ order_date }}<br/>
              <strong>Totale:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Traccia il tuo ordine
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cosa succede adesso?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Prepareremo il tuo ordine (di solito entro 1-2 giorni lavorativi)<br/>
          2. Riceverai una conferma di spedizione con informazioni di tracciamento<br/>
          3. Il tuo ordine verrà consegnato a: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Lo sapevi?</strong><br/>
              Puoi tracciare il tuo ordine in qualsiasi momento nel tuo pannello di controllo dell'account.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Domande? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contatta il nostro team di supporto</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 GRAZIE PER IL TUO ORDINE!

Ciao {{ customer_name }},

Siamo felici che tu abbia completato l'acquisto! Il tuo ordine è stato confermato e lo stiamo preparando per la spedizione.

RIEPILOGO ORDINE:
- Numero Ordine: {{ order_number }}
- Data Ordine: {{ order_date }}
- Totale: {{ order_total }}

Traccia il tuo ordine: {{ order_tracking_url }}

COSA SUCCEDE AD ORA?
1. Prepareremo il tuo ordine (di solito entro 1-2 giorni lavorativi)
2. Riceverai una conferma di spedizione con informazioni di tracciamento
3. Il tuo ordine verrà consegnato a: {{ shipping_address }}

💡 LO SAPEVI?
Puoi tracciare il tuo ordine in qualsiasi momento nel tuo pannello di controllo dell'account.

Domande? Contatta il nostro team di supporto: {{ support_url }}

---
Ordine #{{ order_number }} a {{ shop_name }}