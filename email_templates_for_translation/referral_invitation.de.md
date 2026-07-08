---
template_type: referral_invitation
category: Referral Program
---

# Email Template: referral_invitation

## Subject
{{ referrer_name }} hat Ihnen ein Geschenk gesendet!

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
          🎁 Sie wurden eingeladen!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ referrer_name }} möchte {{ shop_name }} mit Ihnen teilen
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Offer -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          Ihr Willkommensgeschenk abholen
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          Bei Ihrem ersten Kauf
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
          Hallo,
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ referrer_name }} denkt, dass Sie das Einkaufen bei {{ shop_name }} lieben werden. Um Sie willkommen zu heißen, bieten wir Ihnen {{ reward_amount }} Rabatt auf Ihren ersten Kauf!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Klicken Sie einfach auf den untenstehenden Button, um zu beginnen, und Ihr Geschenk wird automatisch auf Ihre erste Bestellung angewendet.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          So funktioniert es
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. Klicken Sie auf den Button, um zu {{ shop_name }} zu gelangen<br/>
          2. Durchsuchen Sie und fügen Sie Artikel zu Ihrem Warenkorb hinzu<br/>
          3. Beenden Sie Ihren Kauf<br/>
          4. Ihr {{ reward_amount }} Geschenk wird automatisch angewendet!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_link }}">
          Mein {{ reward_amount }} Geschenk beanspruchen
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Diese Einladung wurde von {{ referrer_name }} gesendet<br/>
          Fragen? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Support kontaktieren</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ referrer_name }} hat Ihnen ein Geschenk gesendet!

Hallo,

{{ referrer_name }} denkt, dass Sie das Einkaufen bei {{ shop_name }} lieben werden. Um Sie willkommen zu heißen, bieten wir Ihnen {{ reward_amount }} Rabatt auf Ihren ersten Kauf!

{% if personal_message %}"{{ personal_message }}"
- {{ referrer_name }}
{% endif %}

So funktioniert es:
1. Besuchen Sie {{ shop_name }}
2. Durchsuchen Sie und fügen Sie Artikel zu Ihrem Warenkorb hinzu
3. Beenden Sie Ihren Kauf
4. Ihr {{ reward_amount }} Geschenk wird automatisch angewendet!

Ihr Geschenk beanspruchen: {{ referral_link }}

{{ shop_name }}
Diese Einladung wurde von {{ referrer_name }} gesendet
Fragen? Kontaktieren Sie {{ support_email }}