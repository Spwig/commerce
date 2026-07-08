---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
您已被邀請加入 {{ store_name }}

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
          Staff Invitation
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          您已被邀請加入 {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} has invited you to join <strong>{{ store_name }}</strong> as a staff member. You'll be able to help manage the store from the admin dashboard.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Accept Invitation" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          This invitation expires on {{ expires_at|date:"N j, Y" }}. If you did not expect this invitation, you can safely ignore this email.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
您已被邀請加入 {{ store_name }}

Hi {{ first_name }},

{{ invited_by }} has invited you to join {{ store_name }} as a staff member. You'll be able to help manage the store from the admin dashboard.

Accept your invitation: {{ invitation_url }}

This invitation expires on {{ expires_at|date:"N j, Y" }}. If you did not expect this invitation, you can safely ignore this email.

Need help? Contact {{ support_email }}