---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
Richiesta di reso ricevuta - Ordine #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          Richiesta di reso ricevuta
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
          Ordine #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Abbiamo ricevuto la tua richiesta di reso per l'ordine <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli del reso:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Motivo:</strong> {{ return_reason }}<br/>
              <strong>Articoli:</strong> {{ items_count }} articolo(i)<br/>
              <strong>Stato:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cosa succede adesso?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Il nostro team esaminerà la tua richiesta di reso entro 24-48 ore<br/>
          2. Una volta approvata, ti invieremo un'etichetta per il reso via email<br/>
          3. Confeziona gli articoli in modo sicuro e attacca l'etichetta del reso<br/>
          4. Porta il pacco al punto di spedizione più vicino<br/>
          5. Il rimborso verrà processato una volta ricevuti e ispezionati gli articoli
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Se hai domande, non esitare a contattarci.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
RICHIESTA DI RESO RICEVUTA
Ordine #{{ order_number }}

Ciao {{ customer_name }},

Abbiamo ricevuto la tua richiesta di reso per l'ordine #{{ order_number }}.

DETTAGLI DEL RESO:
- Motivo: {{ return_reason }}
- Articoli: {{ items_count }} articolo(i)
- Stato: {{ return_status }}

COSA SUCCEDE AD OGGI?
1. Il nostro team esaminerà la tua richiesta di reso entro 24-48 ore
2. Una volta approvata, ti invieremo un'etichetta per il reso via email
3. Confeziona gli articoli in modo sicuro e attacca l'etichetta del reso
4. Porta il pacco al punto di spedizione più vicino
5. Il rimborso verrà processato una volta ricevuti e ispezionati gli articoli

Se hai domande, non esitare a contattarci.