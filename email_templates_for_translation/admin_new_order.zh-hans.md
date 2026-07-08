---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
新订单收到 - 订单 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          新订单收到
        </mj-text>
        <mj-text>
          您的商店上有一个新订单。
        </mj-text>
        <mj-text>
          <strong>订单编号：</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>客户：</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>总计：</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          在后台查看
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
新订单收到

您的商店上有一个新订单。

订单编号：{{ order_number }}
客户：{{ customer_name }}
总计：{{ order_total }}

在后台查看：{{ admin_order_url }}