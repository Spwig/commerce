---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
重要：账户已被暂停

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
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          账户已被暂停
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
          您的联盟账户 {{ shop_name }} 已被暂停。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          这通常是由于违反了我们的联盟计划条款和条件。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          如果您认为这是错误的，或想讨论此决定，请联系我们的支持团队。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          有问题吗？ <a href="mailto:{{ support_email }}" style="color: #007bff;">联系支持</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
重要：账户已被暂停

你好 {{ affiliate_name }}，

您的联盟账户 {{ shop_name }} 已被暂停。

这通常是由于违反了我们的联盟计划条款和条件。

如果您认为这是错误的，或想讨论此决定，请联系我们的支持团队。

{{ shop_name }}
有问题吗？联系 {{ support_email }}}