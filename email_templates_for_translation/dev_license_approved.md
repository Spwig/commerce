---
template_type: dev_license_approved
category: Developer Portal
---

# Email Template: dev_license_approved

## Subject
Your Spwig developer license is ready!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Success Accent -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          License Approved!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          Your development license is ready
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Hi {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          Your developer license request has been approved. You can use this license to run a local Spwig installation for development and testing.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          YOUR LICENSE KEY
        </mj-text>
        <mj-text font-size="18px" font-family="monospace" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding="20px" background-color="{{ theme.color.background|default:'#ffffff' }}" border="2px solid {{ theme.color.success|default:'#10b981' }}">
          {{ license_key }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>License type:</strong> {{ license_type }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Expires:</strong> {{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Important Notice -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.warning|default:'#f59e0b' }}">
          <strong>Important:</strong> This license is for development purposes only. Do not use it for production environments or share it with others.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Go to Dashboard
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Spwig Developer Portal</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Questions? Contact developer support
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>


## Text Content
Hi {{ developer_name }},

Your developer license request has been approved. You can use this license to run a local Spwig installation for development and testing.

YOUR LICENSE KEY:
{{ license_key }}

License type: {{ license_type }}{% if expires_at %}
Expires: {{ expires_at }}{% endif %}

Important: This license is for development purposes only. Do not use it for production environments or share it with others.

Go to Dashboard: {{ dashboard_url }}

---
Spwig Developer Portal
