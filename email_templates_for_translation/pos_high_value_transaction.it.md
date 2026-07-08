---
template_type: pos_high_value_transaction
category: POS
---

# Email Template: pos_high_value_transaction

## Subject
💰 Transazione di alto valore: {{ transaction_amount }} a {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          💰 Transazione di alto valore
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Transazione di grande importo elaborata
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          È stata elaborata una transazione di {{ transaction_amount }} al {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Dettagli della transazione:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Amount:</strong> <span style="font-size: 18px; font-weight: bold; color: #059669;">{{ transaction_amount }}</span><br/>
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Cashier:</strong> {{ cashier_name }}<br/>
              <strong>Timestamp:</strong> {{ transaction_time }}<br/>
              <strong>Transaction ID:</strong> {{ transaction_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informazioni sul pagamento:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}</strong>: {{ payment.amount }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Riepilogo degli articoli:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Items:</strong> {{ item_count }}<br/>
              <strong>Subtotal:</strong> {{ subtotal }}<br/>
              <strong>Tax:</strong> {{ tax_amount }}<br/>
              <strong>Total:</strong> {{ transaction_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if customer_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informazioni sul cliente:
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
              Questa notifica viene inviata per tutte le transazioni che superano {{ threshold_amount }} per scopi di prevenzione e monitoraggio dello spam.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ transaction_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza transazione
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ receipt_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Visualizza ricevuta
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 TRANSAZIONE DI ALTO VALORE

Transazione di grande importo elaborata

È stata elaborata una transazione di {{ transaction_amount }} al {{ terminal_name }}.

DETTAGLI DELLA TRANSAZIONE:
- Amount: {{ transaction_amount }}
- Terminal: {{ terminal_name }}
- Cashier: {{ cashier_name }}
- Timestamp: {{ transaction_time }}
- Transaction ID: {{ transaction_id }}

INFORMAZIONI SUL PAGAMENTO:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }}
{% endfor %}

RIEPILOGO DEGLI ARTICOLI:
- Total Items: {{ item_count }}
- Subtotal: {{ subtotal }}
- Tax: {{ tax_amount }}
- Total: {{ transaction_amount }}

{% if customer_info %}
INFORMAZIONI SUL CLIENTE:
{{ customer_info }}
{% endif %}

Questa notifica viene inviata per tutte le transazioni che superano {{ threshold_amount }} per scopi di prevenzione e monitoraggio dello spam.

Visualizza transazione: {{ transaction_url }}
Visualizza ricevuta: {{ receipt_url }}