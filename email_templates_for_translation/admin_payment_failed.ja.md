---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
支払い失敗 - 注文 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          支払い失敗
        </mj-text>
        <mj-text>
          注文 #{{ order_number }} への支払いが失敗しました。
        </mj-text>
        <mj-text>
          <strong>顧客:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>金額:</strong> {{ order_total }}
        </mj-text>
        <mj-text>
          <strong>エラー:</strong> {{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          管理画面で確認
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
支払い失敗

注文 #{{ order_number }} への支払いが失敗しました。

顧客: {{ customer_name }}
金額: {{ order_total }}
エラー: {{ error_message }}

管理画面で確認: {{ admin_order_url }}