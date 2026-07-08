---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ Alerta di Discrepanza in Contanti: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Discrepanza in Contanti Rilevata
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Alert di Variazione in Contanti
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          E' stata rilevata una discrepanza in contanti di {{ discrepancy_amount }} durante la chiusura del turno su {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli della Discrepanza:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Cassiere:</strong> {{ cashier_name }}<br/>
              <strong>Data del turno:</strong> {{ shift_date }}<br/>
              <strong>Durata del turno:</strong> {{ shift_duration }}<br/>
              <strong>Rilevata:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Conteggio del Denaro:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>Denaro Previsto:</strong> {{ expected_cash }}<br/>
              <strong>Denaro Contato:</strong> {{ counted_cash }}<br/>
              <strong>Discrepanza:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Denaro Iniziale:</strong> {{ opening_cash }}<br/>
              <strong>Vendite in Contanti:</strong> {{ cash_sales }}<br/>
              <strong>Rimborsi in Contanti:</strong> {{ cash_refunds }}<br/>
              <strong>Denaro Pagato:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nota del Cassiere:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              "{{ cashier_note }}"
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Azioni Consigliate:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Rivedi la cronologia delle transazioni per errori<br/>
          2. Controlla i pagamenti in contanti non registrati<br/>
          3. Verifica che il conteggio del denaro sia stato preciso<br/>
          4. Documenta la discrepanza nelle note del turno<br/>
          5. Segui con il cassiere se necessario
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza Rapporto del Turno
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Rivedi le Transazioni
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ DISCREPANZA IN CONTANTI RILEVATA

Alert di Variazione in Contanti

E' stata rilevata una discrepanza in contanti di {{ discrepancy_amount }} durante la chiusura del turno su {{ terminal_name }}.

DETTAGLI DELLA DISCREPANZA:
- Terminal: {{ terminal_name }}
- Cassiere: {{ cashier_name }}
- Data del turno: {{ shift_date }}
- Durata del turno: {{ shift_duration }}
- Rilevata: {{ detected_at }}

CONTENUTO DEL DENARO:
- Denaro Previsto: {{ expected_cash }}
- Denaro Contato: {{ counted_cash }}
- Discrepanza: {{ discrepancy_amount }}

DETTAGLI:
- Denaro Iniziale: {{ opening_cash }}
- Vendite in Contanti: {{ cash_sales }}
- Rimborsi in Contanti: {{ cash_refunds }}
- Denaro Pagato: {{ cash_paid_out }}

{% if cashier_note %}
NOTA DEL CASSIERE:
"{{ cashier_note }}"
{% endif %}

AZIONI CONSIGLIATE:
1. Rivedi la cronologia delle transazioni per errori
2. Controlla i pagamenti in contanti non registrati
3. Verifica che il conteggio del denaro sia stato preciso
4. Documenta la discrepanza nelle note del turno
5. Segui con il cassiere se necessario

Visualizza Rapporto del Turno: {{ shift_report_url }}
Rivedi le Transazioni: {{ transaction_history_url }}