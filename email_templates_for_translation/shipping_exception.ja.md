---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
配送異常 - 注文番号 #{{ order_number }} にご注意ください

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 配送異常
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ご挨拶 {{ customer_name }} 様、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ご注文の配送に異常が発生したことをご報告いたします。この問題をできるだけ早く解決するために取り組んでおります。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              異常の詳細:
            </mj-text>
            <mj-text color="#92400e">
              <strong>異常の種類:</strong> {{ exception_type }}<br/>
              <strong>説明:</strong> {{ exception_description }}<br/>
              <strong>発生日時:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              注文情報:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>注文番号:</strong> {{ order_number }}<br/>
              <strong>追跡番号:</strong> {{ tracking_number }}<br/>
              <strong>配送業者:</strong> {{ carrier_name }}<br/>
              <strong>現在の位置:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          次のステップは?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ 必要なアクション:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          注文の追跡
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          サポートへの連絡
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 配送異常

ご挨拶 {{ customer_name }} 様、

ご注文の配送に異常が発生したことをご報告いたします。この問題をできるだけ早く解決するために取り組んでおります。

異常の詳細:
- 異常の種類: {{ exception_type }}
- 説明: {{ exception_description }}
- 発生日時: {{ exception_date }}

注文情報:
- 注文番号: {{ order_number }}
- 追跡番号: {{ tracking_number }}
- 配送業者: {{ carrier_name }}
- 現在の位置: {{ current_location }}

次のステップは?
{{ resolution_steps }}

{% if action_required %}
⚠️ 必要なアクション:
{{ action_required_description }}
{% endif %}

注文の追跡: {{ tracking_url }}
サポートへの連絡: {{ support_url }}