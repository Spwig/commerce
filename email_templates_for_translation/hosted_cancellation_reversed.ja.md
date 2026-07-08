---
template_type: hosted_cancellation_reversed
category: License
---

# Email Template: hosted_cancellation_reversed

## Subject
キャンセルが取り消されました - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          キャンセルが取り消されました
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          こんにちは、
        </mj-text>
        <mj-text>
          {{ store_name }} のキャンセルリクエストが取り消されました。あなたの <strong>{{ plan_name }}</strong> サブスクリプションは通常通り続きます — あなたのほうで何らかのアクションは必要ありません。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Subscription Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          サブスクリプションの詳細
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          プラン: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          次回請求日: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          あなたのストアは通常通り運営を続けています。上記の日付に請求が再開されます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% if admin_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}
    {% endif %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
キャンセルが取り消されました - {{ store_name }}

こんにちは、

{{ store_name }} のキャンセルリクエストが取り消されました。あなたの {{ plan_name }} サブスクリプションは通常通り続きます — あなたのほうで何らかのアクションは必要ありません。

サブスクリプションの詳細:
- プラン: {{ plan_name }}
- 次回請求日: {{ next_billing_date }}

あなたのストアは通常通り運営を続けています。上記の日付に請求が再開されます。

{% if admin_url %}Go to Your Store: {{ admin_url }}

{% endif %}Need help? Contact {{ support_email }}