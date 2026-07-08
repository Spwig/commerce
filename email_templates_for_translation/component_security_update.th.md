---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 การอัปเดตความปลอดภัยที่สำคัญสำหรับ {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 การอัปเดตความปลอดภัยที่จำเป็น
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Critical Security Patch
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          A security vulnerability has been discovered in {{ component_name }}. Please update immediately to protect your store.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Security Information
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Component:</strong> {{ component_name }}<br/>
              <strong>Current Version:</strong> {{ current_version }}<br/>
              <strong>Patched Version:</strong> {{ patched_version }}<br/>
              <strong>Severity:</strong> {{ severity_level }}<br/>
              <strong>CVE ID:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Vulnerability Details:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Potential Impact:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Temporary Mitigation
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Action Required: Install Update Immediately
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Install Security Patch
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Read Security Advisory
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          If you need assistance, contact Spwig support immediately.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 การอัปเดตความปลอดภัยที่จำเป็น

Critical Security Patch

A security vulnerability has been discovered in {{ component_name }}. Please update immediately to protect your store.

⚠️ SECURITY INFORMATION:
- Component: {{ component_name }}
- Current Version: {{ current_version }}
- Patched Version: {{ patched_version }}
- Severity: {{ severity_level }}
- CVE ID: {{ cve_id }}

VULNERABILITY DETAILS:
{{ vulnerability_description }}

POTENTIAL IMPACT:
{{ impact_description }}

{% if mitigation_steps %}
TEMPORARY MITIGATION:
{{ mitigation_steps }}
{% endif %}

ACTION REQUIRED: INSTALL UPDATE IMMEDIATELY

Install security patch: {{ update_url }}
Read security advisory: {{ advisory_url }}

If you need assistance, contact Spwig support immediately.