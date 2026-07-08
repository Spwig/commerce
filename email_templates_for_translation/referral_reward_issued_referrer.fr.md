---
template_type: referral_reward_issued_referrer
category: Referral Program
---

# Email Template: referral_reward_issued_referrer

## Subject
🎉 Vous avez gagné une récompense de {{ reward_amount }} !

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
          🎉 Vous avez gagné une récompense !
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Merci d'avoir recommandé {{ referee_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Display -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          🎉 Votre Récompense
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          {{ reward_type_display }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="13px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="5px">
          Expire le : {{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Bonjour {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Félicitations ! {{ referee_name }} vient de passer son premier achat en utilisant votre lien de recommandation, et vous avez gagné une récompense de {{ reward_amount }} !
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Continuez à partager votre lien de recommandation pour gagner plus de récompenses. Plus d'amis vous recommandent, plus vous gagnez !
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Referral Stats -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="20px">
          Vos Statistiques de Références
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="10px 20px 30px 20px">
      <mj-group>
        <mj-column width="50%" background-color="{{ theme.color.background|default:'#ffffff' }}" border-radius="8px" padding="20px 10px">
          <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" line-height="1">
            {{ total_referrals }}
          </mj-text>
          <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="8px" text-transform="uppercase">
            Références Réussies
          </mj-text>
        </mj-column>

        <mj-column width="50%" background-color="{{ theme.color.background|default:'#ffffff' }}" border-radius="8px" padding="20px 10px">
          <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.success|default:'#10b981' }}" align="center" line-height="1">
            {{ total_rewards_earned }}
          </mj-text>
          <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="8px" text-transform="uppercase">
            Récompenses Totales
          </mj-text>
        </mj-column>
      </mj-group>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_dashboard_url }}">
          Voir mes références
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Keep Sharing -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Continuez à partager, continuez à gagner !
        </mj-text>
        <mj-text
          background-color="{{ theme.color.background|default:'#ffffff' }}"
          border="2px dashed {{ theme.color.primary|default:'#2563eb' }}"
          border-radius="8px"
          padding="15px"
          font-size="14px"
          color="{{ theme.color.primary|default:'#2563eb' }}"
          align="center"
          font-family="monospace"
        >
          {{ referral_link }}
        </mj-text>
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Partagez ce lien avec vos amis pour gagner plus de récompenses
        </mj-text>
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
Vous avez gagné une récompense de {{ reward_amount }} !

Bonjour {{ customer_name }},

Félicitations ! {{ referee_name }} vient de passer son premier achat en utilisant votre lien de recommandation, et vous avez gagné une récompense de {{ reward_amount }} !

Votre Récompense : {{ reward_amount }}
Type : {{ reward_type_display }}
{% if expires_at %}Expire le : {{ expires_at }}{% endif %}

Vos Statistiques de Références:
- Références Réussies : {{ total_referrals }}
- Récompenses Totales : {{ total_rewards_earned }}

Continuez à partager votre lien de recommandation pour gagner plus de récompenses:
{{ referral_link }}

Voir vos références : {{ referral_dashboard_url }}

{{ shop_name }}
Questions ? Contacter {{ support_email }}