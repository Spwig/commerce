---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
لقد تم دعوك للانضمام إلى {{ store_name }}

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
          دعوة للانضمام إلى الفريق
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          لقد تم دعوك للانضمام إلى {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          مرحبًا {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} قد دعوك للانضمام إلى <strong>{{ store_name }}</strong> كعضو في الفريق. ستتمكن من مساعدة إدارة المتجر من خلال لوحة التحكم الإدارية.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="تقبل الدعوة" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          تنتهي هذه الدعوة في {{ expires_at|date:"N j, Y" }}. إذا لم تتوقع هذه الدعوة، يمكنك تجاهل هذا البريد الإلكتروني بأمان.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
لقد تم دعوك للانضمام إلى {{ store_name }}

مرحبًا {{ first_name }},

{{ invited_by }} قد دعوك للانضمام إلى {{ store_name }} كعضو في الفريق. ستتمكن من مساعدة إدارة المتجر من خلال لوحة التحكم الإدارية.

تقبل دعوتك: {{ invitation_url }}

تنتهي هذه الدعوة في {{ expires_at|date:"N j, Y" }}. إذا لم تتوقع هذه الدعوة، يمكنك تجاهل هذا البريد الإلكتروني بأمان.

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}