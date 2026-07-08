---
template_type: admin_report_weekly_digest
category: Admin Reports
---

# Email Template: admin_report_weekly_digest

## Subject
📈 Wöchentlicher Bericht - {{ week_range }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📈 Wöchentlicher Bericht
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Woche von {{ week_range }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Umsatz:</strong> <span style="font-size: 20px; color: #059669;">{{ total_revenue }}</span> ({{ revenue_change }})<br/>
              <strong>Bestellungen:</strong> {{ total_orders }} ({{ orders_change }})<br/>
              <strong>Neue Kunden:</strong> {{ new_customers }}<br/>
              <strong>Durchschnittswert pro Bestellung:</strong> {{ avg_order_value }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Highlights:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ highlights }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Bericht vollständig anzeigen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📈 WÖCHENTLICHER BERICHT

Woche von {{ week_range }}

LEISTUNGSDATEN:
- Umsatz: {{ total_revenue }} ({{ revenue_change }})
- Bestellungen: {{ total_orders }} ({{ orders_change }})
- Neue Kunden: {{ new_customers }}
- Durchschnittswert pro Bestellung: {{ avg_order_value }}

HIGHLIGHTS:
{{ highlights }}

Vollständigen Bericht ansehen: {{ full_report_url }}