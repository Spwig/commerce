---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
您已被邀请加入 {{ store_name }}

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
          您已被邀请加入 {{ store_name }}
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
          {{ invited_by }} 已邀请您加入 <strong>{{ store_name }}</strong> 作为工作人员。您将能够通过管理员仪表板帮助管理商店。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Accept Invitation" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          此邀请将于 {{ expires_at|date:"N j, Y" }} 过期。如果您未预料到此邀请，可以安全地忽略此电子邮件。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
您已被邀请加入 {{ store_name }}

Hi {{ first_name }},

{{ invited_by }} 已邀请您加入 {{ store_name }} 作为工作人员。您将能够通过管理员仪表板帮助管理商店。

接受邀请：{{ invitation_url }}

此邀请将于 {{ expires_at|date:"N j, Y" }} 过期。如果您未预料到此邀请，可以安全地忽略此电子邮件。

需要帮助？请联系 {{ support_email }}