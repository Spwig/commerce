---
template_type: loyalty_welcome
category: Loyalty Program
---

# Email Template: loyalty_welcome

## Subject
Willkommen bei {{ shop_name }} Rewards!

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
          🎉 Willkommen bei Rewards!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Starten Sie mit jedem Kauf Punkte zu sammeln
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
          Willkommen im {{ shop_name }} Rewards-Programm! Sie wurden automatisch angemeldet und können sofort Punkte sammeln.
        </mj-text>

        <!-- Bonus Points (if any) -->
        {% if bonus_points %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          <strong>🎁 Willkommensbonus: {{ bonus_points }} Punkte!</strong>
        </mj-text>
        {% endif %}

        <!-- Current Tier -->
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding="20px 0" />
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Ihr Tier:</strong> {{ current_tier }}
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
          Wie Sie Punkte sammeln können
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Kaufe tätigen - Punkte für jeden Auftrag<br/>
          • Rezensionen schreiben - Teilen Sie Ihre Meinung<br/>
          • Freunde empfehlen - Verbreiten Sie die Nachricht<br/>
          • Geburtstagsbelohnungen - Besondere Punkte an Ihrem Geburtstag
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ account_url }}">
          Meine Belohnungen ansehen
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
Willkommen bei {{ shop_name }} Rewards!

Hi {{ customer_name }},

Willkommen im {{ shop_name }} Rewards-Programm! Sie wurden automatisch angemeldet und können sofort Punkte sammeln.

{% if bonus_points %}Willkommensbonus: {{ bonus_points }} Punkte!{% endif %}

Ihr Tier: {{ current_tier }}
{{ tier_benefits }}

Wie Sie Punkte sammeln können:
- Kaufe tätigen - Punkte für jeden Auftrag
- Rezensionen schreiben - Teilen Sie Ihre Meinung
- Freunde empfehlen - Verbreiten Sie die Nachricht
- Geburtstagsbelohnungen - Besondere Punkte an Ihrem Geburtstag

Meine Belohnungen ansehen: {{ account_url }}

{{ shop_name }}
Fragen? Kontaktieren Sie {{ support_email }}