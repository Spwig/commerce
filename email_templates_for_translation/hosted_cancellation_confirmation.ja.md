---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
キャンセルが確認されました - {{ store_name }}

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
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          キャンセルが確認されました
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
          こんにちは {{ name|default:'there' }}、
        </mj-text>
        <mj-text>
          あなたの <strong>{{ plan_name }}</strong> サブスクリプションはキャンセルされました。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          次の手順
        </mj-text>
        <mj-text font-size="14px">
          {{ access_until_date }} までフルアクセスが可能です。
        </mj-text>
        <mj-text font-size="14px">
          その後、{{ termination_date }} まで 30 日間、ストアデータが保持されます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          アクセスが終了する前にデータをエクスポートしたい場合は、管理パネルから行うことができます。考えを変更しましたか？いつでもサブスクリプションを再アクティベートできます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="サブスクリプションを再アクティベート" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
キャンセルが確認されました - {{ store_name }}

こんにちは {{ name|default:'there' }},

あなたの {{ plan_name }} サブスクリプションはキャンセルされました。

次の手順:
- {{ access_until_date }} までフルアクセスが可能です。
- その後、{{ termination_date }} まで 30 日間、ストアデータが保持されます。

アクセスが終了する前にデータをエクスポートしたい場合は、管理パネルから行うことができます。考えを変更しましたか？いつでもサブスクリプションを再アクティベートできます。

サブスクリプションを再アクティベート: https://spwig.com/account

お手伝いが必要ですか？{{ support_email }} にご連絡ください