---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
購読が確認されました - {{ store_name }}

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
          購読が確認されました！
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Spwigへようこそ
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
          購読ありがとうございます！{{ store_name }}向けの<strong>{{ plan_name }}</strong>プランが確認されました。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          プランの詳細
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          プラン: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          請求間隔: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          金額: {{ currency }}{{ amount }}{% if intro_period %} (導入価格){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          導入価格は{{ intro_period }}適用されます。その後、プランは{{ currency }}{{ full_amount }}/{{ billing_interval }}で更新されます。
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          あなたのストアの設定が今進行中です。準備が整ったときに、もう1通のメールをお送りします。
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          次の請求日: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
購読が確認されました！

こんにちは {{ name|default:'there' }}、

購読ありがとうございます！{{ store_name }}向けの{{ plan_name }}プランが確認されました。

プランの詳細:
- プラン: {{ plan_name }}
- 請求間隔: {{ billing_interval }}
- 金額: {{ currency }}{{ amount }}{% if intro_period %} (導入価格){% endif %}
{% if intro_period %}
これは{{ intro_period }}の導入価格です。その後、プランは{{ currency }}{{ full_amount }}/{{ billing_interval }}で更新されます。
{% endif %}
あなたのストアの設定が今進行中です。準備が整ったときに、もう1通のメールをお送りします。

次の請求日: {{ next_billing_date }}

お手伝いが必要ですか？{{ support_email }}にご連絡ください。