---
template_type: loyalty_tier_demotion_warning
category: Loyalty Program
---

# Email Template: loyalty_tier_demotion_warning

## Subject
⚠️ Ваша текущая {{ current_tier }} статус заканчивается скоро - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Tier Status Expiring
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Don't Lose Your {{ current_tier }} Benefits!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Your {{ current_tier }} tier status will expire on {{ expiry_date }} unless you maintain your activity level.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Current Status:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Current Tier:</strong> {{ current_tier }}<br/>
              <strong>Expires:</strong> {{ expiry_date }} ({{ days_remaining }} days)<br/>
              <strong>Next Tier:</strong> {{ next_tier }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          How to Keep Your {{ current_tier }} Status:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          You need to {{ requirement_type }} before {{ expiry_date }}:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              {{ requirement_description }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              Current: {{ current_progress }} | Needed: {{ required_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Benefits You'll Lose:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% for benefit in tier_benefits %}
          • {{ benefit }}<br/>
          {% endfor %}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Shop Now & Keep Your Status
        </mj-button>

        <mj-spacer height="20px" />

        <mj-button href="{{ shop_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Full Details
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ TIER STATUS EXPIRING

Don't Lose Your {{ current_tier }} Benefits!

Hi {{ customer_name }},

Your {{ current_tier }} tier status will expire on {{ expiry_date }} unless you maintain your activity level.

CURRENT STATUS:
- Current Tier: {{ current_tier }}
- Expires: {{ expiry_date }} ({{ days_remaining }} days)
- Next Tier: {{ next_tier }}

HOW TO KEEP YOUR {{ current_tier }} STATUS:
You need to {{ requirement_type }} before {{ expiry_date }}:

{{ requirement_description }}
Current: {{ current_progress }} | Needed: {{ required_amount }}

BENEFITS YOU'LL LOSE:
{% for benefit in tier_benefits %}
• {{ benefit }}
{% endfor %}

Shop now & keep your status: {{ shop_url }}
View full details: {{ loyalty_dashboard_url }}