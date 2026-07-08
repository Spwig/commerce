---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
感謝您的訂單 #{{ order_number }}！- {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 感謝您的訂單！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我們很高興您完成了購買！您的訂單已確認，我們正在為您準備發貨。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              訂單摘要
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>訂單編號：</strong> {{ order_number }}<br/>
              <strong>訂單日期：</strong> {{ order_date }}<br/>
              <strong>總計：</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          跟進您的訂單
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          接下來會發生什麼？
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 我們將為您準備訂單（通常在 1-2 個工作日內）<br/>
          2. 您將收到包含跟進信息的運輸確認<br/>
          3. 您的訂單將送達：{{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>您知道嗎？</strong><br/>
              您可以隨時在您的帳戶儀表板上跟進您的訂單。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          有問題？ <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">聯繫我們的支援團隊</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 感謝您的訂單！

Hi {{ customer_name }},

我們很高興您完成了購買！您的訂單已確認，我們正在為您準備發貨。

ORDER SUMMARY:
- 訂單編號：{{ order_number }}
- 訂單日期：{{ order_date }}
- 總計：{{ order_total }}

跟進您的訂單：{{ order_tracking_url }}

WHAT HAPPENS NEXT?
1. 我們將為您準備訂單（通常在 1-2 個工作日內）
2. 您將收到包含跟進信息的運輸確認
3. 您的訂單將送達：{{ shipping_address }}

💡 您知道嗎？
您可以隨時在您的帳戶儀表板上跟進您的訂單。

有問題？聯繫我們的支援團隊：{{ support_url }}

---
訂單 #{{ order_number }} at {{ shop_name }}