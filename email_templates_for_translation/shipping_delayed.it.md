---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
Aggiornamento sulla tua ordinazione #{{ order_number }} - Ritardo di consegna

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Aggiornamento sulla tua ordinazione
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Volevamo informarti di un ritardo per la tua ordinazione. Ci scusiamo per l'inconveniente e apprezziamo la tua pazienza.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli dell'Ordine:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Numero Ordine:</strong> {{ order_number }}<br/>
              <strong>Data di consegna originale:</strong> {{ original_delivery_date }}<br/>
              <strong>Nuova data di consegna:</strong> {{ new_delivery_date }}<br/>
              <strong>Numero di tracciamento:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Motivo del ritardo:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Traccia la tua ordinazione
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Stiamo lavorando duramente per consegnarti l'ordinazione il prima possibile. Riceverai un altro aggiornamento quando il tuo pacco sarà in transito.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Domande? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contatta il nostro team di assistenza clienti</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Aggiornamento sulla tua ordinazione #{{ order_number }}

Ciao {{ customer_name }},

Volevamo informarti di un ritardo per la tua ordinazione. Ci scusiamo per l'inconveniente e apprezziamo la tua pazienza.

DETTAGLI DELL'ORDINE:
- Numero Ordine: {{ order_number }}
- Data di consegna originale: {{ original_delivery_date }}
- Nuova data di consegna: {{ new_delivery_date }}
- Numero di tracciamento: {{ tracking_number }}

MOTIVO DEL RITARDO:
{{ delay_reason }}

Traccia la tua ordinazione: {{ tracking_url }}

Stiamo lavorando duramente per consegnarti l'ordinazione il prima possibile. Riceverai un altro aggiornamento quando il tuo pacco sarà in transito.

Domande? Contatta il nostro team di assistenza clienti: {{ support_url }}

---
Questo aggiornamento è per l'ordinazione #{{ order_number }} a {{ shop_name }}.