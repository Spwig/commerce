---
template_type: digital_product_license_expired
category: Digital Products
---

# Email Template: digital_product_license_expired

## Subject
Chave de Licença Prestes a Expirar - {{ product_name }}

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
          Licença Prestes a Expirar
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Olá {{ customer_name }},
        </mj-text>
        <mj-text>
          Sua licença para <strong>{{ product_name }}</strong> expirará em breve.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section background-color="#fffbeb" padding="20px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#92400e">
          <strong>Chave de Licença:</strong> {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>Expira:</strong> {{ expiration_date }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>Dias Restantes:</strong> {{ days_remaining }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Renove Sua Licença
        </mj-text>
        <mj-text>
          Continue aproveitando {{ product_name }} renovando sua licença hoje.
        </mj-text>
        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.warning|default:'#f59e0b' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Renovar Agora
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Perguntas sobre renovação? Entre em contato com {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Licença Prestes a Expirar

Olá {{ customer_name }},

Sua licença para {{ product_name }} expirará em breve.

Detalhes da Licença:
• Chave de Licença: {{ license_key }}
• Expira: {{ expiration_date }}
• Dias Restantes: {{ days_remaining }}

Renove Sua Licença:
Continue aproveitando {{ product_name }} renovando sua licença hoje.

Renovar Agora: {{ renewal_url }}

Perguntas sobre renovação? Entre em contato com {{ support_email }}