---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
我們已收到您的退貨 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          退貨已收到
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          訂單 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您好 {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我們已收到您對訂單 <strong>#{{ order_number }}</strong> 的退貨商品。
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>接下來會發生什麼：</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. 我們的團隊將在 2-3 個工作天內檢查退貨商品<br/>
          2. 我們將確認商品處於原始狀態<br/>
          3. 檢查完成後，我們將處理您的退款<br/>
          4. 退款處理完成後，您將收到確認郵件
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          退款將會退還至您原始的付款方式，可能需要 5-10 個工作天才會顯示在您的帳戶中。
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          感謝您的耐心等待！
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
退貨已收到 - 訂單 #{{ order_number }}

您好 {{ customer_name }},

我們已收到您對訂單 #{{ order_number }} 的退貨商品。

接下來會發生什麼：
1. 我們的團隊將在 2-3 個工作天內檢查退貨商品
2. 我們將確認商品處於原始狀態
3. 檢查完成後，我們將處理您的退款
4. 退款處理完成後，您將收到確認郵件

退款將會退還至您原始的付款方式，可能需要 5-10 個工作天才會顯示在您的帳戶中。

感謝您的耐心等待！