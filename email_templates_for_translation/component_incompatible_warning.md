---
template_type: component_incompatible_warning
category: Component Updates
---

# Email Template: component_incompatible_warning

## Subject
⚠️ Compatibility Issue: {{ component_name }} and {{ conflicting_component }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Compatibility Warning
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Version Conflict Detected
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          A compatibility issue has been detected between components in your Spwig store.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Conflict Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Component 1:</strong> {{ component_name }} v{{ component_version }}<br/>
              <strong>Component 2:</strong> {{ conflicting_component }} v{{ conflicting_version }}<br/>
              <strong>Detected:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Compatibility Issue:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ incompatibility_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              Potential Impact
            </mj-text>
            <mj-text font-size="14px" color="#991b1b" line-height="1.6">
              {{ impact_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Recommended Action:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_action }}
        </mj-text>

        {% if compatible_versions %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              Compatible Versions
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ compatible_versions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if update_url %}
        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Resolve Conflict
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contact Support
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Your store is still operational, but we recommend resolving this conflict soon.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ COMPATIBILITY WARNING

Version Conflict Detected

A compatibility issue has been detected between components in your Spwig store.

CONFLICT DETAILS:
- Component 1: {{ component_name }} v{{ component_version }}
- Component 2: {{ conflicting_component }} v{{ conflicting_version }}
- Detected: {{ detected_at }}

COMPATIBILITY ISSUE:
{{ incompatibility_description }}

POTENTIAL IMPACT:
{{ impact_description }}

RECOMMENDED ACTION:
{{ recommended_action }}

{% if compatible_versions %}
COMPATIBLE VERSIONS:
{{ compatible_versions }}
{% endif %}

{% if update_url %}Resolve conflict: {{ update_url }}{% endif %}
Contact support: {{ support_url }}

Your store is still operational, but we recommend resolving this conflict soon.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| component_name | First component name | Stripe Payment Gateway |
| component_version | First component version | 2.0.0 |
| conflicting_component | Second component name | Advanced Checkout |
| conflicting_version | Second component version | 3.5.0 |
| detected_at | When conflict detected | February 15, 2026 at 3:45 PM |
| incompatibility_description | What the conflict is | Stripe 2.0 requires Advanced Checkout <3.0 |
| impact_description | What could go wrong | Payment processing may fail for some customers |
| recommended_action | What to do | Downgrade Advanced Checkout to 2.9.x or upgrade Stripe to 2.1+ |
| compatible_versions | Working combinations | Stripe 2.0 + Checkout 2.9.x OR Stripe 2.1+ + Checkout 3.5.0 |
| update_url | Component management page | https://shop.com/en/admin/components |
| support_url | Support contact | https://shop.com/en/support |

## Notes

- Admin notification - compatibility warning
- Sent when version conflict detected
- Store still operational but action recommended
- Provides clear resolution path
- Lists compatible version combinations
- Medium priority
