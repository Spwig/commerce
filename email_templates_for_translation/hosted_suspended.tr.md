---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
Mağaza Askıda - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Hesap Askıda
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
          Ödemeniz yapılmadığı için mağazanız <strong>{{ store_name }}</strong> askıya alındı.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Bu Ne Demek?
        </mj-text>
        <mj-text font-size="14px">
          Mağazanız artık sadece okunabilir modda -- müşteriler ürünleri görebilir ama siparişler devre dışı. Verileriniz güvenli ve 30 gün boyunca korunacak.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          Tam erişimi geri almak için lütfen ödeme yönteminizi güncelleyin ve kalan borcu ödediğinizden emin olun.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Mağazanızı Aktif Et" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Hesap Askıda - {{ store_name }}

Merhaba {{ name|default:'there' }},

Ödemeniz yapılmadığı için mağazanız {{ store_name }} askıya alındı.

Bu Ne Demek?:
Mağazanız artık sadece okunabilir modda -- müşteriler ürünleri görebilir ama siparişler devre dışı. Verileriniz güvenli ve 30 gün boyunca korunacak.

Tam erişimi geri almak için lütfen ödeme yönteminizi güncelleyin ve kalan borcu ödediğinizden emin olun.

Mağazanızı Aktif Et: https://spwig.com/account

Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin