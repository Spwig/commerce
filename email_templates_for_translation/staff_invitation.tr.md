---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
{{ store_name }}'e Katılmaya Davet Edildiniz

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
          Personel Davetiyesi
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}'e katılmaya davet edildiniz
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Merhaba {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} sizi {{ store_name }}'e personel olarak katılmaya davet etti. Yönetici panelinden mağazayı yönetmeniz mümkün olacak.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Davetiye Kabul Et" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Bu davetiye {{ expires_at|date:"N j, Y" }} tarihinde sona erecektir. Bu davetiye beklenmedik şekilde alırsanız, bu e-postayı güvenle ihmal edebilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
{{ store_name }}'e Katılmaya Davet Edildiniz

Merhaba {{ first_name }},

{{ invited_by }} sizi {{ store_name }}'e personel olarak katılmaya davet etti. Yönetici panelinden mağazayı yönetmeniz mümkün olacak.

Davetiye Kabul Et: {{ invitation_url }}

Bu davetiye {{ expires_at|date:"N j, Y" }} tarihinde sona erecektir. Bu davetiye beklenmedik şekilde alırsanız, bu e-postayı güvenle ihmal edebilirsiniz.

Yardıma mı ihtiyacınız var? {{ support_email }} adresine ulaşın