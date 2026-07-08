---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
Downloadlink abgelaufen - Bestellung #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Downloadlink abgelaufen
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
          Ihr Downloadlink für <strong>{{ product_name }}</strong> aus der Bestellung #{{ order_number }} ist abgelaufen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          Downloadlinks verfallen {{ expiration_days }} Tage nach dem Kauf aus Sicherheitsgründen.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Benötigen Sie einen neuen Downloadlink?
        </mj-text>
        <mj-text>
          Sie können einen neuen Downloadlink anfordern, indem Sie sich in Ihrem Konto anmelden oder unseren Support-Team kontaktieren.
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Zu meinem Konto
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Fragen? Kontaktieren Sie {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Downloadlink abgelaufen

Hi {{ customer_name }},

Ihr Downloadlink für {{ product_name }} aus der Bestellung #{{ order_number }} ist abgelaufen.

Downloadlinks verfallen {{ expiration_days }} Tage nach dem Kauf aus Sicherheitsgründen.

Benötigen Sie einen neuen Downloadlink?
Sie können einen neuen Downloadlink anfordern, indem Sie sich in Ihrem Konto anmelden oder unseren Support-Team kontaktieren.

Zu meinem Konto: {{ account_url }}

Fragen? Kontaktieren Sie {{ support_email }}