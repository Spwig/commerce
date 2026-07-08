---
template_type: affiliate_monthly_report
category: Affiliate Program
---

# Email Template: affiliate_monthly_report

## Subject
Ihr monatlicher Partnerbericht - {{ month_name }} {{ year }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          📊 Monatlicher Partnerbericht
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          {{ month_name }} {{ year }} Leistungsbericht
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Summary Cards -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          💰 Gesamteinnahmen
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#28a745" align="center" line-height="1">
          {{ total_earned }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📦 Kommissionen
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#007bff" align="center" line-height="1">
          {{ commission_count }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📈 Durchschnitt pro Verkauf
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#6f42c1" align="center" line-height="1">
          {{ avg_commission }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hallo {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Hier ist Ihr Leistungsbericht für {{ month_name }} {{ year }}. Große Arbeit diesen Monat!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Top Orders Table -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" padding-bottom="15px">
          🏆 Top {{ top_orders_count }} Bestellungen
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          <table style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="background-color: #f8f9fa;">
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Bestellung</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Kommission</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Datum</th>
              </tr>
            </thead>
            <tbody>
              {% for order in top_orders %}
              <tr>
                <td style="padding: 10px; border-bottom: 1px solid #dee2e6;">#{{ order.order_number }}</td>
                <td style="padding: 10px; text-align: right; border-bottom: 1px solid #dee2e6; color: #28a745; font-weight: 600;">{{ order.commission_amount }}</td>
                <td style="padding: 10px; text-align: right; border-bottom: 1px solid #dee2e6; color: #6c757d;">{{ order.order_date }}</td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Status -->
    <mj-section background-color="#e3f2fd" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>💳 Zahlungsstatus</strong>
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          Ausstehender Betrag: <strong>{{ pending_balance }}</strong><br/>
          Status: {{ payment_status }}
          {% if next_payout_date %}
          <br/>Nächste Auszahlung: {{ next_payout_date }}
          {% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Vollständige Dashboard ansehen
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Fragen? <a href="mailto:{{ support_email }}" style="color: #007bff;">Support kontaktieren</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ihr monatlicher Partnerbericht - {{ month_name }} {{ year }}

Hi {{ affiliate_name }},

Hier ist Ihr Leistungsbericht für {{ month_name }} {{ year }}:

📊 MONATLICHER LEISTUNGSBERICHT
- Gesamteinnahmen: {{ total_earned }}
- Anzahl der Kommissionen: {{ commission_count }}
- Durchschnitt pro Verkauf: {{ avg_commission }}

🏆 BESTE {{ top_orders_count }} BESTELLUNGEN
{% for order in top_orders %}
#{{ order.order_number }} - {{ order.commission_amount }} ({{ order.order_date }})
{% endfor %}

💳 ZAHLUNGSSTATUS
Ausstehender Betrag: {{ pending_balance }}
Status: {{ payment_status }}
{% if next_payout_date %}Nächste Auszahlung: {{ next_payout_date }}{% endif %}

Vollständige Dashboard ansehen: {{ portal_url }}

Große Arbeit diesen Monat!

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}