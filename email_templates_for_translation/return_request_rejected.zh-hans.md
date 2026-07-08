---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
退货申请更新 - 订单 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          退货申请更新
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
          订单 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我们已审核您的订单 <strong>#{{ order_number }}</strong> 的退货申请，但目前无法批准。
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
          如果您对这一决定有疑问或认为出现了错误，请联系我们的支持团队。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
退货申请更新 - 订单 #{{ order_number }}

你好 {{ customer_name }}，

我们已审核您的订单 #{{ order_number }} 的退货申请，但目前无法批准。

{% if rejection_reason %}原因： {{ rejection_reason }}{% endif %}

如果您对这一决定有疑问或认为出现了错误，请联系我们的支持团队。