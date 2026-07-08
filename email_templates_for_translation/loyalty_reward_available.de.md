---
template_type: loyalty_reward_available
category: Loyalty Program
---

# Email Template: loyalty_reward_available

## Subject
Neue Belohnung entriegelt: {{ reward_name }}!

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
          🎁 Belohnung entriegelt!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Display -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          {{ reward_name }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          {{ reward_description }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          {{ points_cost }} Punkte
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
          Große Nachricht! Sie haben nun genügend Punkte, um {{ reward_name }} einzulösen.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Ihr aktueller Saldo: {{ current_points }} Punkte
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ redeem_url }}">
          Jetzt einlösen
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
Neue Belohnung entriegelt: {{ reward_name }}!

Hi {{ customer_name }},

Große Nachricht! Sie haben nun genügend Punkte, um {{ reward_name }} einzulösen.

{{ reward_description }}
Kosten: {{ points_cost }} Punkte

Ihr aktueller Saldo: {{ current_points }} Punkte

Jetzt einlösen: {{ redeem_url }}

{{ shop_name }}