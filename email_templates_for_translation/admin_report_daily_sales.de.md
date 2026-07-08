---
template_type: admin_report_daily_sales
category: Admin Reports
---

# Email Template: admin_report_daily_sales

## Subject
📊 Täglicher Umsatzbericht - {{ report_date }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Täglicher Umsatzbericht
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Umsatzzusammenfassung - {{ report_date }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Gesamter Umsatz:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_revenue }}</span><br/>
              <strong>Bestellungen:</strong> {{ order_count }}<br/>
              <strong>Durchschnittswert einer Bestellung:</strong> {{ avg_order_value }}<br/>
              <strong>Umwandlungsrate:</strong> {{ conversion_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Besucher:</strong> {{ visitor_count }}<br/>
              <strong>Neue Kunden:</strong> {{ new_customers }}<br/>
              <strong>Rückkehrende Kunden:</strong> {{ returning_customers }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Top Produkte:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.sales }} Verkäufe ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Bericht vollständig ansehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 TÄGLICHER UMSATZBERICHT

Umsatzzusammenfassung - {{ report_date }}

LEISTUNGEN:
- Gesamter Umsatz: {{ total_revenue }}
- Bestellungen: {{ order_count }}
- Durchschnittswert einer Bestellung: {{ avg_order_value }}
- Umwandlungsrate: {{ conversion_rate }}%

VERKEHR:
- Besucher: {{ visitor_count }}
- Neue Kunden: {{ new_customers }}
- Rückkehrende Kunden: {{ returning_customers }}

TOP PRODUKTE:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.sales }} Verkäufe ({{ product.revenue }})
{% endfor %}

Vollständigen Bericht ansehen: {{ full_report_url }}