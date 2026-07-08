---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
重要：帳戶已被停用

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
          帳戶已被停用
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          您好 {{ affiliate_name }}，
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          您的聯營帳戶 {{ shop_name }} 已被停用。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          這通常是由於違反我們的聯營計劃條款和條件所致。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          如果您認為這是個錯誤，或想討論此決定，請聯繫我們的支援團隊。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          問題？ <a href="mailto:{{ support_email }}" style="color: #007bff;">聯繫支援</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
重要：帳戶已被停用

您好 {{ affiliate_name }}，

您的聯營帳戶 {{ shop_name }} 已被停用。

這通常是由於違反我們的聯營計劃條款和條件所致。

如果您認為這是個錯誤，或想討論此決定，請聯繫我們的支援團隊。

{{ shop_name }}
問題？聯繫 {{ support_email }}