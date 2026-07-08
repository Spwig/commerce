---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
您的退貨已核准 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          退貨核准
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          訂單 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您的退貨申請針對訂單 <strong>#{{ order_number }}</strong> 已核准。
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>下一步：</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. 下載並列印下方的退貨標籤<br/>
          2. 如果可能，請將商品安全地包裝在原始包裝中<br/>
          3. 將退貨標籤貼在包裹的外側<br/>
          4. 前往最近的運輸點交寄
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          下載退貨標籤
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>退貨追蹤號碼：</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>重要：</strong> 請在 7 天內寄出退貨，以確保退款能及時處理。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          一旦我們收到並檢查您的退貨，我們將將退款處理至原始付款方式。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
退貨核准 - 訂單 #{{ order_number }}

您好 {{ customer_name }}，

您的退貨申請針對訂單 #{{ order_number }} 已核准。

下一步：
1. 下載並列印退貨標籤
2. 如果可能，請將商品安全地包裝在原始包裝中
3. 將退貨標籤貼在包裹的外側
4. 前往最近的運輸點交寄

{% if return_label_url %}下載退貨標籤： {{ return_label_url }}{% endif %}
{% if return_tracking_number %}退貨追蹤號碼： {{ return_tracking_number }}{% endif %}

重要：請在 7 天內寄出退貨，以確保退款能及時處理。

一旦我們收到並檢查您的退貨，我們將將退款處理至原始付款方式。