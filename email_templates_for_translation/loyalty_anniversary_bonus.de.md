---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} Jahr{{ years_as_member|pluralize }} bei {{ shop_name }} - Vielen Dank!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} Jahr{{ years_as_member|pluralize }} zusammen!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Heute markiert {{ years_as_member }} Jahr{{ years_as_member|pluralize }} seit Ihrem Beitritt zu unserem Treueprogramm. Vielen Dank, dass Sie ein so wertvoller Mitglied sind!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Jubiläumsbonus
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Punkte
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Hinzugefügt, um {{ years_as_member }} Jahr{{ years_as_member|pluralize }} zu feiern!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ihre {{ years_as_member }}-Jahr-Reise:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          <strong>Seit:</strong> {{ member_since }}<br/>
          <strong>Gesamte Bestellungen:</strong> {{ total_orders }}<br/>
          <strong>Erhaltene Punkte:</strong> {{ lifetime_points }} Punkte<br/>
          <strong>Aktueller Status:</strong> {{ loyalty_tier }}<br/>
          <strong>Gesamte Einsparungen:</strong> {{ total_savings }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Treuekonto ansehen
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Vielen Dank für {{ years_as_member }} unglaubliche Jahr{{ years_as_member|pluralize }}!<br/>
          Auf viele mehr 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} JAHR{{ years_as_member|pluralize|upper }} ZUSAMMEN!

Hi {{ customer_name }},

Heute markiert {{ years_as_member }} Jahr{{ years_as_member|pluralize }} seit Ihrem Beitritt zu unserem Treueprogramm. Vielen Dank, dass Sie ein so wertvoller Mitglied sind!

JUBILÄUMSBONUS:
{{ bonus_points }} Punkte
Hinzugefügt, um {{ years_as_member }} Jahr{{ years_as_member|pluralize }} zu feiern!

IHR {{ years_as_member }}-JAHR-REISE:
- Seit: {{ member_since }}
- Gesamte Bestellungen: {{ total_orders }}
- Erhaltene Punkte: {{ lifetime_points }} Punkte
- Aktueller Status: {{ loyalty_tier }}
- Gesamte Einsparungen: {{ total_savings }}

Treuekonto ansehen: {{ loyalty_dashboard_url }}

Vielen Dank für {{ years_as_member }} unglaubliche Jahr{{ years_as_member|pluralize }}!
Auf viele mehr 🥂

