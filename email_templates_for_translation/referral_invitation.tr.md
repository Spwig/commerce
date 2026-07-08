---
template_type: referral_invitation
category: Referral Program
---

# Email Template: referral_invitation

## Subject
{{ referrer_name }} sizi bir hediye ile davet etti!

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
          🎁 Davetiniz Var!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ referrer_name }} sizi {{ shop_name }} ile tanıştırmak istiyor
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Offer -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          Hoş geldiniz hediyesini alın
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          İlk alışverişinizde
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personal Message -->
    {% if personal_message %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" font-style="italic" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.primary|default:'#2563eb' }}">
          "{{ personal_message }}"
          <br/><br/>
          - {{ referrer_name }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Merhaba,
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ referrer_name }} sizi {{ shop_name }} de alışveriş yapmayı çok seveceğinizi düşünüyor. Size hoş geldiniz hediyesi olarak ilk alışverişinizde {{ reward_amount }} indirim sunuyoruz!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Aşağıdaki butona tıklayarak başlayın ve hediye otomatik olarak ilk siparişinize uygulanacaktır.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          Nasıl Çalışır
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. {{ shop_name }}'a gitmek için butona tıklayın<br/>
          2. Ürünleri inceleyin ve sepetinize ekleyin<br/>
          3. Alışverişi tamamlayın<br/>
          4. {{ reward_amount }} hediyeniz otomatik olarak uygulanır!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_link }}">
          {{ reward_amount }} Hediyesini Al
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Bu davet {{ referrer_name }} tarafından gönderildi<br/>
          Sorularınız varsa <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Destek ile iletişime geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ referrer_name }} sizi bir hediye ile davet etti!

Merhaba,

{{ referrer_name }} sizi {{ shop_name }} de alışveriş yapmayı çok seveceğinizi düşünüyor. Size hoş geldiniz hediyesi olarak ilk alışverişinizde {{ reward_amount }} indirim sunuyoruz!

{% if personal_message %}"{{ personal_message }}"
- {{ referrer_name }}
{% endif %}

Nasıl Çalışır:
1. {{ shop_name }}'a git
2. Ürünleri inceleyin ve sepetinize ekleyin
3. Alışverişi tamamlayın
4. {{ reward_amount }} hediyeniz otomatik olarak uygulanır!

Hediyesini al: {{ referral_link }}

{{ shop_name }}
Bu davet {{ referrer_name }} tarafından gönderildi
Sorularınız varsa {{ support_email }} ile iletişime geçin