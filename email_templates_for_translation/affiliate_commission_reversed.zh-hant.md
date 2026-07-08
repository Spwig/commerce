---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
佣金已退回 - 訂單 #{{ order_number }}

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
          佣金已退回
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
          因客戶退款，訂單 #{{ order_number }} ({{ commission_amount }}) 的佣金已退回。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          當客戶申請退款時，相關的佣金會自動退回，以確保賬務準確。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          這是聯營過程中的正常情況。繼續推廣 {{ shop_name }} 以賺取新佣金！
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          查看聯營儀表板
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          問題？<a href="mailto:{{ support_email }}" style="color: #007bff;">聯繫支援</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
佣金已退回 - 訂單 #{{ order_number }}

親愛的 {{ affiliate_name }}，

因客戶退款，訂單 #{{ order_number }} ({{ commission_amount }}) 的佣金已退回。

當客戶申請退款時，相關的佣金會自動退回，以確保賬務準確。

這是聯營過程中的正常情況。繼續推廣 {{ shop_name }} 以賺取新佣金！

查看你的儀表板：{{ portal_url }}

{{ shop_name }}
問題？聯繫 {{ support_email }}
