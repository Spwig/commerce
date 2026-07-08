---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 Schichtbericht: {{ terminal_name }} - {{ shift_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Schicht geschlossen
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Schichtzusammenfassungsbericht
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Schicht wurde auf {{ terminal_name }} von {{ cashier_name }} geschlossen.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Schichtdetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Kassierer:</strong> {{ cashier_name }}<br/>
              <strong>Beginn:</strong> {{ shift_started }}<br/>
              <strong>Ende:</strong> {{ shift_ended }}<br/>
              <strong>Dauer:</strong> {{ shift_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Verkaufsbericht:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Gesamte Verkäufe:</strong> {{ total_sales }}<br/>
              <strong>Transaktionen:</strong> {{ transaction_count }}<br/>
              <strong>Verkaufte Artikel:</strong> {{ items_sold }}<br/>
              <strong>Durchschnittlicher Verkauf:</strong> {{ average_sale }}<br/>
              <strong>Erhobene Steuern:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Zahlungsaufschlüsselung:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }} ({{ payment.count }} Transaktionen)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kassenabrechnung:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Anfangskasse:</strong> {{ opening_cash }}<br/>
              <strong>Kassengeschäfte:</strong> {{ cash_sales }}<br/>
              <strong>Erwartete Kasse:</strong> {{ expected_cash }}<br/>
              <strong>Zählte Kasse:</strong> {{ counted_cash }}<br/>
              <strong>Unterschied:</strong> <span style="color: {{ cash_difference_color }};">{{ cash_difference }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        {% if discrepancy_amount != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Kassenunterschied: {{ discrepancy_amount }}
            </mj-text>
            {% if discrepancy_note %}
            <mj-text font-size="14px" color="#92400e">
              Hinweis: {{ discrepancy_note }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Bericht vollständig anzeigen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 SCHICHT GESCHLOSSEN

Schichtzusammenfassungsbericht

Schicht wurde auf {{ terminal_name }} von {{ cashier_name }} geschlossen.

SCHICHTDETAILS:
- Terminal: {{ terminal_name }}
- Kassierer: {{ cashier_name }}
- Begonnen: {{ shift_started }}
- Beendet: {{ shift_ended }}
- Dauer: {{ shift_duration }}

VERKAUFSZUSAMMENFASSUNG:
- Gesamte Verkäufe: {{ total_sales }}
- Transaktionen: {{ transaction_count }}
- Verkaufte Artikel: {{ items_sold }}
- Durchschnittlicher Verkauf: {{ average_sale }}
- Erhobene Steuern: {{ tax_collected }}

ZAHLUNGAUFSTÜCKELUNG:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} Transaktionen)
{% endfor %}

KASSENABRECHNUNG:
- Anfangskasse: {{ opening_cash }}
- Kassengeschäfte: {{ cash_sales }}
- Erwartete Kasse: {{ expected_cash }}
- Zählte Kasse: {{ counted_cash }}
- Unterschied: {{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ KASSENUNTERSCHIED: {{ discrepancy_amount }}
{% if discrepancy_note %}Hinweis: {{ discrepancy_note }}{% endif %}
{% endif %}

Vollständigen Bericht ansehen: {{ shift_report_url }}