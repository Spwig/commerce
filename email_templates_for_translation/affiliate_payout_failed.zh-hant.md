---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
需要采取行動：付款失敗

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
          ⚠️ 付款失敗
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          付款 ID：{{ payout_id }}
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
          我們在處理您 {{ payout_amount }} 的付款時遇到了問題。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          這通常是由于付款信息不正確或付款提供商的問題。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          請在您的聯營經銷商儀表板上更新付款信息，並聯繫我們的支援團隊以解決此問題。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          更新付款信息
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          需要幫助？ <a href="mailto:{{ support_email }}" style="color: #007bff;">聯繫支援</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
需要采取行動：付款失敗

您好 {{ affiliate_name }}，

我們在處理您 {{ payout_amount }} 的付款時遇到了問題（付款 ID：{{ payout_id }}）。

這通常是由于付款信息不正確或付款提供商的問題。

請在您的聯營經銷商儀表板上更新付款信息，並聯繫我們的支援團隊以解決此問題。

更新付款信息：{{ portal_url }}

{{ shop_name }}
需要幫助？聯繫 {{ support_email }}