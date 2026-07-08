---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
佣金状态更新 - 订单 #{{ order_number }}

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
          佣金状态更新
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          你好 {{ affiliate_name }}，
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          我们想通知你，订单 #{{ order_number }}（{{ commission_amount }}）的佣金未获批准。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          这通常发生在佣金周期结束前订单被取消或退款的情况下。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          如果你对这笔佣金有疑问，请联系我们的支持团队。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          查看联盟仪表板
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          有问题？ <a href="mailto:{{ support_email }}" style="color: #007bff;">联系支持</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
佣金状态更新 - 订单 #{{ order_number }}

你好 {{ affiliate_name }}，

我们想通知你，订单 #{{ order_number }}（{{ commission_amount }}）的佣金未获批准。

这通常发生在佣金周期结束前订单被取消或退款的情况下。

如果你对这笔佣金有疑问，请联系我们的支持团队。

查看你的仪表板：{{ portal_url }}

{{ shop_name }}
有问题？联系 {{ support_email }}
