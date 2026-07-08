---
template_type: digital_product_license_expired
category: Digital Products
---

# Email Template: digital_product_license_expired

## Subject
Chiave di Licenza Prossima alla Scadenza - {{ product_name }}

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
    <mj-section background-color="{{ theme.color.warning|default:'#f59e0b' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Licenza Prossima alla Scadenza
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Ciao {{ customer_name }},
        </mj-text>
        <mj-text>
          La tua licenza per <strong>{{ product_name }}</strong> scadrà presto.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section background-color="#fffbeb" padding="20px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#92400e">
          <strong>Chiave di Licenza:</strong> {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>Scade:</strong> {{ expiration_date }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>Giorni Rimasti:</strong> {{ days_remaining }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Rinnova la Tua Licenza
        </mj-text>
        <mj-text>
          Continua a godere di {{ product_name }} rinnovando la tua licenza oggi.
        </mj-text>
        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.warning|default:'#f59e0b' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Rinnova Ora
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Hai domande sul rinnovo? Contatta {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Licenza Prossima alla Scadenza

Ciao {{ customer_name }},

La tua licenza per {{ product_name }} scadrà presto.

Dettagli Licenza:
• Chiave di Licenza: {{ license_key }}
• Scade: {{ expiration_date }}
• Giorni Rimasti: {{ days_remaining }}

Rinnova la Tua Licenza:
Continua a godere di {{ product_name }} rinnovando la tua licenza oggi.

Rinnova Ora: {{ renewal_url }}

Hai domande sul rinnovo? Contatta {{ support_email }}