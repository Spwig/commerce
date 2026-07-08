---
template_type: affiliate_commission_approved
category: Affiliate Program
---

# Email Template: affiliate_commission_approved

## Subject
佣金已通过：{{ commission_amount }}

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
          ✓ 佣金已通过！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Approval Display -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          已通过付款
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
          您来自订单 #{{ order_number }} 的佣金 {{ commission_amount }} 已通过，并将包含在您的下一次付款中。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          付款将按照您的付款计划进行处理。付款处理时，您将收到另一封电子邮件。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          查看佣金
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
佣金已通过：{{ commission_amount }}

你好 {{ affiliate_name }}，

您来自订单 #{{ order_number }} 的佣金 {{ commission_amount }} 已通过，并将包含在您的下一次付款中。

付款将按照您的付款计划进行处理。付款处理时，您将收到另一封电子邮件。

查看您的佣金：{{ portal_url }}

{{ shop_name }}
有问题？联系 {{ support_email }}