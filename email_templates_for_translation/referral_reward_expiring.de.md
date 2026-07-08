---
template_type: referral_reward_expiring
category: Referral Program
---

# Email Template: referral_reward_expiring

## Subject
Erinnerung: Ihre {{ reward_amount }} Belohnung läuft bald ab

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
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}" align="center">
          ⏰ Belohnung läuft bald ab
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Banner -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="18px" color="#856404" align="center" padding-top="10px">
          läuft in {{ days_until_expiration }} Tagen ab
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center" padding-top="5px">
          Ablaufdatum: {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Hi {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Lassen Sie Ihre {{ reward_amount }} Empfehlungsbelohnung nicht verfallen! Sie läuft in {{ days_until_expiration }} Tagen ab.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Nutzen Sie sie jetzt bei Ihrem nächsten Kauf, bevor es zu spät ist!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Belohnungstyp:</strong> {{ reward_type_display }}<br/>
          <strong>Betrag:</strong> {{ reward_amount }}<br/>
          <strong>Läuft ab:</strong> {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          Jetzt einkaufen
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
Erinnerung: Ihre {{ reward_amount }} Belohnung läuft bald ab

Hi {{ customer_name }},

Lassen Sie Ihre {{ reward_amount }} Empfehlungsbelohnung nicht verfallen! Sie läuft in {{ days_until_expiration }} Tagen ab.

Belohnungsdetails:
- Typ: {{ reward_type_display }}
- Betrag: {{ reward_amount }}
- Läuft ab: {{ expiration_date }}

Nutzen Sie sie jetzt bei Ihrem nächsten Kauf, bevor es zu spät ist!

Jetzt einkaufen: {{ shop_url }}

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}