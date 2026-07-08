---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ Attività di Commissione Anomala Rilevata - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Alert Commissione Elevata
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Attività Anomala Rilevata
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          È stata guadagnata una commissione insolitamente elevata dall'affiliato {{ affiliate_name }}. Questo richiede una revisione per la prevenzione dello frode.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli dell'Alert:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Affiliato:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>Importo della Commissione:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>Valore dell'Ordine:</strong> {{ order_value }}<br/>
              <strong>ID Ordine:</strong> {{ order_number }}<br/>
              <strong>Rilevato:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Perché Questo è Stato Segnalato:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Azioni Consigliate:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Verificare i dettagli dell'ordine per legittimità<br/>
          • Controllare la cronologia dei riferimenti dell'affiliato<br/>
          • Verificare che il cliente non sia affiliato al riferente<br/>
          • Approvare o rifiutare la commissione nel pannello di amministrazione
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rivedi la Commissione
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Visualizza Dettagli Affiliato
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Questa commissione è in attesa di revisione e non verrà pagata fino all'approvazione.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ALERT COMMISSIONE ELEVATA

Attività Anomala Rilevata

È stata guadagnata una commissione insolitamente elevata dall'affiliato {{ affiliate_name }}. Questo richiede una revisione per la prevenzione dello frode.

DETTAGLI DELL'ALERT:
- Affiliato: {{ affiliate_name }} ({{ affiliate_id }})
- Importo della Commissione: {{ commission_amount }}
- Valore dell'Ordine: {{ order_value }}
- ID Ordine: {{ order_number }}
- Rilevato: {{ detected_at }}

PERCHÉ QUESTO È STATO SEGNALATO:
{{ flag_reason }}

AZIONI CONSIGLIATE:
• Verificare i dettagli dell'ordine per legittimità
• Controllare la cronologia dei riferimenti dell'affiliato
• Verificare che il cliente non sia affiliato al riferente
• Approvare o rifiutare la commissione nel pannello di amministrazione

Rivedi la commissione: {{ review_commission_url }}
Visualizza dettagli affiliato: {{ affiliate_details_url }}

Questa commissione è in attesa di revisione e non verrà pagata fino all'approvazione.