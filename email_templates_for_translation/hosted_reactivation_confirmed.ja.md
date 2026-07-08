---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
ようこそ戻り! {{ store_name }} が再びアクティブになりました

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          ようこそ戻り!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} が再びアクティブになりました
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
          グレートニュース！あなたの <strong>{{ store_name }}</strong> ストアが再びアクティブになりました。あなたの <strong>{{ plan_name }}</strong> サブスクリプションが今アクティブになり、ストアがオンラインに戻ってきます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          再アクティブ化の詳細
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          プラン: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          支払い処理済み: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          次回請求日: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          あなたのストアは今すぐオンラインに戻ってきます。すべてが完全に復元されるまで、数分かかる場合があります。オンラインになると、ストアは {{ store_url }} からアクセス可能になります。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
ようこそ戻り! {{ store_name }} が再びアクティブになりました

こんにちは、

グレートニュース！あなたの {{ store_name }} ストアが再びアクティブになりました。あなたの {{ plan_name }} サブスクリプションが今アクティブになり、ストアがオンラインに戻ってきます。

再アクティブ化の詳細:
- プラン: {{ plan_name }}
- 支払い処理済み: {{ currency }}{{ amount }}
- 次回請求日: {{ next_billing_date }}

あなたのストアは今すぐオンラインに戻ってきます。すべてが完全に復元されるまで、数分かかる場合があります。オンラインになると、ストアは {{ store_url }} からアクセス可能になります。

Go to Your Store: {{ admin_url }}

Need help? Contact {{ support_email }}