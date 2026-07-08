---
template_type: subscription_trial_ending
category: Subscriptions
---

# Email Template: subscription_trial_ending

## Subject
⏰ {{ plan_name }} の無料トライアルが {{ days_remaining }} 日後に終了します - {{ shop_name }}

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
          ⏰ トライアルが間もなく終了します
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          {{ plan_name }} のトライアルは {{ trial_end_date|date:"F d, Y" }} に終了します
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Trial Info Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#fff7ed" padding="30px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="48px" font-weight="bold" color="#ea580c" align="center" padding-bottom="10px">
                {{ days_remaining }}
              </mj-text>
              <mj-text font-size="16px" color="#9a3412" align="center" text-transform="uppercase" letter-spacing="1px">
                残り日数
              </mj-text>

              <mj-divider border-color="#fed7aa" border-width="1px" padding="20px 0" />

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>トライアル終了日:</strong> {{ trial_end_date|date:"F d, Y at g:i A" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>初回請求:</strong> {{ subscription_amount }} が {{ trial_end_date|date:"F d, Y" }} に請求されます
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>支払い方法:</strong> {{ payment_method }}
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What Happens Next -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          次に何が起こるか
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">•</span>
          トライアル終了後、サブスクリプションは自動的に継続されます
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">•</span>
          {{ subscription_amount }} が {{ payment_method }} から請求されます
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">•</span>
          {{ trial_end_date|date:"F d, Y" }} までにいつでもキャンセルできます（料金はかかりません）
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ manage_subscription_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          サブスクリプションを管理
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ cancel_subscription_url }}" style="color: {{ theme.color.error|default:'#ef4444' }}; text-decoration: underline;">
            トライアル終了前にキャンセル
          </a>
        </mj-text>
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
⏰ トライアルが間もなく終了します

{{ plan_name }} のトライアルは {{ trial_end_date|date:"F d, Y" }} に終了します

TRIAL INFO:
{{ days_remaining }} 残り日数

トライアル終了日: {{ trial_end_date|date:"F d, Y at g:i A" }}
初回請求: {{ subscription_amount }} が {{ trial_end_date|date:"F d, Y" }} に請求されます
支払い方法: {{ payment_method }}

次に何が起こるか
• トライアル終了後、サブスクリプションは自動的に継続されます
• {{ subscription_amount }} が {{ payment_method }} から請求されます
• {{ trial_end_date|date:"F d, Y" }} までにいつでもキャンセルできます（料金はかかりません）

サブスクリプションを管理: {{ manage_subscription_url }}
トライアル終了前にキャンセル: {{ cancel_subscription_url }}

お手伝いが必要ですか？ {{ support_email }} までご連絡ください

---
Spwig によって提供されています - https://spwig.com