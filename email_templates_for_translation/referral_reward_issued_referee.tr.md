---
template_type: referral_reward_issued_referee
category: Referral Program
---

# Email Template: referral_reward_issued_referee

## Subject
Hoş geldiniz! Burada {{ reward_amount }} ödülünüz var

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎁 Hoş geldiniz Hediyesi!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Bize katılmak için teşekkür ederiz
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Display -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          🎉 Hoş geldiniz Ödülünüz
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          {{ reward_type_display }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="13px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="5px">
          Bitiş: {{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Merhaba {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ shop_name }}'a hoş geldiniz! {{ referrer_name }} sizi önerdi ve bir {{ reward_amount }} hoş geldiniz ödülü ile teşekkür etmek istedik.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Ödülünüz hesabınıza eklendi ve bir sonraki alışverişinizde kullanmaya hazırsınız!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Use -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          Ödülünüzü Nasıl Kullanabilirsiniz
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. Ürünlerimizi inceleyin ve sepetinize ürün ekleyin<br/>
          2. Ödeme adımına geçin<br/>
          3. Ödülünüz otomatik olarak uygulanacaktır<br/>
          4. Tasarrufunuzu keyifli şekilde kullanın!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          Alışverişe Başla
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Share and Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          Ödül Kazanmak İçin Size de Şansınız Var!
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Arkadaşlarınıza kendi referans linkinizi paylaşın ve onların ilk alışverişinde ödüller kazanın.
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ my_referral_link_url }}">
          Referans Linkimi Al
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Sorularınız var mı? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Destek ile iletişime geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Hoş geldiniz! Burada {{ reward_amount }} ödülünüz var

Merhaba {{ customer_name }},

{{ shop_name }}'a hoş geldiniz! {{ referrer_name }} sizi önerdi ve bir {{ reward_amount }} hoş geldiniz ödülü ile teşekkür etmek istedik.

Ödülünüz: {{ reward_amount }}
Tip: {{ reward_type_display }}
{% if expires_at %}Bitiş: {{ expires_at }}{% endif %}

Ödülünüzü Nasıl Kullanabilirsiniz:
1. Ürünlerimizi inceleyin ve sepetinize ürün ekleyin
2. Ödeme adımına geçin
3. Ödülünüz otomatik olarak uygulanacaktır
4. Tasarrufunuzu keyifli şekilde kullanın!

Alışverişe Başla: {{ shop_url }}

Ödül Kazanmak İçin Size de Şansınız Var!
Arkadaşlarınıza kendi referans linkinizi paylaşın ve onların ilk alışverişinde ödüller kazanın.
Referans Linkimi Al: {{ my_referral_link_url }}

{{ shop_name }}
Sorularınız var mı? {{ support_email }} ile iletişime geçin