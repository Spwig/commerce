---
template_type: hosted_cancellation_reversed
category: License
---

# Email Template: hosted_cancellation_reversed

## Subject
İptal Geri Alındı - {{ store_name }}

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
          İptal Geri Alındı
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
          Merhaba,
        </mj-text>
        <mj-text>
          {{ store_name }} için iptal talebiniz geri alınmıştır. {{ plan_name }} abonelikiniz normal şekilde devam edecek — sizin tarafınızdan herhangi bir işlem gerekmemektedir.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Subscription Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Abonelik Detayları
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Bir Sonraki Fatura Tarihi: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Mağazanız normal şekilde çalışmaya devam ediyor. Yukarıdaki tarihte faturalandırma yeniden başlayacaktır.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% if admin_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Mağazanıza Git" %}
    {% endif %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
İptal Geri Alındı - {{ store_name }}

Merhaba,

{{ store_name }} için iptal talebiniz geri alınmıştır. {{ plan_name }} abonelikiniz normal şekilde devam edecek — sizin tarafınızdan herhangi bir işlem gerekmemektedir.

Abonelik Detayları:
- Plan: {{ plan_name }}
- Bir Sonraki Fatura Tarihi: {{ next_billing_date }}

Mağazanız normal şekilde çalışmaya devam ediyor. Faturalandırma yukarıdaki tarihte yeniden başlayacaktır.

{% if admin_url %}Mağazanıza Git: {{ admin_url }}

{% endif %}Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin