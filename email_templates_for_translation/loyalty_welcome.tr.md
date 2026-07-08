---
template_type: loyalty_welcome
category: Loyalty Program
---

# Email Template: loyalty_welcome

## Subject
🎉 {{ shop_name }} Ödüllere Hoş Geldiniz!

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
          🎉 {{ shop_name }} Ödüllere Hoş Geldiniz!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Her alışverişle puan kazanmaya başlayın
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Merhaba {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ shop_name }} Ödülleri programına hoş geldiniz! Otomatik olarak kaydoldunuz ve hemen puan kazanmaya başlayabilirsiniz.
        </mj-text>

        <!-- Bonus Points (if any) -->
        {% if bonus_points %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          <strong>🎁 Hoş Geldiniz Bonusu: {{ bonus_points }} puan!</strong>
        </mj-text>
        {% endif %}

        <!-- Current Tier -->
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding="20px 0" />
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Sınıflamanız:</strong> {{ current_tier }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          {{ tier_benefits }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Puan Kazanma Şekli
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Alışveriş yapın - Her siparişte puan kazanın<br/>
          • Değerlendirme yazın - Geri bildirim verin<br/>
          • Arkadaşlarınızı davet edin - Kelimeyi yayın<br/>
          • Doğum günündeki ödüller - Doğum gününüzde özel puanlar
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ account_url }}">
          Ödülleri Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Sorularınız varsa? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Destek ile iletişime geçin</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ shop_name }} Ödüllere Hoş Geldiniz!

Merhaba {{ customer_name }},

{{ shop_name }} Ödülleri programına hoş geldiniz! Otomatik olarak kaydoldunuz ve hemen puan kazanmaya başlayabilirsiniz.

{% if bonus_points %}Hoş Geldiniz Bonusu: {{ bonus_points }} puan!{% endif %}

Sınıflamanız: {{ current_tier }}
{{ tier_benefits }}

Puan Kazanma Şekli:
- Alışveriş yapın - Her siparişte puan kazanın
- Değerlendirme yazın - Geri bildirim verin
- Arkadaşlarınızı davet edin - Kelimeyi yayın
- Doğum günündeki ödüller - Doğum gününüzde özel puanlar

Ödülleri Görüntüle: {{ account_url }}

{{ shop_name }}
Sorularınız varsa? {{ support_email }}