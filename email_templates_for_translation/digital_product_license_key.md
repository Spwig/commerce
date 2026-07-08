---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
Your Software License Key - Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Your License Key is Ready
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ customer_name }},
        </mj-text>
        <mj-text>
          Thank you for your purchase of {{ product_name }}! Here is your license key for activation.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          YOUR LICENSE KEY
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Click to copy or write it down carefully
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          License Details:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Product: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Version: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • License Type: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Max Activations: {{ max_activations }} device(s)
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Validity: Lifetime License
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Valid Until: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          How to Activate:
        </mj-text>
        <mj-text font-size="14px">
          1. Download and install the software
        </mj-text>
        <mj-text font-size="14px">
          2. Open the application
        </mj-text>
        <mj-text font-size="14px">
          3. Enter your license key when prompted
        </mj-text>
        <mj-text font-size="14px">
          4. Click "Activate" to complete the process
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Download Software
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ Important:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Keep this email safe - you'll need the license key for reinstallation
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Do not share your license key with others
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • You can deactivate devices from your account dashboard
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Need help with activation? Contact {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Your License Key is Ready

Hi {{ customer_name }},

Thank you for your purchase of {{ product_name }}! Here is your license key for activation.

YOUR LICENSE KEY:
{{ license_key }}

License Details:
• Product: {{ product_name }}
• Version: {{ product_version }}
• License Type: {{ license_type }}
• Max Activations: {{ max_activations }} device(s)
{% if is_lifetime %}• Validity: Lifetime License{% else %}• Valid Until: {{ expiration_date }}{% endif %}

How to Activate:
1. Download and install the software
2. Open the application
3. Enter your license key when prompted
4. Click "Activate" to complete the process

{% if download_url %}Download Software: {{ download_url }}

{% endif %}IMPORTANT:
• Keep this email safe - you'll need the license key for reinstallation
• Do not share your license key with others
• You can deactivate devices from your account dashboard

Need help with activation? Contact {{ support_email }}
