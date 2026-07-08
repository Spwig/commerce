---
template_type: affiliate_monthly_report
category: Affiliate Program
---

# Email Template: affiliate_monthly_report

## Subject
アフィリエイト月次レポート - {{ month_name }} {{ year }}

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
          📊 月次アフィリエイトレポート
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          {{ month_name }} {{ year }} パフォーマンスサマリー
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Summary Cards -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          💰 総収入
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#28a745" align="center" line-height="1">
          {{ total_earned }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📦 委譲金
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="#007bff" align="center" line-height="1">
          {{ commission_count }}
        </mj-text>
      </mj-column>
      <mj-column width="33%">
        <mj-text font-size="14px" color="#6c757d" align="center" padding-bottom="5px">
          📈 売上平均
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
          こんにちは {{ affiliate_name }}、
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          こちらが {{ month_name }} {{ year }} のパフォーマンスサマリーです。今月は素晴らしい仕事でした！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Top Orders Table -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" padding-bottom="15px">
          🏆 {{ top_orders_count }} 位の注文
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
          <strong>💳 支払いステータス</strong>
        </mj-text>
        <mj-text font-size="14px" color="#212529">
          保留金額: <strong>{{ pending_balance }}</strong><br/>
          ステータス: {{ payment_status }}
          {% if next_payout_date %}
          <br/>次の支払い日: {{ next_payout_date }}
          {% endif %}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          ダッシュボードを確認する
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          質問は？ <a href="mailto:{{ support_email }}" style="color: #007bff;">
            サポートに連絡する
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
アフィリエイト月次レポート - {{ month_name }} {{ year }}

こんにちは {{ affiliate_name }}、

こちらが {{ month_name }} {{ year }} のパフォーマンスサマリーです：

📊 モンスリー・サマリー
- 総収入：{{ total_earned }}
- 委譲金の数：{{ commission_count }}
- 売上平均：{{ avg_commission }}

🏆 ベスト {{ top_orders_count }} 注文
{% for order in top_orders %}
#{{ order.order_number }} - {{ order.commission_amount }} ({{ order.order_date }})
{% endfor %}

💳 支払いステータス
保留金額：{{ pending_balance }}
ステータス：{{ payment_status }}
{% if next_payout_date %}次の支払い日：{{ next_payout_date }}{% endif %}

ダッシュボードを確認する：{{ portal_url }}

今月は素晴らしい仕事でした！

{{ shop_name }}
質問は？ {{ support_email }} に連絡してください。