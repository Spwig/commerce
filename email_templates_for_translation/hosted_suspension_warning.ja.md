---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
アクションが必要 - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          懸念警告
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} に関するアクションが必要です
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
          {{ plan_name }} のお支払いが期限切れです。{{ grace_end_date }} までに解決しない場合、店舗は読み取り専用モードになります。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          懸念の意味
        </mj-text>
        <mj-text font-size="14px">
          店舗が停止された場合、訪問者は依然としてアクセスできますが、変更は行えません。未払いの残高が清算されるまで、新しい注文は一時停止されます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          店舗の中断を避けるために、お支払い方法を更新してください。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="支払い方法を更新" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Suspension Warning - {{ store_name }}

Hi {{ name|default:'there' }},

Your payment for {{ plan_name }} is overdue. If not resolved by {{ grace_end_date }}, your store will be placed in read-only mode.

What Suspension Means:
If your store is suspended, it will remain visible to visitors but you will not be able to make changes. New orders will be paused until the outstanding balance is settled.

Please update your payment method to avoid any disruption to your store.

Update Payment Method: https://spwig.com/account

Need help? Contact {{ support_email }}