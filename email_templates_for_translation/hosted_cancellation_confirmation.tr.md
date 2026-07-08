---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
İptal Onaylandı - {{ store_name }}

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
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          İptal Onaylandı
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Merhaba {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          {{ plan_name }} abonelikiniz iptal edilmiştir.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Sonrasında Ne Olur
        </mj-text>
        <mj-text font-size="14px">
          {{ access_until_date }} tarihine kadar tam erişiminiz devam edecektir.
        </mj-text>
        <mj-text font-size="14px">
          Bunun ardından, mağazanızın verileri {{ termination_date }} tarihine kadar 30 gün boyunca korunacaktır.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Erişim sona ermeden önce verilerinizi dışa aktarmak isterseniz, yönetici panelinizden bunu yapabilirsiniz. Fikrinizi değiştirdiniz mi? Aboneliklerinizi herhangi bir zaman tekrar etkinleştirebilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Abonelikleri Etkinleştir" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
İptal Onaylandı - {{ store_name }}

Merhaba {{ name|default:'there' }},

{{ plan_name }} abonelikiniz iptal edilmiştir.

Sonrasında Ne Olur:
- {{ access_until_date }} tarihine kadar tam erişiminiz devam edecektir.
- Bunun ardından, mağazanızın verileri {{ termination_date }} tarihine kadar 30 gün boyunca korunacaktır.

Erişim sona ermeden önce verilerinizi dışa aktarmak isterseniz, yönetici panelinizden bunu yapabilirsiniz. Fikrinizi değiştirdiniz mi? Aboneliklerinizi herhangi bir zaman tekrar etkinleştirebilirsiniz.

Abonelikleri Etkinleştir: https://spwig.com/account

Yardıma mı ihtiyacınız var? {{ support_email }} adresine ulaşın