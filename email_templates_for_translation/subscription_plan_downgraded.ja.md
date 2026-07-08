---
template_type: subscription_plan_downgraded
category: Subscriptions
---

# Email Template: subscription_plan_downgraded

## Subject
ご契約プランが{{ new_plan_name }}に変更されました

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          プラン変更
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ご契約プランが更新されました
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは、{{ customer_name }}さん、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ご契約プランが{{ new_plan_name }}に変更されました。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              プラン変更の詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>前のプラン:</strong> {{ old_plan_name }}<br/>
              <strong>新しいプラン:</strong> {{ new_plan_name }}<br/>
              <strong>変更日:</strong> {{ downgrade_date }}<br/>
              <strong>適用日:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          変更内容:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ plan_changes }}
        </mj-text>

        {% if features_lost %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              今後利用不可になる機能:
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ features_lost }}
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
              <strong>新しい価格:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>適用日:</strong> {{ effective_date }}<br/>
              <strong>次の請求日:</strong> {{ next_billing_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 以前のプランの未使用分に応じて、{{ credit_amount }}のクレジットがアカウントに適用されました。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          ご検討変更ですか？
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color_secondary|default:'#6b7280' }}" align="center">
          いつでも{{ old_plan_name }}へのアップグレードが可能です。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ upgrade_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          プランをアップグレード
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ご契約の確認
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
プラン変更

ご契約プランが更新されました

こんにちは、{{ customer_name }}さん、

ご契約プランが{{ new_plan_name }}に変更されました。

プラン変更の詳細:
- 前のプラン: {{ old_plan_name }}
- 新しいプラン: {{ new_plan_name }}
- 変更日: {{ downgrade_date }}
- 適用日: {{ effective_date }}

変更内容:
{{ plan_changes }}

{% if features_lost %}
今後利用不可になる機能:
{{ features_lost }}
{% endif %}

請求情報:
- 新しい価格: {{ new_price }} / {{ billing_period }}
- 適用日: {{ effective_date }}
- 次の請求日: {{ next_billing_date }}

{% if credit_applied %}
💰 以前のプランの未使用分に応じて、{{ credit_amount }}のクレジットがアカウントに適用されました。
{% endif %}

ご検討変更ですか？
いつでも{{ old_plan_name }}へのアップグレードが可能です。

Upgrade plan: {{ upgrade_url }}
View my subscription: {{ account_url }}