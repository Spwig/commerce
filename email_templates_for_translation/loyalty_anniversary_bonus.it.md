---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} Anno{{ years_as_member|pluralize }} con {{ shop_name }} - Grazie!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} Anno{{ years_as_member|pluralize }} Insieme!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Oggi segna {{ years_as_member }} anno{{ years_as_member|pluralize }} da quando hai aderito al nostro programma fedeltà. Grazie per essere un membro così apprezzato!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Bonus Anniversario
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Punti
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Aggiunti per celebrare {{ years_as_member }} anno{{ years_as_member|pluralize }}!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Il tuo viaggio di {{ years_as_member }} anni:
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
          Visualizza il tuo pannello fedeltà
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Grazie per {{ years_as_member }} anno{{ years_as_member|pluralize }} eccezionale!<br/>
          A molti altri anni! 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} ANNO{{ years_as_member|pluralize|upper }} INSIEME!

Ciao {{ customer_name }},

Oggi segna {{ years_as_member }} anno{{ years_as_member|pluralize }} da quando hai aderito al nostro programma fedeltà. Grazie per essere un membro così apprezzato!

BONUS ANNIVERSARIO:
{{ bonus_points }} Punti
Aggiunti per celebrare {{ years_as_member }} anno{{ years_as_member|pluralize }}!

IL TUO VIAGGIO DI {{ years_as_member }} ANNI:
- Member Since: {{ member_since }}
- Total Orders: {{ total_orders }}
- Points Earned: {{ lifetime_points }} points
- Current Tier: {{ loyalty_tier }}
- Total Savings: {{ total_savings }}

Visualizza il tuo pannello fedeltà: {{ loyalty_dashboard_url }}

Grazie per {{ years_as_member }} anno{{ years_as_member|pluralize }} eccezionale!
A molti altri anni! 🥂