---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
Crie sua conta no {{ site_name }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Você foi convidado!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Crie sua conta no {{ site_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Olá {{ customer_name }},
        </mj-text>
        <mj-text>
          Nós notamos que você tem estado comprando conosco como visitante. Crie uma conta completa para desbloquear benefícios como rastreamento de pedidos, checkout mais rápido e ofertas exclusivas.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Seu histórico de compras
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Total de Pedidos: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Total Gasto: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Por que criar uma conta?
        </mj-text>
        <mj-text font-size="14px">
          - Rastreie suas pedidos e veja o histórico de pedidos
        </mj-text>
        <mj-text font-size="14px">
          - Checkout mais rápido com detalhes salvos
        </mj-text>
        <mj-text font-size="14px">
          - Gerencie seus endereços e preferências
        </mj-text>
        <mj-text font-size="14px">
          - Acesse ofertas e promoções exclusivas
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Crie sua conta" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Este link permitirá que você defina uma senha para sua conta. Seu histórico de pedidos existente será preservado.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Você foi convidado a criar sua conta!

Olá {{ customer_name }},

Nós notamos que você tem estado comprando conosco como visitante. Crie uma conta completa para desbloquear benefícios como rastreamento de pedidos, checkout mais rápido e ofertas exclusivas.

Seu histórico de compras:
- Total de Pedidos: {{ total_orders }}
- Total Gasto: {{ total_spent }}

Por que criar uma conta?
- Rastreie suas pedidos e veja o histórico de pedidos
- Checkout mais rápido com detalhes salvos
- Gerencie seus endereços e preferências
- Acesse ofertas e promoções exclusivas

Crie sua conta: {{ activation_url }}

Este link permitirá que você defina uma senha para sua conta. Seu histórico de pedidos existente será preservado.

Precisa de ajuda? Entre em contato com {{ support_email }}