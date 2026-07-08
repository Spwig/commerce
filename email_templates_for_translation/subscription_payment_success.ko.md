---
template_type: subscription_payment_success
category: Subscriptions
---

# Email Template: subscription_payment_success

## Subject
✅ {{ plan_name }} 결제 완료 - {{ shop_name }}

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
          ✅ 결제 성공
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          결제 감사합니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#f0fdf4" padding="30px" border="2px solid {{ theme.color.success|default:'#10b981' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#14532d" align="center" padding-bottom="15px">
                결제 영수증
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Plan:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Amount Paid:</strong> {{ amount_paid }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Payment Date:</strong> {{ payment_date|date:"F d, Y" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Payment Method:</strong> {{ payment_method }}
              </mj-text>

              {% if transaction_id %}
              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Transaction ID:</strong> {{ transaction_id }}
              </mj-text>
              {% endif %}

              <mj-divider border-color="#bbf7d0" border-width="1px" padding="15px 0" />

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Next Billing Date:</strong> {{ next_billing_date|date:"F d, Y" }}
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- Thank You Message -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px" line-height="1.6" align="center">
          구독이 계속 활성화되어 있으며, 모든 혜택에 대한 전체적인 접근이 가능합니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ manage_subscription_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          구독 보기
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ download_receipt_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: underline;">
            영수증 다운로드
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          도움이 필요하신가요? {{ support_email }}로 연락주세요
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
            Spwig에서 제공함
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✅ 결제 성공

결제 감사합니다

결제 영수증:
Plan: {{ plan_name }}
Amount Paid: {{ amount_paid }}
Payment Date: {{ payment_date|date:"F d, Y" }}
Payment Method: {{ payment_method }}
{% if transaction_id %}Transaction ID: {{ transaction_id }}
{% endif %}
Next Billing Date: {{ next_billing_date|date:"F d, Y" }}

구독이 계속 활성화되어 있으며, 모든 혜택에 대한 전체적인 접근이 가능합니다.

View Subscription: {{ manage_subscription_url }}
Download Receipt: {{ download_receipt_url }}

도움이 필요하신가요? {{ support_email }}로 연락주세요

---
Spwig에서 제공함 - https://spwig.com