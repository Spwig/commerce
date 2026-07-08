---
template_type: affiliate_commission_approved
category: Affiliate Program
---

# Email Template: affiliate_commission_approved

## Subject
佣金已核准：{{ commission_amount }}

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
          ✓ 佣金已核准！
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
          已核准發款
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
          您來自訂單 #{{ order_number }} 的佣金 {{ commission_amount }} 已核准，將包含在您下一次的發款中。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          發款將根據您的付款時間表進行處理。發款處理時，您會收到另一封郵件。
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
          問題？ <a href="mailto:{{ support_email }}" style="color: #007bff;">聯絡支援</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
佣金已核准：{{ commission_amount }}

您好 {{ affiliate_name }}，

您來自訂單 #{{ order_number }} 的佣金 {{ commission_amount }} 已核准，將包含在您下一次的發款中。

發款將根據您的付款時間表進行處理。發款處理時，您會收到另一封郵件。

查看您的佣金：{{ portal_url }}

{{ shop_name }}
問題？聯絡 {{ support_email }}