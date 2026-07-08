---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
退貨申請已收到 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          退貨申請已收到
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
          訂單 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我們已收到您針對訂單 <strong>#{{ order_number }}</strong> 的退貨申請。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              退貨詳情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>原因：</strong> {{ return_reason }}<br/>
              <strong>商品：</strong> {{ items_count }} 項<br/>
              <strong>狀態：</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          接下來會發生什麼？
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. 我們的團隊將在 24-48 小時內審核您的退貨申請<br/>
          2. 一旦審核通過，我們將透過電子郵件寄送退貨運送標籤給您<br/>
          3. 將商品安全包裝並附上退貨標籤<br/>
          4. 將包裹寄送到您最近的運輸點<br/>
          5. 一旦我們收到並檢查商品，將為您處理退款
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          如果您有任何問題，請隨時聯繫我們。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
退貨申請已收到
訂單 #{{ order_number }}

Hi {{ customer_name }},

我們已收到您針對訂單 #{{ order_number }} 的退貨申請。

退貨詳情：
- 原因：{{ return_reason }}
- 商品：{{ items_count }} 項
- 狀態：{{ return_status }}

接下來會發生什麼？
1. 我們的團隊將在 24-48 小時內審核您的退貨申請
2. 一旦審核通過，我們將透過電子郵件寄送退貨運送標籤給您
3. 將商品安全包裝並附上退貨標籤
4. 將包裹寄送到您最近的運輸點
5. 一旦我們收到並檢查商品，將為您處理退款

如果您有任何問題，請隨時聯繫我們。