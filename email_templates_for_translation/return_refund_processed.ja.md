---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
返金処理完了 - 注文 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          返金処理完了
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
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
          注文 <strong>#{{ order_number }}</strong> に関する返品が確認され、返金処理が完了しました。
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              返金の詳細
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>返金額:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>再販売手数料:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>注意:</strong> 返金がアカウントに反映されるまで、5〜10営業日かかる場合があります。これは、お支払いプロバイダーによって異なります。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          返金に関するご質問がございましたら、お気軽にお問い合わせください。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
返金処理完了 - 注文 #{{ order_number }}

こんにちは {{ customer_name }}、

注文 #{{ order_number }} に関する返品が確認され、返金処理が完了しました。

返金の詳細:
- 返金額: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- 再販売手数料: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

注意: 返金がアカウントに反映されるまで、5〜10営業日かかる場合があります。これは、お支払いプロバイダーによって異なります。

返金に関するご質問がございましたら、お気軽にお問い合わせください。