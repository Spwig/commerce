---
template_type: affiliate_monthly_report
category: Affiliate Program
---

# Email Template: affiliate_monthly_report

## Subject
Aylık Ortak Raporunuz - {{ month_name }} {{ year }}

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
          📊 Aylık Ortak Raporu
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          {{ month_name }} {{ year }} Performans Özeti
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Summary Cards -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          💰 Toplam Kazanç
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#28a745" align="center" line-height="1">
          {{ total_earned }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📦 Komisyonlar
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#007bff" align="center" line-height="1">
          {{ commission_count }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📈 Satış Başına Ortalama
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
          Merhaba {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Burada {{ month_name }} {{ year }} için performans özeti. Bu ay harikulade bir iş çıkardınız!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Top Orders Table -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" padding-bottom="15px">
          🏆 {{ top_orders_count }} En İyi Siparişler
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          <table style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="background-color: #f8f9fa;">
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Sipariş</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Komisyon</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Tarih</th>
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
          <strong>💳 Ödeme Durumu</strong>
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          Bekleyen Bakiye: <strong>{{ pending_balance }}</strong><br/>
          Durum: {{ payment_status }}
          {% if next_payout_date %}
          <br/>Sonraki Ödeme: {{ next_payout_date }}
          {% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Tam Dashboard'ı Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Sorularınız mı var? <a href="mailto:{{ support_email }}" style="color: #007bff;">Destek ile İletişime Geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Aylık Ortak Raporunuz - {{ month_name }} {{ year }}

Merhaba {{ affiliate_name }},

{{ month_name }} {{ year }} için performans özeti:

📊 AYLIK ÖZET
- Toplam Kazanç: {{ total_earned }}
- Komisyon Sayısı: {{ commission_count }}
- Satış Başına Ortalama: {{ avg_commission }}

🏆 EN İYİ {{ top_orders_count }} SİPARİŞ
{% for order in top_orders %}
#{{ order.order_number }} - {{ order.commission_amount }} ({{ order.order_date }})
{% endfor %}

💳 ÖDEME DURUMU
Bekleyen Bakiye: {{ pending_balance }}
Durum: {{ payment_status }}
{% if next_payout_date %}Sonraki Ödeme: {{ next_payout_date }}{% endif %}

Tam dashboard'ı görüntüleyin: {{ portal_url }}

Bu ay harikulade bir iş çıkardınız!

{{ shop_name }}
Sorularınız mı var? {{ support_email }} ile iletişime geçin