---
template_type: subscription_plan_downgraded
category: Subscriptions
---

# Email Template: subscription_plan_downgraded

## Subject
Abonelik planınız {{ new_plan_name }} olarak değiştirildi

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          Plan Changed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Subscription Plan Updated
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Abonelik planınız {{ new_plan_name }} olarak değiştirildi.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Plan Change Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Previous Plan:</strong> {{ old_plan_name }}<br/>
              <strong>New Plan:</strong> {{ new_plan_name }}<br/>
              <strong>Changed On:</strong> {{ downgrade_date }}<br/>
              <strong>Effective:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What Changes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ plan_changes }}
        </mj-text>

        {% if features_lost %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Features No Longer Available:
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ features_lost }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Billing Information:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>New Price:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Effective Date:</strong> {{ effective_date }}<br/>
              <strong>Next Billing Date:</strong> {{ next_billing_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 A credit of {{ credit_amount }} has been applied to your account for the unused portion of your previous plan.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Changed Your Mind?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color_secondary|default:'#6b7280' }}" align="center">
          You can upgrade back to {{ old_plan_name }} at any time.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ upgrade_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Upgrade Plan
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View My Subscription
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
PLAN CHANGED

Subscription Plan Updated

Merhaba {{ customer_name }},

Abonelik planınız {{ new_plan_name }} olarak değiştirildi.

PLAN CHANGE DETAILS:
- Previous Plan: {{ old_plan_name }}
- New Plan: {{ new_plan_name }}
- Changed On: {{ downgrade_date }}
- Effective: {{ effective_date }}

WHAT CHANGES:
{{ plan_changes }}

{% if features_lost %}
FEATURES NO LONGER AVAILABLE:
{{ features_lost }}
{% endif %}

BILLING INFORMATION:
- New Price: {{ new_price }} / {{ billing_period }}
- Effective Date: {{ effective_date }}
- Next Billing Date: {{ next_billing_date }}

{% if credit_applied %}
💰 A credit of {{ credit_amount }} has been applied to your account for the unused portion of your previous plan.
{% endif %}

CHANGED YOUR MIND?
You can upgrade back to {{ old_plan_name }} at any time.

Upgrade plan: {{ upgrade_url }}
View my subscription: {{ account_url }}