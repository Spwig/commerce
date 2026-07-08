---
template_type: subscription_created
category: Subscriptions
---

# Email Template: subscription_created

## Subject
✅ {{ plan_name }} サブスクリプションが有効になりました - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          ✅ サブスクリプションが有効になりました！
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          {{ plan_name }} へようこそ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Subscription Details Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#f0f9ff" padding="30px" border="2px solid #0ea5e9" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#0c4a6e" align="center" padding-bottom="15px">
                サブスクリプションの詳細
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>プラン:</strong> {{ plan_name }}
              </mj-text>

              {% if product_name %}
              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>製品:</strong> {{ product_name }}
              </mj-text>
              {% endif %}

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>金額:</strong> {{ subscription_amount }} / {{ billing_cycle }}
              </mj-text>

              {% if trial_period %}
              <mj-text font-size="14px" color="{{ theme.color.success|default:'#10b981' }}" padding="5px 0">
                <strong>トライアル期間:</strong> {{ trial_period }} 日 (無料)
              </mj-text>
              <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding="5px 0">
                <strong>初回請求日:</strong> {{ next_billing_date|date:"F d, Y" }}
              </mj-text>
              {% else %}
              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>次回請求日:</strong> {{ next_billing_date|date:"F d, Y" }}
              </mj-text>
              {% endif %}

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>支払い方法:</strong> {{ payment_method }}
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What's Next Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          次のステップは？
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">✓</span>
          サブスクリプションが有効になりました
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">✓</span>
          製品や特典にすぐにアクセスできます
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">✓</span>
          アカウント内からいつでもサブスクリプションを管理できます
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ manage_subscription_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          サブスクリプションを管理する
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          お手伝いが必要ですか？ {{ support_email }} までご連絡ください
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Spwig によって提供されています
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✅ サブスクリプションが有効になりました！

{{ plan_name }} へようこそ

サブスクリプションの詳細:
プラン: {{ plan_name }}
{% if product_name %}製品: {{ product_name }}
{% endif %}金額: {{ subscription_amount }} / {{ billing_cycle }}
{% if trial_period %}トライアル期間: {{ trial_period }} 日 (無料)
初回請求日: {{ next_billing_date|date:"F d, Y" }}
{% else %}次回請求日: {{ next_billing_date|date:"F d, Y" }}
{% endif %}支払い方法: {{ payment_method }}

次のステップは？
✓ サブスクリプションが有効になりました
✓ 製品や特典にすぐにアクセスできます
✓ アカウント内からいつでもサブスクリプションを管理できます

サブスクリプションを管理する: {{ manage_subscription_url }}

お手伝いが必要ですか？ {{ support_email }} までご連絡ください

---
Spwig によって提供されています - https://spwig.com