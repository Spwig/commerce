---
template_type: subscription_addon_removed
category: Subscriptions
---

# Email Template: subscription_addon_removed

## Subject
サブスクリプションから {{ addon_name }} が削除されました

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          アドオンの削除
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          アドオンの削除
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ addon_name }} は、あなたの {{ plan_name }} サブスクリプションから削除されました。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              削除の詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>アドオン:</strong> {{ addon_name }}<br/>
              <strong>サブスクリプション:</strong> {{ plan_name }}<br/>
              <strong>削除日:</strong> {{ removed_date }}<br/>
              <strong>適用日:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if access_until %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              アクセス期限: {{ access_until }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ addon_name }} へのアクセスは、現在の請求期間終了まで続きます。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          請求情報:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>以前の合計:</strong> {{ old_total }} / {{ billing_period }}<br/>
              <strong>アドオン価格:</strong> -{{ addon_price }} / {{ billing_period }}<br/>
              <strong>新しい合計:</strong> {{ new_total }} / {{ billing_period }}<br/>
              <strong>適用日:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 このアドオンの未使用分について、{{ credit_amount }} のクレジットがアカウントに適用されました。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if data_retention_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          重要な情報:
        </mj-text>
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ data_retention_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          必要ですか？
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          いつでも {{ addon_name }} をサブスクリプションに戻すことができます。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ addons_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          アドオンを閲覧
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          サブスクリプションを確認
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
アドオンが削除されました

アドオンの削除

こんにちは {{ customer_name }}、

{{ addon_name }} は、あなたの {{ plan_name }} サブスクリプションから削除されました。

削除の詳細:
- アドオン: {{ addon_name }}
- サブスクリプション: {{ plan_name }}
- 削除日: {{ removed_date }}
- 適用日: {{ effective_date }}

{% if access_until %}
アクセス期限 {{ access_until }}:
{{ addon_name }} へのアクセスは、現在の請求期間終了まで続きます。
{% endif %}

請求情報:
- 以前の合計: {{ old_total }} / {{ billing_period }}
- アドオン価格: -{{ addon_price }} / {{ billing_period }}
- 新しい合計: {{ new_total }} / {{ billing_period }}
- 適用日: {{ effective_date }}

{% if credit_applied %}
💰 このアドオンの未使用分について、{{ credit_amount }} のクレジットがアカウントに適用されました。
{% endif %}

{% if data_retention_info %}
重要な情報:
{{ data_retention_info }}
{% endif %}

必要ですか？
いつでも {{ addon_name }} をサブスクリプションに戻すことができます。

アドオンを閲覧: {{ addons_url }}
サブスクリプションを確認: {{ account_url }}