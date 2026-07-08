---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
{{ store_name }} への招待を受けました

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
          スタッフ招待
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} への招待を受けました
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          こんにちは {{ first_name }}、
        </mj-text>
        <mj-text>
          {{ invited_by }} が、あなたを {{ store_name }} のスタッフとして招待しました。管理ダッシュボードから店舗の管理をお手伝いいただけます。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="招待を受ける" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          この招待は {{ expires_at|date:"N j, Y" }} に期限切れになります。この招待が予期せぬものであれば、このメールを無視しても問題ありません。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
{{ store_name }} への招待を受けました

こんにちは {{ first_name }},

{{ invited_by }} が、あなたを {{ store_name }} のスタッフとして招待しました。管理ダッシュボードから店舗の管理をお手伝いいただけます。

招待を受ける: {{ invitation_url }}

この招待は {{ expires_at|date:"N j, Y" }} に期限切れになります。この招待が予期せぬものであれば、このメールを無視しても問題ありません。

お手伝いが必要ですか？ {{ support_email }} にご連絡ください。