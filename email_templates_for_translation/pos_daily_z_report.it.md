---
template_type: pos_daily_z_report
category: POS
---

# Email Template: pos_daily_z_report

## Subject
📊 Rapporto Z Giornaliero - {{ report_date }} - {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Rapporto Z Giornaliero
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Rapporto di Liquidazione Fine Giornata
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Riepilogo giornaliero per {{ location_name }} del {{ report_date }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Riepilogo Vendite:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Totale Vendite:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_sales }}</span><br/>
              <strong>Transazioni:</strong> {{ transaction_count }}<br/>
              <strong>Articoli Venduti:</strong> {{ items_sold }}<br/>
              <strong>Vendita Media:</strong> {{ average_sale }}<br/>
              <strong>Tasse Riscosse:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Metodi di Pagamento:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }} ({{ payment.count }} transazioni)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Riepilogo Turni:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Totale Turni:</strong> {{ shift_count }}<br/>
              <strong>Terminali Utilizzati:</strong> {{ terminal_count }}<br/>
              <strong>Cassieri Attivi:</strong> {{ cashier_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% for terminal in terminal_stats %}
        <mj-spacer height="15px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ terminal.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Vendite: {{ terminal.sales }} | Transazioni: {{ terminal.transactions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Regolamenti e Sconti:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Sconti Concessi:</strong> {{ discounts_total }}<br/>
              <strong>Rimborsi Eseguiti:</strong> {{ refunds_total }}<br/>
              <strong>Annullamenti:</strong> {{ voids_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cash_variance != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Variazione Totale Cassa: {{ cash_variance }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              {{ variance_note }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Prodotti Più Venduti:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.quantity }} venduti ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza Rapporto Completo
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 RAPPORTO Z GIORNALIERO

Rapporto di Liquidazione Fine Giornata

Riepilogo giornaliero per {{ location_name }} del {{ report_date }}.

RIEPILOGO VENDITE:
- Totale Vendite: {{ total_sales }}
- Transazioni: {{ transaction_count }}
- Articoli Venduti: {{ items_sold }}
- Vendita Media: {{ average_sale }}
- Tasse Riscosse: {{ tax_collected }}

METODI DI PAGAMENTO:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} transazioni)
{% endfor %}

RIEPILOGO DEI TURNI:
- Totale Turni: {{ shift_count }}
- Terminali Utilizzati: {{ terminal_count }}
- Cassieri Attivi: {{ cashier_count }}

DETTAGLIO DEI TERMINALI:
{% for terminal in terminal_stats %}
{{ terminal.name }}: {{ terminal.sales }} | {{ terminal.transactions }} transazioni
{% endfor %}

REGOLAMENTI & SCONTI:
- Sconti Concessi: {{ discounts_total }}
- Rimborsi Eseguiti: {{ refunds_total }}
- Annullamenti: {{ voids_total }}

{% if cash_variance != 0 %}
⚠️ VARIAZIONE TOTALE CASSA: {{ cash_variance }}
{{ variance_note }}
{% endif %}

PRODOTTI PIÙ VENDUTI:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.quantity }} venduti ({{ product.revenue }})
{% endfor %}

Visualizza rapporto completo: {{ full_report_url }}