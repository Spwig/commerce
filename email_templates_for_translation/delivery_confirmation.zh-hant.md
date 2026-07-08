---
template_type: delivery_confirmation
category: Core E-commerce
---

# Email Template: delivery_confirmation

## Subject
訂單已送達 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          訂單已送達
        </mj-text>
        <mj-text>
          您的訂單 #{{ order_number }} 已送達！
        </mj-text>
        <mj-text>
          我們希望您喜歡您的購買。如果您有任何問題或疑慮，請隨時聯繫我們。
        </mj-text>
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          查看訂單
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
訂單已送達

您的訂單 #{{ order_number }} 已送達！

我們希望您喜歡您的購買。如果您有任何問題或疑慮，請隨時聯繫我們。

查看訂單：{{ order_url }}