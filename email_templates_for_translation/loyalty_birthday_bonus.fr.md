---
template_type: loyalty_birthday_bonus
category: Loyalty Program
---

# Email Template: loyalty_birthday_bonus

## Subject
🎂 Bon anniversaire {{ customer_name }} ! Voici un cadeau spécial de {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="32px" align="center">🎂🎉🎁</mj-text>
        <mj-text font-size="26px" font-weight="bold" color="#92400e" align="center">
          Bon anniversaire !
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bon anniversaire, {{ customer_name }} !
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Pour célébrer votre journée spéciale, nous avons ajouté {{ bonus_points }} points bonus à votre compte de fidélité !
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Votre Cadeau d'Anniversaire
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Points
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Ajoutés à votre compte !
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Votre Compte de Fidélité :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Solde des Points :</strong> {{ total_points }} points<br/>
          <strong>Niveau Actuel :</strong> {{ loyalty_tier }}<br/>
          <strong>Bonus d'Anniversaire :</strong> +{{ bonus_points }} points
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Commencer les achats et utiliser vos points
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Bonne anniversaire ! 🎉<br/>
          - L'équipe {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎂🎉🎁 BON ANNIVERSAIRE !

Bon anniversaire, {{ customer_name }} !

Pour célébrer votre journée spéciale, nous avons ajouté {{ bonus_points }} points bonus à votre compte de fidélité !

VOTRE CADEAU D'ANNIVERSAIRE :
{{ bonus_points }} Points
Ajoutés à votre compte !

VOTRE COMPTE DE FIDÉLITÉ :
- Solde des Points : {{ total_points }} points
- Niveau Actuel : {{ loyalty_tier }}
- Bonus d'Anniversaire : +{{ bonus_points }} points

Commencer les achats et utiliser vos points : {{ shop_url }}

Bonne anniversaire ! 🎉
- L'équipe {{ shop_name }}