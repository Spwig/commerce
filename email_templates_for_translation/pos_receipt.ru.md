---
template_type: pos_receipt
category: POS
---

# Email Template: pos_receipt

## Subject
Ваш чек от {{ store_name }} - Заказ #{{ order_number }}

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
          Чек
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column width="50%">
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Номер заказа
        </mj-text>
        <mj-text font-size="14px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="2px">
          #{{ order_number }}
        </mj-text>
      </mj-column>
      <mj-column width="50%">
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="right">
          Дата и время
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
          Обслуживал: {{ cashier_name }}
        </mj-text>
      </mj-column>
      {% endif %}
      {% if terminal_name %}
      <mj-column width="50%">
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="right">
          Терминал: {{ terminal_name }}
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
          ТОВАР
        </mj-text>
      </mj-column>
      <mj-column width="15%">
        <mj-text font-size="12px" font-weight="600" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          КОЛ-ВО
        </mj-text>
      </mj-column>
      <mj-column width="25%">
        <mj-text font-size="12px" font-weight="600" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="right">
          СТОИМОСТЬ
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
          Промежуточно
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
          Скидка
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
          Налог
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
          ИТОГО
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
          ОПЛАТА
        </mj-text>
        {% for payment in payments %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ payment.method }}: {{ payment.amount }}
          {% if payment.card_last4 %}(****{{ payment.card_last4 }}){% endif %}
        </mj-text>
        {% endfor %}
        {% if change_given %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px">
          Сдача: {{ change_given }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    {% if loyalty_points_earned %}
    <!-- Loyalty Points -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="15px 20px">
      <mj-column>
        <mj-text font-size="14px" color="#92400e" align="center">
          <strong>+{{ loyalty_points_earned }} баллов лояльности заработано!</strong>
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Thank You -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Спасибо за покупку!
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
          Посмотреть чек онлайн
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
        ЧЕК
================================

Заказ #{{ order_number }}
Дата: {{ order_date }}
{% if cashier_name %}Обслуживал: {{ cashier_name }}{% endif %}
{% if terminal_name %}Терминал: {{ terminal_name }}{% endif %}

--------------------------------
ТОВАРЫ
--------------------------------
{% for item in items %}
{{ item.name }}
  {{ item.quantity }} x {{ item.unit_price }} = {{ item.line_total }}
{% endfor %}

--------------------------------
Сумма:    {{ subtotal }}
{% if discount_amount %}Скидка:   -{{ discount_amount }}{% endif %}
{% if tax_amount %}Налог:         {{ tax_amount }}{% endif %}
--------------------------------
ИТОГО:       {{ total }}
--------------------------------

ОПЛАТА
{% for payment in payments %}
{{ payment.method }}: {{ payment.amount }}{% if payment.card_last4 %} (****{{ payment.card_last4 }}){% endif %}
{% endfor %}
{% if change_given %}Сдача: {{ change_given }}{% endif %}

{% if loyalty_points_earned %}
+{{ loyalty_points_earned }} баллов лояльности заработано!
{% endif %}

Спасибо за покупку!

{% if return_policy %}{{ return_policy }}{% endif %}

{% if receipt_url %}Посмотреть чек онлайн: {{ receipt_url }}{% endif %}

---
Powered by Spwig - https://spwig.com