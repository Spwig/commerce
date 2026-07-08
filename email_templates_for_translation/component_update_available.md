---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
Update Available: {{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 Update Available
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          New Version Available
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          A new version of {{ component_name }} is available for your Spwig store.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Update Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Component:</strong> {{ component_name }}<br/>
              <strong>Current Version:</strong> {{ current_version }}<br/>
              <strong>New Version:</strong> {{ new_version }}<br/>
              <strong>Release Date:</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What's New:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Breaking Changes
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Install Update
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">View Full Changelog</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 UPDATE AVAILABLE

New Version Available

A new version of {{ component_name }} is available for your Spwig store.

UPDATE DETAILS:
- Component: {{ component_name }}
- Current Version: {{ current_version }}
- New Version: {{ new_version }}
- Release Date: {{ release_date }}

WHAT'S NEW:
{{ changelog }}

{% if breaking_changes %}
⚠️ BREAKING CHANGES:
{{ breaking_changes }}
{% endif %}

Install update: {{ update_url }}
View full changelog: {{ changelog_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| component_name | Component display name | Stripe Payment Gateway |
| current_version | Currently installed version | 1.2.0 |
| new_version | Available version | 1.3.0 |
| release_date | When released | February 15, 2026 |
| changelog | What's new summary | - Added Apple Pay support\n- Fixed webhook retry logic |
| breaking_changes | Breaking changes notice | Requires PHP 8.1+ |
| update_url | Admin update page | https://shop.com/en/admin/components/updates |
| changelog_url | Full changelog URL | https://spwig.com/components/stripe/changelog |

## Notes

- Admin notification - sent to store administrators
- Triggered by upgrade server version check
- Non-urgent update notification
- Includes changelog and breaking changes warnings
- Links to admin panel for one-click installation
