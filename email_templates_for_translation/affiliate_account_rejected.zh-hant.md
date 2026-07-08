---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
合作夥伴申請更新

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
          申請更新
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          請問 {{ affiliate_name }}，
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          感謝您對加入 {{ shop_name }} 合作夥伴計劃的興趣。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          在審查您的申請後，我們目前決定不繼續進行。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          這個決定是基於我們目前的合作夥伴計劃要求，可能不會反映您的資格或潛力。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          如果您的情況發生變化，歡迎您未來重新申請。
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
合作夥伴申請更新

請問 {{ affiliate_name }}，

感謝您對加入 {{ shop_name }} 合作夥伴計劃的興趣。

在審查您的申請後，我們目前決定不繼續進行。

這個決定是基於我們目前的合作夥伴計劃要求，可能不會反映您的資格或潛力。

如果您的情況發生變化，歡迎您未來重新申請。

{{ shop_name }}
問題？聯繫 {{ support_email }}