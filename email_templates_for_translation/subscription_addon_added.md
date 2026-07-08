---
template_type: subscription_addon_added
category: Subscriptions
---

# Email Template: subscription_addon_added

## Subject
✓ {{ addon_name }} has been added to your subscription

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ Add-on Activated
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Add-on Added Successfully
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ addon_name }} has been added to your {{ plan_name }} subscription and is now active!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Add-on Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Add-on:</strong> {{ addon_name }}<br/>
              <strong>Subscription:</strong> {{ plan_name }}<br/>
              <strong>Added On:</strong> {{ added_date }}<br/>
              <strong>Status:</strong> Active
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What You Get:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ addon_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Billing Information:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Add-on Price:</strong> {{ addon_price }} / {{ billing_period }}<br/>
              <strong>Your Plan:</strong> {{ plan_price }} / {{ billing_period }}<br/>
              <strong>New Total:</strong> {{ new_total }} / {{ billing_period }}<br/>
              {% if prorated_charge %}<strong>Prorated Charge Today:</strong> {{ prorated_charge }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if prorated_charge %}
        <mj-spacer height="20px" />
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 You were charged {{ prorated_charge }} today for the remainder of your current billing period.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View My Subscription
        </mj-button>

        {% if addon_setup_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ addon_setup_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Configure {{ addon_name }}
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ADD-ON ACTIVATED

Add-on Added Successfully

Hi {{ customer_name }},

{{ addon_name }} has been added to your {{ plan_name }} subscription and is now active!

ADD-ON DETAILS:
- Add-on: {{ addon_name }}
- Subscription: {{ plan_name }}
- Added On: {{ added_date }}
- Status: Active

WHAT YOU GET:
{{ addon_description }}

BILLING INFORMATION:
- Add-on Price: {{ addon_price }} / {{ billing_period }}
- Your Plan: {{ plan_price }} / {{ billing_period }}
- New Total: {{ new_total }} / {{ billing_period }}
{% if prorated_charge %}- Prorated Charge Today: {{ prorated_charge }}{% endif %}

{% if prorated_charge %}
💡 You were charged {{ prorated_charge }} today for the remainder of your current billing period.
{% endif %}

View my subscription: {{ account_url }}
{% if addon_setup_url %}Configure {{ addon_name }}: {{ addon_setup_url }}{% endif %}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's first name | John |
| addon_name | Add-on display name | Extra Storage |
| plan_name | Base subscription plan | Premium Plan |
| added_date | When addon added | February 15, 2026 |
| addon_description | What addon provides | 100GB additional cloud storage for your files |
| addon_price | Add-on price | $9.99 |
| plan_price | Base plan price | $49.99 |
| billing_period | Billing frequency | month |
| new_total | New total price | $59.98 |
| prorated_charge | Prorated amount (if any) | $3.00 |
| account_url | Customer account page | https://shop.com/en/account/subscription |
| addon_setup_url | Optional addon config page | https://shop.com/en/account/storage |

## Notes

- Customer confirmation - addon purchase
- Sent immediately after addon added
- Explains prorated billing if applicable
- Shows new total subscription cost
- May include setup/configuration link
- Positive, welcoming tone
- Transactional email
