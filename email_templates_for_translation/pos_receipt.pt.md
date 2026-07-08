---
template_type: pos_receipt
category: POS
---

# Email Template: pos_receipt

## Subject
Seu recibo da {{ store_name }} - Pedido #{{ order_number }}

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
    <!-- Store Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        {% if store_logo_url %}
        <mj-image src="{{ store_logo_url }}" alt="{{ store_name }}" width="150px" align="center" />
        {% endif %}
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-top="15px">
          {{ store_name }}
        </mj-text>
        {% if store_address %}
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          {{ store_address }}
        </mj-text>
        {% endif %}
        {% if store_phone %}
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ store_phone }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Receipt Title -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="15px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Recibo
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column width="50%">
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Número do Pedido
        </mj-text>
        <mj-text font-size="14px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="2px">
          #{{ order_number }}
        </mj-text>
      </mj-column>
      <mj-column width="50%">
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="right">
          Data e Hora
        </mj-text>
        <mj-text font-size="14px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="2px" align="right">
          {{ order_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    {% if cashier_name or terminal_name %}
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="0 20px 20px 20px">
      {% if cashier_name %}
      <mj-column width="50%">
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Atendido por: {{ cashier_name }}
        </mj-text>
      </mj-column>
      {% endif %}
      {% if terminal_name %}
      <mj-column width="50%">
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="right">
          Terminal: {{ terminal_name }}
        </mj-text>
      </mj-column>
      {% endif %}
    </mj-section>
    {% endif %}

    <!-- Divider -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="0 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" />
      </mj-column>
    </mj-section>

    <!-- Items Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="15px 20px 10px 20px">
      <mj-column width="60%">
        <mj-text font-size="12px" font-weight="600" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          ITEM
        </mj-text>
      </mj-column>
      <mj-column width="15%">
        <mj-text font-size="12px" font-weight="600" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          QTD
        </mj-text>
      </mj-column>
      <mj-column width="25%">
        <mj-text font-size="12px" font-weight="600" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="right">
          PREÇO
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Items -->
    {% for item in items %}
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="8px 20px">
      <mj-column width="60%">
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ item.name }}
          {% if item.sku %}<br/><span style="font-size: 11px; color: #9ca3af;">SKU: {{ item.sku }}</span>{% endif %}
        </mj-text>
      </mj-column>
      <mj-column width="15%">
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ item.quantity }}
        </mj-text>
      </mj-column>
      <mj-column width="25%">
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="right">
          {{ item.line_total }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endfor %}

    <!-- Divider -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" />
      </mj-column>
    </mj-section>

    <!-- Totals -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="5px 20px">
      <mj-column width="70%">
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="right">
          Subtotal
        </mj-text>
      </mj-column>
      <mj-column width="30%">
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="right">
          {{ subtotal }}
        </mj-text>
      </mj-column>
    </mj-section>

    {% if discount_amount %}
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="5px 20px">
      <mj-column width="70%">
        <mj-text font-size="14px" color="{{ theme.color.success|default:'#10b981' }}" align="right">
          Desconto
        </mj-text>
      </mj-column>
      <mj-column width="30%">
        <mj-text font-size="14px" color="{{ theme.color.success|default:'#10b981' }}" align="right">
          -{{ discount_amount }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    {% if tax_amount %}
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="5px 20px">
      <mj-column width="70%">
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="right">
          Imposto
        </mj-text>
      </mj-column>
      <mj-column width="30%">
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="right">
          {{ tax_amount }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column width="70%">
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="right">
          TOTAL
        </mj-text>
      </mj-column>
      <mj-column width="30%">
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="right">
          {{ total }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Methods -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="15px 20px">
      <mj-column>
        <mj-text font-size="12px" font-weight="600" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-bottom="8px">
          PAGAMENTO
        </mj-text>
        {% for payment in payments %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ payment.method }}: {{ payment.amount }}
          {% if payment.card_last4 %}(****{{ payment.card_last4 }}){% endif %}
        </mj-text>
        {% endfor %}
        {% if change_given %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px">
          Troco: {{ change_given }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    {% if loyalty_points_earned %}
    <!-- Loyalty Points -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="15px 20px">
      <mj-column>
        <mj-text font-size="14px" color="#92400e" align="center">
          <strong>+{{ loyalty_points_earned }} pontos de fidelidade conquistados!</strong>
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Thank You -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Obrigado por sua compra!
        </mj-text>
        {% if return_policy %}
        <mj-text font-size="11px" color="#9ca3af" align="center" padding-top="15px">
          {{ return_policy }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- View Online Link -->
    {% if receipt_url %}
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="0 20px 20px 20px">
      <mj-column>
        <mj-button href="{{ receipt_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="14px" border-radius="6px" padding="12px 24px">
          Ver Recibo Online
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Powered by Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ store_name }}
{% if store_address %}{{ store_address }}{% endif %}
{% if store_phone %}{{ store_phone }}{% endif %}

================================
        RECIBO
================================

Pedido #{{ order_number }}
Data: {{ order_date }}
{% if cashier_name %}Atendido por: {{ cashier_name }}{% endif %}
{% if terminal_name %}Terminal: {{ terminal_name }}{% endif %}

--------------------------------
ITENS
--------------------------------
{% for item in items %}
{{ item.name }}
  {{ item.quantity }} x {{ item.unit_price }} = {{ item.line_total }}
{% endfor %}

--------------------------------
Subtotal:    {{ subtotal }}
{% if discount_amount %}Desconto:   -{{ discount_amount }}{% endif %}
{% if tax_amount %}Imposto:         {{ tax_amount }}{% endif %}
--------------------------------
TOTAL:       {{ total }}
--------------------------------

PAGAMENTO
{% for payment in payments %}
{{ payment.method }}: {{ payment.amount }}{% if payment.card_last4 %} (****{{ payment.card_last4 }}){% endif %}
{% endfor %}
{% if change_given %}Troco: {{ change_given }}{% endif %}

{% if loyalty_points_earned %}
+{{ loyalty_points_earned }} pontos de fidelidade conquistados!
{% endif %}

Obrigado por sua compra!

{% if return_policy %}{{ return_policy }}{% endif %}

{% if receipt_url %}Ver seu recibo online: {{ receipt_url }}{% endif %}

---
Powered by Spwig - https://spwig.com