---
template_type: loyalty_tier_upgrade
category: Loyalty Program
---

# Email Template: loyalty_tier_upgrade

## Subject
Congratulazioni! Sei stato aggiornato a {{ new_tier }}

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
    <mj-section background-color="{{ theme.color.warning|default:'#f59e0b' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" align="center">
          🎉
        </mj-text>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Tier Upgrade!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tier Display -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ old_tier }} → {{ new_tier }}
        </mj-text>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-top="10px">
          {{ new_tier }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Ciao {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Congratulazioni! La tua fedeltà ha dato i suoi frutti. Sei stato aggiornato a {{ new_tier }}!
        </mj-text>

        <!-- Bonus Points (if any) -->
        {% if bonus_points %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          <strong>🎁 Upgrade Bonus: {{ bonus_points }} punti!</strong>
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          I Tuoi Nuovi Benefici:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ tier_benefits }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ account_url }}">
          Visualizza i miei premi
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Congratulazioni! Sei stato aggiornato a {{ new_tier }}

Ciao {{ customer_name }},

Congratulazioni! La tua fedeltà ha dato i suoi frutti. Sei stato aggiornato a {{ new_tier }}!

{{ old_tier }} → {{ new_tier }}

{% if bonus_points %}Upgrade Bonus: {{ bonus_points }} punti!{% endif %}

I Tuoi Nuovi Benefici:
{{ tier_benefits }}

Visualizza i tuoi premi: {{ account_url }}

{{ shop_name }}