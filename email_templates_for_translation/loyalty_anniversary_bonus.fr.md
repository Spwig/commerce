---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} Année{{ years_as_member|pluralize }} avec {{ shop_name }} - Merci !

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} Année{{ years_as_member|pluralize }} Ensemble !
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Aujourd'hui marque {{ years_as_member }} année{{ years_as_member|pluralize }} depuis que vous avez rejoint notre programme de fidelité. Merci d'être un membre si précieux !
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Bonus d'Anniversaire
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Points
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Ajouté pour célébrer {{ years_as_member }} année{{ years_as_member|pluralize }} !
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Votre Trajet de {{ years_as_member }} Année :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          <strong>Member Since:</strong> {{ member_since }}<br/>
          <strong>Total Orders:</strong> {{ total_orders }}<br/>
          <strong>Points Earned:</strong> {{ lifetime_points }} points<br/>
          <strong>Current Tier:</strong> {{ loyalty_tier }}<br/>
          <strong>Total Savings:</strong> {{ total_savings }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir votre tableau de bord de fidelité
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Merci pour {{ years_as_member }} année{{ years_as_member|pluralize }} incroyables !<br/>
          A la santé de beaucoup plus 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} ANNÉE{{ years_as_member|pluralize|upper }} TOGETHER!

Bonjour {{ customer_name }},

Aujourd'hui marque {{ years_as_member }} année{{ years_as_member|pluralize }} depuis que vous avez rejoint notre programme de fidelité. Merci d'être un membre si précieux !

BONUS D'ANNIVERSAIRE : 
{{ bonus_points }} Points
Ajouté pour célébrer {{ years_as_member }} année{{ years_as_member|pluralize }} !

VOTRE {{ years_as_member }}-ANNÉE JOURNEY:
- Member Since: {{ member_since }}
- Total Orders: {{ total_orders }}
- Points Earned: {{ lifetime_points }} points
- Current Tier: {{ loyalty_tier }}
- Total Savings: {{ total_savings }}

Voir votre tableau de bord de fidelité : {{ loyalty_dashboard_url }}

Merci pour {{ years_as_member }} année{{ years_as_member|pluralize }} incroyables !
A la santé de beaucoup plus 🥂