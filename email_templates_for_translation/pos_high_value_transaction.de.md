---
template_type: pos_high_value_transaction
category: POS
---

# Email Template: pos_high_value_transaction

## Subject
💰 Hoher Wert Transaktion: {{ transaction_amount }} an {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          💰 Hoher Wert Transaktion
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Große Transaktion verarbeitet
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Eine Transaktion von {{ transaction_amount }} wurde an {{ terminal_name }} verarbeitet.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Transaktionsdetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Betrag:</strong> <span style="font-size: 18px; font-weight: bold; color: #059669;">{{ transaction_amount }}</span><br/>
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Kassierer:</strong> {{ cashier_name }}<br/>
              <strong>Zeitstempel:</strong> {{ transaction_time }}<br/>
              <strong>Transaktions-ID:</strong> {{ transaction_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Zahlungsinformationen:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Artikelzusammenfassung:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Gesamtartikel:</strong> {{ item_count }}<br/>
              <strong>Unter total:</strong> {{ subtotal }}<br/>
              <strong>Steuer:</strong> {{ tax_amount }}<br/>
              <strong>Gesamt:</strong> {{ transaction_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if customer_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Kundendaten:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ customer_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              Diese Benachrichtigung wird gesendet, wenn Transaktionen {{ threshold_amount }} überschreiten, um Betrug vorzubeugen und zu überwachen.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ transaction_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Transaktion ansehen
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ receipt_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Beleg ansehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 HOHE WERT TRANSAKTION

Große Transaktion verarbeitet

Eine Transaktion von {{ transaction_amount }} wurde an {{ terminal_name }} verarbeitet.

TRANSAKTIONSDETAILS:
- Betrag: {{ transaction_amount }}
- Terminal: {{ terminal_name }}
- Kassierer: {{ cashier_name }}
- Zeitstempel: {{ transaction_time }}
- Transaktions-ID: {{ transaction_id }}

ZAHLUNGSINFORMATIONEN:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }}
{% endfor %}

ARTIKELZUSAMMENFASSUNG:
- Gesamtartikel: {{ item_count }}
- Unter total: {{ subtotal }}
- Steuer: {{ tax_amount }}
- Gesamt: {{ transaction_amount }}

{% if customer_info %}
KUNDENDATEN:
{{ customer_info }}
{% endif %}

Diese Benachrichtigung wird gesendet, wenn Transaktionen {{ threshold_amount }} überschreiten, um Betrug vorzubeugen und zu überwachen.

Transaktion ansehen: {{ transaction_url }}
Beleg ansehen: {{ receipt_url }}