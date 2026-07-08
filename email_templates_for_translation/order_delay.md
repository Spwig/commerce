---
template_type: order_delay
category: Enhanced E-commerce
---

# Email Template: order_delay

## Subject
Update: Delay for Order #{{ order_number }}

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
          Order Delay Notice
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          Order #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Apology Message -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Dear {{ customer_name }},
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
          <strong>Original Delivery Date:</strong>
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-top="5px">
          <s>{{ original_delivery_date }}</s>
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <strong>New Estimated Delivery:</strong>
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
          Affected Items
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
          As an apology...
        </mj-text>
        <mj-text font-size="14px" color="#155724" align="center" padding-top="10px">
          {{ compensation_details }}
        </mj-text>
        {% if discount_code %}
        <mj-text font-size="18px" font-weight="bold" color="#155724" align="center" padding-top="10px">
          Code: {{ discount_code }}
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
Order Delay Notice

Order #{{ order_number }}

Dear {{ customer_name }},

{{ delay_reason }}

Original Delivery Date: {{ original_delivery_date }}
New Estimated Delivery: {{ new_delivery_date }}

Affected Items:
{% for item in items %}
- {{ item.name }} (Qty: {{ item.quantity }})
{% endfor %}

{% if compensation_offered %}
As an apology...
{{ compensation_details }}
{% if discount_code %}Code: {{ discount_code }}{% endif %}
{% endif %}

View order status: {{ order_url }}

Need Help?
Email: {{ support_email }}
Phone: {{ support_phone }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| order_number | Order number | ORD-2026-001234 |
| customer_name | Customer's first name | Sarah |
| delay_reason | Explanation for delay | Due to unexpected high demand, your order is delayed |
| original_delivery_date | Original estimated delivery | February 18, 2026 |
| new_delivery_date | Updated estimated delivery | February 25, 2026 |
| items | Array of order items | [{name: 'Product Name', quantity: 2, product_thumbnail_url: 'https://...'}] |
| compensation_offered | Boolean - if compensation given | true |
| compensation_details | Compensation description | We're applying a 15% discount to your next order |
| discount_code | Optional discount code | SORRY15 |
| order_url | Order tracking page | https://shop.com/en/orders/ORD-2026-001234 |
| support_email | Support email | support@shop.com |
| support_phone | Support phone | 1-800-555-0123 |

## Notes

- Transactional email - sent when order is delayed
- Proactive customer communication
- Apologetic but reassuring tone
- Optional compensation to maintain goodwill
- Should include clear new delivery date
- May be triggered by supplier delays, shipping issues, or inventory problems
- Important for customer satisfaction and trust
