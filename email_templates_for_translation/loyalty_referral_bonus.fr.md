---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 Bonus de points pour avoir recommandé {{ referee_name }} !

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 Bonus de parrainage gagné !
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Merci pour le partage, {{ customer_name }} !
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Grande nouvelle ! {{ referee_name }} vient de rejoindre notre programme de fidélité grâce à votre parrainage, et vous avez gagné des points bonus !
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Vous avez gagné
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} Points
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Pour avoir recommandé {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Votre solde mis à jour :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Points Balance:</strong> {{ total_points }} points<br/>
          <strong>Referral Bonus:</strong> +{{ bonus_points }} points<br/>
          <strong>Friends Referred:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Continuez à partager, continuez à gagner !
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Gagnez {{ points_per_referral }} points pour chaque ami qui rejoint. Aucune limite !
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Partagez votre lien de parrainage
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Commencer à acheter
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 BONUS DE PARRAINAGE GAGNÉ !

Merci pour le partage, {{ customer_name }} !

Grande nouvelle ! {{ referee_name }} vient de rejoindre notre programme de fidélité grâce à votre parrainage, et vous avez gagné des points bonus !

VOUS AVEZ GAGNÉ :
+{{ bonus_points }} Points
Pour avoir recommandé {{ referee_name }}

VOTRE SOLDE MISE À JOUR :
- Points Balance: {{ total_points }} points
- Referral Bonus: +{{ bonus_points }} points
- Friends Referred: {{ total_referrals }}

CONTINUEZ À PARTAGER, CONTINUEZ À GAGNER !
Gagnez {{ points_per_referral }} points pour chaque ami qui rejoint. Aucune limite !

Partagez votre lien de parrainage : {{ referral_url }}
Commencer à acheter : {{ shop_url }}