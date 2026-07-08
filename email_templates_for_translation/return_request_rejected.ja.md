---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
返品依頼の更新 - 注文 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          返品依頼の更新
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
          注文 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          注文 <strong>#{{ order_number }}</strong> に関する返品依頼を確認しましたが、現在のところ承認することはできません。
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>理由:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          この決定について質問がある場合、または誤りがあるとお考えの場合、弊社のサポートチームにお問い合わせください。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
返品依頼の更新 - 注文 #{{ order_number }}

こんにちは {{ customer_name }}、

注文 #{{ order_number }} に関する返品依頼を確認しましたが、現在のところ承認することはできません。

{% if rejection_reason %}理由: {{ rejection_reason }}{% endif %}

この決定について質問がある場合、または誤りがあるとお考えの場合、弊社のサポートチームにお問い合わせください。