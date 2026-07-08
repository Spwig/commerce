---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
Maintenance Renewed - Order #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Maintenance Renewed!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Order #{{ order_number }}
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
          Your Spwig maintenance subscription has been successfully renewed. You'll continue receiving platform updates, security patches, and new features.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Renewal Summary
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          License Key: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Maintenance Valid Until: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Order Number: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          What's Included
        </mj-text>
        <mj-text font-size="14px">
          Your active maintenance gives you access to:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - Platform feature updates and improvements
        </mj-text>
        <mj-text font-size="14px">
          - Security patches and bug fixes
        </mj-text>
        <mj-text font-size="14px">
          - New component releases via the upgrade server
        </mj-text>
        <mj-text font-size="14px">
          - Technical support
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          No action is required on your part. Updates will continue to be available through your admin panel's component update system.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Maintenance Renewed!

Order #{{ order_number }}

Hi {{ customer_name }},

Your Spwig maintenance subscription has been successfully renewed. You'll continue receiving platform updates, security patches, and new features.

Renewal Summary:
- License Key: {{ license_key }}
- Maintenance Valid Until: {{ renewal_expires_at }}
- Order Number: {{ order_number }}

What's Included:
- Platform feature updates and improvements
- Security patches and bug fixes
- New component releases via the upgrade server
- Technical support

No action is required on your part. Updates will continue to be available through your admin panel's component update system.

Need help? Contact {{ support_email }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's name | Sarah |
| license_key | The renewed license key | CORE-XXXX-XXXX |
| renewal_expires_at | New maintenance expiry date | 2027-03-12 |
| order_number | Checkout order number | ORD-00042 |
| support_email | Support contact email | support@spwig.com |

## Notes

- Transactional email - sent after successful maintenance renewal payment
- Confirms renewal and reassures the merchant that updates will continue
- Uses green success header to reinforce positive action
- No CTA button needed - merchant's admin panel handles updates automatically
