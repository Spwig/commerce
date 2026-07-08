---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
付款失敗 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          付款失敗
        </mj-text>
        <mj-text>
          有付款嘗試失敗於訂單 #{{ order_number }}。
        </mj-text>
        <mj-text>
          <strong>顧客：</strong>{{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>金額：</strong>{{ order_total }}
        </mj-text>
        <mj-text>
          <strong>錯誤：</strong>{{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          在管理端查看
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
付款失敗

有付款嘗試失敗於訂單 #{{ order_number }}。

顧客：{{ customer_name }}
金額：{{ order_total }}
錯誤：{{ error_message }}

在管理端查看：{{ admin_order_url }}