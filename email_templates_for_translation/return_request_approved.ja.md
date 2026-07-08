---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
返品が承認されました - 注文 #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          返品が承認されました
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
          注文 <strong>#{{ order_number }}</strong> に関する返品依頼が承認されました。
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>次の手順:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. 下の返品ラベルをダウンロードして印刷してください<br/>
          2. 可能であれば、元の梱包材で商品を安全に梱包してください<br/>
          3. 返品ラベルをパッケージの外側に貼り付けてください<br/>
          4. 最寄りの配送拠点に持ち込んでください
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          返品ラベルをダウンロード
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>返品追跡番号:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>重要:</strong> 返品を7日以内に発送してください。返金の迅速な処理を保証します。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          戻りの受け入れと検査が完了した後、返金は元の支払い方法に処理されます。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
返品が承認されました - 注文 #{{ order_number }}

こんにちは {{ customer_name }}、

注文 #{{ order_number }} に関する返品依頼が承認されました。

次の手順:
1. 返品ラベルをダウンロードして印刷してください
2. 可能であれば、元の梱包材で商品を安全に梱包してください
3. 返品ラベルをパッケージの外側に貼り付けてください
4. 最寄りの配送拠点に持ち込んでください

{% if return_label_url %}返品ラベルをダウンロード: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}返品追跡番号: {{ return_tracking_number }}{% endif %}

重要: 返品を7日以内に発送してください。返金の迅速な処理を保証します。

返品を受け取って検査が完了した後、返金は元の支払い方法に処理されます。