---
template_type: referral_reward_expiring
category: Referral Program
---

# Email Template: referral_reward_expiring

## Subject
Rappel : Votre récompense de {{ reward_amount }} va bientôt expirer

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
          ⏰ Récompense qui va bientôt expirer
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
          expirera dans {{ days_until_expiration }} jours
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center" padding-top="5px">
          Date d'expiration : {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Bonjour {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Ne laissez pas votre récompense de {{ reward_amount }} partir en fumée ! Elle expirera dans {{ days_until_expiration }} jours.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Utilisez-la dès maintenant sur votre prochaine commande avant qu'il ne soit trop tard !
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Type de récompense :</strong> {{ reward_type_display }}<br/>
          <strong>Montant :</strong> {{ reward_amount }}<br/>
          <strong>Expire le :</strong> {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          Magasiner maintenant
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Questions ? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contacter le support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Rappel : Votre récompense de {{ reward_amount }} va bientôt expirer

Bonjour {{ customer_name }},

Ne laissez pas votre récompense de {{ reward_amount }} partir en fumée ! Elle expirera dans {{ days_until_expiration }} jours.

Détails de la récompense :
- Type : {{ reward_type_display }}
- Montant : {{ reward_amount }}
- Expire le : {{ expiration_date }}

Utilisez-la dès maintenant sur votre prochaine commande avant qu'il ne soit trop tard !

Magasiner maintenant : {{ shop_url }}

{{ shop_name }}
Questions ? Contacter {{ support_email }}