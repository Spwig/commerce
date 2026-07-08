---
template_type: admin_report_daily_sales
category: Admin Reports
---

# Email Template: admin_report_daily_sales

## Subject
📊 Rapporto di vendita giornaliero - {{ report_date }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Rapporto di vendita giornaliero
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Riepilogo delle vendite - {{ report_date }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Entrate totali:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_revenue }}</span><br/>
              <strong>Ordini:</strong> {{ order_count }}<br/>
              <strong>Valore medio dell'ordine:</strong> {{ avg_order_value }}<br/>
              <strong>Tasso di conversione:</strong> {{ conversion_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Visitatori:</strong> {{ visitor_count }}<br/>
              <strong>Nuovi clienti:</strong> {{ new_customers }}<br/>
              <strong>Clienti tornati:</strong> {{ returning_customers }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Prodotti più venduti:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.sales }} vendite ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Visualizza rapporto completo
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 RAPPORTO DI VENDITA GIORNALIERO

Riepilogo delle vendite - {{ report_date }}

PRESTAZIONI:
- Entrate totali: {{ total_revenue }}
- Ordini: {{ order_count }}
- Valore medio dell'ordine: {{ avg_order_value }}
- Tasso di conversione: {{ conversion_rate }}%

TRAFFICO:
- Visitatori: {{ visitor_count }}
- Nuovi clienti: {{ new_customers }}
- Clienti tornati: {{ returning_customers }}

PRODOTTI PIÙ VENDUTI:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.sales }} vendite ({{ product.revenue }})
{% endfor %}

Visualizza rapporto completo: {{ full_report_url }}