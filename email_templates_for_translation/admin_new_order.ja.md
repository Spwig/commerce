---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
新規注文の受注 - 注文番号 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          新規注文の受注
        </mj-text>
        <mj-text>
          あなたの店舗に新しい注文が入りました。
        </mj-text>
        <mj-text>
          <strong>注文番号:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>顧客:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>合計金額:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          管理画面で確認
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
新規注文の受注

あなたの店舗に新しい注文が入りました。

注文番号: {{ order_number }}
顧客: {{ customer_name }}
合計金額: {{ order_total }}

管理画面で確認: {{ admin_order_url }}