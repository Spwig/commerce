---
template_type: affiliate_payout_processing
category: Affiliate Program
---

# Email Template: affiliate_payout_processing

## Subject
您的 {{ payout_amount }} 提款正在處理中

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
          💸 提款處理中
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#17a2b8" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          處理您的提款
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          提款 ID：{{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hi {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          好消息！您的 {{ payout_amount }} 提款現在正在處理中。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          資金應在 3-5 個工作天內到達您的帳戶。提款完成後，您將收到另一封電子郵件。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>提款 ID：</strong>{{ payout_id }}<br/>
          <strong>金額：</strong>{{ payout_amount }}<br/>
          <strong>付款方式：</strong>{{ payout_method }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          查看提款記錄
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          有問題？<a href="mailto:{{ support_email }}" style="color: #007bff;">
            聯絡支援
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
您的 {{ payout_amount }} 提款正在處理中

Hi {{ affiliate_name }},

好消息！您的 {{ payout_amount }} 提款現在正在處理中。

提款細節：
- 提款 ID：{{ payout_id }}
- 金額：{{ payout_amount }}
- 付款方式：{{ payout_method }}

資金應在 3-5 個工作天內到達您的帳戶。提款完成後，您將收到另一封電子郵件。

查看提款記錄：{{ portal_url }}

{{ shop_name }}
有問題？聯繫 {{ support_email }}