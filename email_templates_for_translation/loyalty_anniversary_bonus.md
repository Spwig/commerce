---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} Year{{ years_as_member|pluralize }} with {{ shop_name }} - Thank You!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} Year{{ years_as_member|pluralize }} Together!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Today marks {{ years_as_member }} year{{ years_as_member|pluralize }} since you joined our loyalty program. Thank you for being such a valued member!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Anniversary Bonus
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Points
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Added to celebrate {{ years_as_member }} year{{ years_as_member|pluralize }}!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Your {{ years_as_member }}-Year Journey:
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
          View Your Loyalty Dashboard
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Thank you for {{ years_as_member }} amazing year{{ years_as_member|pluralize }}!<br/>
          Here's to many more 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} YEAR{{ years_as_member|pluralize|upper }} TOGETHER!

Hi {{ customer_name }},

Today marks {{ years_as_member }} year{{ years_as_member|pluralize }} since you joined our loyalty program. Thank you for being such a valued member!

ANNIVERSARY BONUS:
{{ bonus_points }} Points
Added to celebrate {{ years_as_member }} year{{ years_as_member|pluralize }}!

YOUR {{ years_as_member }}-YEAR JOURNEY:
- Member Since: {{ member_since }}
- Total Orders: {{ total_orders }}
- Points Earned: {{ lifetime_points }} points
- Current Tier: {{ loyalty_tier }}
- Total Savings: {{ total_savings }}

View your loyalty dashboard: {{ loyalty_dashboard_url }}

Thank you for {{ years_as_member }} amazing year{{ years_as_member|pluralize }}!
Here's to many more 🥂

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | Sarah |
| years_as_member | Years in program | 2 |
| bonus_points | Anniversary bonus | 1000 |
| member_since | Join date | February 15, 2024 |
| total_orders | Lifetime orders | 47 |
| lifetime_points | Points ever earned | 12,450 |
| loyalty_tier | Current tier | Gold |
| total_savings | Savings from loyalty | $342.50 |
| loyalty_dashboard_url | Dashboard link | https://shop.com/en/account/loyalty |
| shop_name | Store name | Amazing Shop |

## Notes

- Sent on program membership anniversary
- Shows appreciation and customer value
- Includes impressive stats
- Marketing email - respects preferences
- Bonus points auto-added
