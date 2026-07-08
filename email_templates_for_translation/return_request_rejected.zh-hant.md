---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
退貨申請更新 - 訂單 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          退貨申請更新
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
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
          我們已審核您的退貨申請，針對訂單 <strong>#{{ order_number }}</strong>，目前無法批准。
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>原因：</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          如果您對此決定有任何疑問，或認為有錯誤，請聯繫我們的支援團隊。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
退貨申請更新 - 訂單 #{{ order_number }}

Hi {{ customer_name }},

我們已審核您的退貨申請，針對訂單 #{{ order_number }}，目前無法批准。

{% if rejection_reason %}原因： {{ rejection_reason }}{% endif %}

如果您對此決定有任何疑問，或認為有錯誤，請聯繫我們的支援團隊。