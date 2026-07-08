---
template_type: affiliate_monthly_report
category: Affiliate Program
---

# Email Template: affiliate_monthly_report

## Subject
您的每月聯盟報告 - {{ month_name }} {{ year }}

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
          📊 每月聯盟報告
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          {{ month_name }} {{ year }} 表現摘要
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Summary Cards -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          💰 總收入
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#28a745" align="center" line-height="1">
          {{ total_earned }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📦 分紅
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#007bff" align="center" line-height="1">
          {{ commission_count }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📈 每筆平均
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
          Hi {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          這是 {{ month_name }} {{ year }} 的表現摘要。本月表現出色！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Top Orders Table -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" padding-bottom="15px">
          🏆 本月 {{ top_orders_count }} 頂部訂單
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          <table style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="background-color: #f8f9fa;">
                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Order</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Commission</th>
                <th style="padding: 10px; text-align: right; border-bottom: 2px solid #dee2e6;">Date</th>
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
          <strong>💳 支付狀態</strong>
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          懸浮餘額: <strong>{{ pending_balance }}</strong><br/>
          狀態: {{ payment_status }}
          {% if next_payout_date %}
          <br/>下一次發放: {{ next_payout_date }}
          {% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          查看完整儀錶板
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          問題? <a href="mailto:{{ support_email }}" style="color: #007bff;">
            聯絡支援
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
您的每月聯盟報告 - {{ month_name }} {{ year }}

您好 {{ affiliate_name }}，

以下是 {{ month_name }} {{ year }} 的表現摘要：

📊 月度摘要
- 總收入：{{ total_earned }}
- 分紅數量：{{ commission_count }}
- 每筆平均：{{ avg_commission }}

🏆 頂部 {{ top_orders_count }} 訂單
{% for order in top_orders %}
#{{ order.order_number }} - {{ order.commission_amount }} ({{ order.order_date }})
{% endfor %}

💳 支付狀態
懸浮餘額：{{ pending_balance }}
狀態：{{ payment_status }}
{% if next_payout_date %}下一次發放：{{ next_payout_date }}{% endif %}

查看完整儀錶板：{{ portal_url }}

本月表現出色！

{{ shop_name }}
問題？聯絡 {{ support_email }}