---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
收到新訂單 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          收到新訂單
        </mj-text>
        <mj-text>
          有新的訂單已放在您的商店。
        </mj-text>
        <mj-text>
          <strong>訂單編號：</strong>{{ order_number }}
        </mj-text>
        <mj-text>
          <strong>客戶：</strong>{{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>總計：</strong>{{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          在管理後台查看
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
收到新訂單

有新的訂單已放在您的商店。

訂單編號：{{ order_number }}
客戶：{{ customer_name }}
總計：{{ order_total }}

在管理後台查看：{{ admin_order_url }}