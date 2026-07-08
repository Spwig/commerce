---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ 資金撥款完成：{{ payout_amount }}

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
          🎉 資金撥款完成！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ 已成功付款
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          資金撥款 ID：{{ payout_id }}
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
          您的資金撥款 {{ payout_amount }} 已成功完成！
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          資金已匯款至您的支付方式。根據您的銀行或支付處理商，可能需要 1-2 個工作天才會出現在您的帳戶中。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          謝謝您推廣 {{ shop_name }}。繼續保持優異的表現！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          查看資金撥款詳情
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          問題？<a href="mailto:{{ support_email }}" style="color: #007bff;">聯絡支援</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 資金撥款完成：{{ payout_amount }}

您好 {{ affiliate_name }}，

您的資金撥款 {{ payout_amount }} 已成功完成！

資金撥款詳情：
- 資金撥款 ID：{{ payout_id }}
- 金額：{{ payout_amount }}
- 支付方式：{{ payout_method }}

資金已匯款至您的支付方式。根據您的銀行或支付處理商，可能需要 1-2 個工作天才會出現在您的帳戶中。

謝謝您推廣 {{ shop_name }}。繼續保持優異的表現！

查看資金撥款詳情：{{ portal_url }}

{{ shop_name }}
問題？聯絡 {{ support_email }}