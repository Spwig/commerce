---
template_type: license_trial_welcome
category: License
---
 
# Email Template: license_trial_welcome

## Subject
Welcome to Spwig - Your {{ trial_days }}-Day Free Trial

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Welcome to Spwig!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Your {{ trial_days }}-day free trial is ready
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ customer_name }},
        </mj-text>
        <mj-text>
          Thank you for trying <strong>{{ product_name }}</strong>! Your trial has been activated and you have <strong>{{ trial_days }} days</strong> to explore everything Spwig has to offer{% if includes_pos %}, including our Point of Sale system{% endif %}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          YOUR SETUP TOKEN
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Use this token during installation to activate your trial store
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Getting Started
        </mj-text>
        <mj-text font-size="14px">
          1. Follow our setup guide to install Spwig on your server
        </mj-text>
        <mj-text font-size="14px">
          2. Enter your setup token when prompted during installation
        </mj-text>
        <mj-text font-size="14px">
          3. Start building your online store!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          What's Included in Your Trial
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Full access to all core features for {{ trial_days }} days
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Product catalog, orders, and customer management
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Theme customization and page builder
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Payment and shipping provider integrations
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Point of Sale (POS) system
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Your trial will expire in {{ trial_days }} days. When you're ready, upgrade to a full license to keep your store running with no data loss.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Welcome to Spwig!
Your {{ trial_days }}-day free trial is ready.

Hi {{ customer_name }},

Thank you for trying {{ product_name }}! Your trial has been activated and you have {{ trial_days }} days to explore everything Spwig has to offer{% if includes_pos %}, including our Point of Sale system{% endif %}.

YOUR SETUP TOKEN:
{{ setup_token }}
Use this token during installation to activate your trial store.

Getting Started:
1. Follow our setup guide to install Spwig on your server
2. Enter your setup token when prompted during installation
3. Start building your online store!

View Setup Guide: {{ setup_url }}

What's Included in Your Trial:
- Full access to all core features for {{ trial_days }} days
- Product catalog, orders, and customer management
- Theme customization and page builder
- Payment and shipping provider integrations
{% if includes_pos %}- Point of Sale (POS) system{% endif %}

Your trial will expire in {{ trial_days }} days. When you're ready, upgrade to a full license to keep your store running with no data loss.

Need help? Contact {{ support_email }}
