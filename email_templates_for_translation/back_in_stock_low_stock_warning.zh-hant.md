---
template_type: back_in_stock_low_stock_warning
category: Stock Notifications
---

# Email Template: back_in_stock_low_stock_warning

## Subject
⚠️ {{ product_name }} 重上架了，但銷售情況良好！- {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 限量貨品 - 請立即行動！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }} 重上架了！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          好消息！您一直在等待的貨品已經重新上架了。但請趕快行動 - 我們只剩下 {{ stock_remaining }} 個貨品！
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ product_description }}
            </mj-text>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              型號：{{ variant_name }}
            </mj-text>
            {% endif %}
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ 僅剩 {{ stock_remaining }} 個貨品！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          在貨品售完前立即購買
        </mj-button>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              🔥 <strong>此產品在過去一個月內已售罄 {{ times_sold_out }} 次！</strong><br/>
              再次錯過將會很遺憾 - 請趁還有貨品時立即訂購。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          不再感興趣？<a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">取消訂閱此通知</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 限量貨品 - 請立即行動！

{{ product_name }} 重上架了！

Hi {{ customer_name }},

好消息！您一直在等待的貨品已經重新上架了。但請趕快行動 - 我們只剩下 {{ stock_remaining }} 個貨品！

PRODUCT:
{{ product_name }}
{{ product_description }}
Price: {{ product_price }}
{% if variant_name %}型號：{{ variant_name }}{% endif %}

⚠️ 僅剩 {{ stock_remaining }} 個貨品！

Buy now before it's gone: {{ product_url }}

🔥 此產品在過去一個月內已售罄 {{ times_sold_out }} 次！
Don't miss out again - order now while supplies last.

Not interested anymore? Unsubscribe: {{ unsubscribe_url }}