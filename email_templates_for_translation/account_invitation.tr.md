---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
Hesabınızı {{ site_name }}'de Oluşturun

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
          Davetiniz Var!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ site_name }}'de hesabınızı oluşturun
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Merhaba {{ customer_name }},
        </mj-text>
        <mj-text>
          Bizimle misafir olarak alışveriş yaptığınızı fark ettik. Hesap oluşturarak sipariş takibi, daha hızlı ödeme ve özel teklifler gibi faydaları elde edin.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Alışveriş Geçmişiniz
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Toplam Siparişler: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Toplam Harcama: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Neden Hesap Oluşturmalısınız?
        </mj-text>
        <mj-text font-size="14px">
          - Siparişlerinizi takip edin ve sipariş geçmişinizi görün
        </mj-text>
        <mj-text font-size="14px">
          - Kayıtlı bilgilerle daha hızlı ödeme yapın
        </mj-text>
        <mj-text font-size="14px">
          - Adreslerinizi ve tercihlerinizi yönetin
        </mj-text>
        <mj-text font-size="14px">
          - Özel tekliflere ve kamplara erişin
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Hesabınızı Oluşturun" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Bu bağlantı, hesabınız için bir şifre ayarlamanıza olanak tanır. Mevcut sipariş geçmişiniz korunacaktır.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Hesabınızı Oluşturmak İçin Davetiniz Var!

Merhaba {{ customer_name }},

Bizimle misafir olarak alışveriş yaptığınızı fark ettik. Hesap oluşturarak sipariş takibi, daha hızlı ödeme ve özel teklifler gibi faydaları elde edin.

Alışveriş Geçmişiniz:
- Toplam Siparişler: {{ total_orders }}
- Toplam Harcama: {{ total_spent }}

Neden Hesap Oluşturmalısınız?
- Siparişlerinizi takip edin ve sipariş geçmişinizi görün
- Kayıtlı bilgilerle daha hızlı ödeme yapın
- Adreslerinizi ve tercihlerinizi yönetin
- Özel tekliflere ve kamplara erişin

Hesabınızı Oluşturun: {{ activation_url }}

Bu bağlantı, hesabınız için bir şifre ayarlamanıza olanak tanır. Mevcut sipariş geçmişiniz korunacaktır.

Yardıma mı ihtiyacınız var? {{ support_email }} ile iletişime geçin.