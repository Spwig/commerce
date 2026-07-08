---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ Bargeld-Unterschied: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Bargeld-Unterschied erkannt
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bargeld-Unterschied Meldung
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Ein Bargeld-Unterschied von {{ discrepancy_amount }} wurde beim Schließen des Schichts auf {{ terminal_name }} erkannt.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Unterschied Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Kassierer:</strong> {{ cashier_name }}<br/>
              <strong>Schichtdatum:</strong> {{ shift_date }}<br/>
              <strong>Schichtdauer:</strong> {{ shift_duration }}<br/>
              <strong>Erkannt um:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bargeld-Abrechnung:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>Erwartetes Bargeld:</strong> {{ expected_cash }}<br/>
              <strong>Zugezähltes Bargeld:</strong> {{ counted_cash }}<br/>
              <strong>Unterschied:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Anfangsbestand:</strong> {{ opening_cash }}<br/>
              <strong>Bargeldverkäufe:</strong> {{ cash_sales }}<br/>
              <strong>Bargeld-Rückerstattungen:</strong> {{ cash_refunds }}<br/>
              <strong>Bargeld-Auszahlungen:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kassierer-Notiz:
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
          Empfohlene Aktionen:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Transaktionshistorie auf Fehler überprüfen<br/>
          2. Nicht erfasste Bargeldzahlungen prüfen<br/>
          3. Sicherstellen, dass die Bargeldabrechnung korrekt war<br/>
          4. Unterschied in der Schichtnotiz dokumentieren<br/>
          5. Bei Bedarf mit dem Kassierer folgen
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Schichtbericht ansehen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Transaktionen überprüfen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ BARGELD-UNTERSCHIED ERKENNT

Bargeld-Unterschied Meldung

Ein Bargeld-Unterschied von {{ discrepancy_amount }} wurde beim Schließen des Schichts auf {{ terminal_name }} erkannt.

UNTERSCHIED DETAIL:
- Terminal: {{ terminal_name }}
- Kassierer: {{ cashier_name }}
- Schichtdatum: {{ shift_date }}
- Schichtdauer: {{ shift_duration }}
- Erkannt um: {{ detected_at }}

BARGELD-ABRECHNUNG:
- Erwartetes Bargeld: {{ expected_cash }}
- Zugezähltes Bargeld: {{ counted_cash }}
- Unterschied: {{ discrepancy_amount }}

BREAKDOWN:
- Anfangsbestand: {{ opening_cash }}
- Bargeldverkäufe: {{ cash_sales }}
- Bargeld-Rückerstattungen: {{ cash_refunds }}
- Bargeld-Auszahlungen: {{ cash_paid_out }}

{% if cashier_note %}
BARGELD-UNTERSCHIED NOTIZ:
"{{ cashier_note }}"
{% endif %}

EMPFOHLENE AKTIONEN:
1. Transaktionshistorie auf Fehler überprüfen
2. Nicht erfasste Bargeldzahlungen prüfen
3. Sicherstellen, dass die Bargeldabrechnung korrekt war
4. Unterschied in der Schichtnotiz dokumentieren
5. Bei Bedarf mit dem Kassierer folgen

Schichtbericht ansehen: {{ shift_report_url }}
Transaktionen überprüfen: {{ transaction_history_url }}
