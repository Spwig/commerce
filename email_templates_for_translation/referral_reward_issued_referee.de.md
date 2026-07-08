---
template_type: referral_reward_issued_referee
category: Referral Program
---

# Email Template: referral_reward_issued_referee

## Subject
Willkommen! Hier ist Ihr {{ reward_amount }} Willkommensgeschenk

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
          🎁 Willkommensgeschenk!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Vielen Dank, dass Sie uns beigetreten sind
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Display -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          🎉 Ihr Willkommensgeschenk
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          {{ reward_type_display }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="13px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="5px">
          Ablaufdatum: {{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Hallo {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Willkommen bei {{ shop_name }}! {{ referrer_name }} hat Sie empfohlen, und wir möchten uns mit einem {{ reward_amount }} Willkommensgeschenk bedanken.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Ihr Geschenk wurde Ihrem Konto hinzugefügt und ist für Ihren nächsten Kauf bereit!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Use -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          Wie Sie Ihr Geschenk verwenden können
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. Durchsuchen Sie unsere Produkte und fügen Sie Artikel zu Ihrem Warenkorb hinzu<br/>
          2. Gehen Sie zur Kasse<br/>
          3. Ihr Geschenk wird automatisch angewendet<br/>
          4. Genießen Sie Ihre Ersparnisse!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          Einkaufen starten
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Share and Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          Sie können auch Belohnungen verdienen!
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Teilen Sie Ihren eigenen Empfehlungslink mit Freunden und verdienen Sie Belohnungen, wenn sie ihren ersten Kauf tätigen.
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ my_referral_link_url }}">
          Meinen Empfehlungslink erhalten
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Fragen? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Support kontaktieren</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Willkommen! Hier ist Ihr {{ reward_amount }} Willkommensgeschenk

Hi {{ customer_name }},

Willkommen bei {{ shop_name }}! {{ referrer_name }} hat Sie empfohlen, und wir möchten uns mit einem {{ reward_amount }} Willkommensgeschenk bedanken.

Ihr Geschenk: {{ reward_amount }}
Typ: {{ reward_type_display }}
{% if expires_at %}Ablaufdatum: {{ expires_at }}{% endif %}

Wie Sie Ihr Geschenk verwenden können:
1. Durchsuchen Sie unsere Produkte und fügen Sie Artikel zu Ihrem Warenkorb hinzu
2. Gehen Sie zur Kasse
3. Ihr Geschenk wird automatisch angewendet
4. Genießen Sie Ihre Ersparnisse!

Einkaufen starten: {{ shop_url }}

Sie können auch Belohnungen verdienen!
Teilen Sie Ihren eigenen Empfehlungslink mit Freunden und verdienen Sie Belohnungen, wenn sie ihren ersten Kauf tätigen.
Erhalten Sie Ihren Empfehlungslink: {{ my_referral_link_url }}

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}