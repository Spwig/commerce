---
template_type: order_delay
category: Enhanced E-commerce
---

# Email Template: order_delay

## Subject
Atualização: Atraso na Entrega da Encomenda #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#856404" align="center">
          Aviso de Atraso na Entrega
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          Encomenda #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Apology Message -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Caro(a) {{ customer_name }},
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="15px" line-height="1.8">
          {{ delay_reason }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Delivery Date Update -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Data de Entrega Original:</strong>
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-top="5px">
          <s>{{ original_delivery_date }}</s>
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <strong>Nova Data Estimada de Entrega:</strong>
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.primary|default:'#2563eb' }}" font-weight="600" align="center" padding-top="5px">
          {{ new_delivery_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Delayed Items -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          Itens Afetados
        </mj-text>
      </mj-column>
    </mj-section>

    {% for item in items %}
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px">
      <mj-column width="80px">
        <mj-image src="{{ item.product_thumbnail_url }}" alt="{{ item.name }}" width="60px" border-radius="6px" />
      </mj-column>
      <mj-column width="80%" vertical-align="middle">
        <mj-text font-size="14px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ item.name }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Qty: {{ item.quantity }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endfor %}

    <!-- Compensation (if offered) -->
    {% if compensation_offered %}
    <mj-section background-color="#d4edda" padding="20px">
      <mj-column>
        <mj-text font-size="16px" font-weight="600" color="#155724" align="center">
          Como desculpa...
        </mj-text>
        <mj-text font-size="14px" color="#155724" align="center" padding-top="10px">
          {{ compensation_details }}
        </mj-text>
        {% if discount_code %}
        <mj-text font-size="18px" font-weight="bold" color="#155724" align="center" padding-top="10px">
          Código: {{ discount_code }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=order_url text="View Order Status" %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Aviso de Atraso na Entrega

Encomenda #{{ order_number }}

Caro(a) {{ customer_name }},

{{ delay_reason }}

Data de Entrega Original: {{ original_delivery_date }}
Nova Data Estimada de Entrega: {{ new_delivery_date }}

Itens Afetados:
{% for item in items %}
- {{ item.name }} (Qty: {{ item.quantity }})
{% endfor %}

{% if compensation_offered %}
Como desculpa...
{{ compensation_details }}
{% if discount_code %}Código: {{ discount_code }}{% endif %}
{% endif %}

Verificar status da encomenda: {{ order_url }}

Precisa de ajuda?
Email: {{ support_email }}
Telefone: {{ support_phone }}