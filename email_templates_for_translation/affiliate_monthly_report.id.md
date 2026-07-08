---
template_type: affiliate_monthly_report
category: Affiliate Program
---

# Email Template: affiliate_monthly_report

## Subject
Laporan Afiliasi Bulanan Anda - {{ month_name }} {{ year }}

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
          📊 Laporan Afiliasi Bulanan
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Ringkasan Kinerja {{ month_name }} {{ year }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Summary Cards -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          💰 Total Diperoleh
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#28a745" align="center" line-height="1">
          {{ total_earned }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📦 Komisi
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#007bff" align="center" line-height="1">
          {{ commission_count }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📈 Rata-rata per Penjualan
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
          Hai {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Berikut adalah ringkasan kinerja Anda untuk {{ month_name }} {{ year }}. Kerja bagus bulan ini!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Top Orders Table -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" padding-bottom="15px">
          🏆 Top {{ top_orders_count }} Pesanan
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          <table style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="background-color: #f8f9fa;">
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Order</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Komisi</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Tanggal</th>
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
          <strong>💳 Status Pembayaran</strong>
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          Saldo Tertunda: <strong>{{ pending_balance }}</strong><br/>
          Status: {{ payment_status }}
          {% if next_payout_date %}
          <br/>Pembayaran Berikutnya: {{ next_payout_date }}
          {% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Lihat Dashboard Lengkap
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Pertanyaan? <a href="mailto:{{ support_email }}" style="color: #007bff;">Hubungi Dukungan</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Laporan Afiliasi Bulanan Anda - {{ month_name }} {{ year }}

Hai {{ affiliate_name }},

Berikut adalah ringkasan kinerja Anda untuk {{ month_name }} {{ year }}:

📊 RINGKASAN BULANAN
- Total Diperoleh: {{ total_earned }}
- Jumlah Komisi: {{ commission_count }}
- Rata-rata per Penjualan: {{ avg_commission }}

🏆 TOP {{ top_orders_count }} PESANAN
{% for order in top_orders %}
#{{ order.order_number }} - {{ order.commission_amount }} ({{ order.order_date }})
{% endfor %}

💳 STATUS PEMBAYARAN
Saldo Tertunda: {{ pending_balance }}
Status: {{ payment_status }}
{% if next_payout_date %}Pembayaran Berikutnya: {{ next_payout_date }}{% endif %}

Lihat dashboard lengkap Anda: {{ portal_url }}

Kerja bagus bulan ini!

{{ shop_name }}
Pertanyaan? Hubungi {{ support_email }}