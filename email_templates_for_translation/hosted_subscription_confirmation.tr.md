---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
Abonelik Onaylandı - {{ store_name }}

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Abonelik Onaylandı!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Spwig'a Hoş Geldiniz
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
          Abonelik için teşekkür ederiz! {{ store_name }} için <strong>{{ plan_name }}</strong> planınız onaylandı.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Plan Detayları
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Fatura Aralığı: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tutar: {{ currency }}{{ amount }}{% if intro_period %} (tanıtım fiyatı){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          Tanıtım fiyatı, {{ intro_period }} için geçerlidir. Sonra planınız {{ currency }}{{ full_amount }}/{{ billing_interval }} olarak yenilenir.
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          Mağazanız şu anda kurulumu yapılıyor ve hazır olduğunda başka bir e-posta alacaksınız.
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          Bir sonraki fatura tarihi: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Abonelik Onaylandı!

Merhaba {{ name|default:'there' }},

Abonelik için teşekkür ederiz! {{ store_name }} için {{ plan_name }} planınız onaylandı.

Plan Detayları:
- Plan: {{ plan_name }}
- Fatura Aralığı: {{ billing_interval }}
- Tutar: {{ currency }}{{ amount }}{% if intro_period %} (tanıtım fiyatı){% endif %}
{% if intro_period %}
Bu tanıtım fiyatı {{ intro_period }} için geçerlidir. Sonra planınız {{ currency }}{{ full_amount }}/{{ billing_interval }} olarak yenilenir.
{% endif %}
Mağazanız şu anda kurulumu yapılıyor ve hazır olduğunda başka bir e-posta alacaksınız.

Bir sonraki fatura tarihi: {{ next_billing_date }}

Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin.