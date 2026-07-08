---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
付款取消 - {{ payout_amount }}

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
          付款取消
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          親愛的 {{ affiliate_name }}，
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          您的付款 {{ payout_amount }} (付款 ID：{{ payout_id }}) 已被取消。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          如果您對此付款被取消有任何疑問，請聯繫我們的支援團隊。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          查看聯盟專區
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          有問題？ <a href="mailto:{{ support_email }}" style="color: #007bff;">聯繫支援</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
付款取消 - {{ payout_amount }}

親愛的 {{ affiliate_name }}，

您的付款 {{ payout_amount }} (付款 ID：{{ payout_id }}) 已被取消。

如果您對此付款被取消有任何疑問，請聯繫我們的支援團隊。

查看您的專區：{{ portal_url }}

{{ shop_name }}
有問題？聯繫 {{ support_email }}