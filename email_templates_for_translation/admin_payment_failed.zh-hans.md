---
template_type: admin_payment_failed
category: Admin Notifications
---

# Email Template: admin_payment_failed

## Subject
付款失败 - 订单 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}">
          付款失败
        </mj-text>
        <mj-text>
          有一笔订单 #{{ order_number }} 的付款尝试失败。
        </mj-text>
        <mj-text>
          <strong>客户：</strong>{{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>金额：</strong>{{ order_total }}
        </mj-text>
        <mj-text>
          <strong>错误：</strong>{{ error_message }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}">
          在管理后台中查看
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
付款失败

有一笔订单 #{{ order_number }} 的付款尝试失败。

客户：{{ customer_name }}
金额：{{ order_total }}
错误：{{ error_message }}

在管理后台中查看：{{ admin_order_url }}