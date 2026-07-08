---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
有關您的訂單 #{{ order_number }} - 運送延遲

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          有關您的訂單
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我們想通知您有關您的訂單的延遲情況。我們對由此帶來的不便表示歉意，並感謝您的耐心等待。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              訂單詳情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>訂單號碼：</strong> {{ order_number }}<br/>
              <strong>原預計到貨時間：</strong> {{ original_delivery_date }}<br/>
              <strong>新預計到貨時間：</strong> {{ new_delivery_date }}<br/>
              <strong>追蹤號碼：</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          延遲原因：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          追蹤您的訂單
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          我們正在努力盡快將您的訂單送達。當您包裹開始運送時，您將收到另一個更新。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          有問題？<a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">聯繫我們的客服團隊</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
有關您的訂單 #{{ order_number }}

Hi {{ customer_name }},

我們想通知您有關您的訂單的延遲情況。我們對由此帶來的不便表示歉意，並感謝您的耐心等待。

ORDER DETAILS:
- 訂單號碼：{{ order_number }}
- 原預計到貨時間：{{ original_delivery_date }}
- 新預計到貨時間：{{ new_delivery_date }}
- 追蹤號碼：{{ tracking_number }}

REASON FOR DELAY:
{{ delay_reason }}

Track your order: {{ tracking_url }}

我們正在努力盡快將您的訂單送達。當您包裹開始運送時，您將收到另一個更新。

有問題？聯繫我們的客服團隊：{{ support_url }}

---
此更新是針對 {{ shop_name }} 的訂單 #{{ order_number }}。