---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 Low Stock Alert: {{ product_count }} product{{ product_count|pluralize }} running low at {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 Low Inventory Alert
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Stock Running Low
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} product{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} running low at {{ location_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Alert Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Location:</strong> {{ location_name }}<br/>
              <strong>Products Affected:</strong> {{ product_count }}<br/>
              <strong>Detected:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Low Stock Items:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>Variant:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>Current Stock:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>Reorder Point:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Recommended Actions:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Create purchase orders for low stock items<br/>
          • Transfer stock from other locations<br/>
          • Update reorder points if needed<br/>
          • Consider adjusting par levels
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Inventory
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Create Purchase Order
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 LOW INVENTORY ALERT

Stock Running Low

{{ product_count }} product{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} running low at {{ location_name }}.

ALERT DETAILS:
- Location: {{ location_name }}
- Products Affected: {{ product_count }}
- Detected: {{ detected_at }}

LOW STOCK ITEMS:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}Variant: {{ item.variant_name }}{% endif %}
Current Stock: {{ item.current_stock }}
Reorder Point: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

RECOMMENDED ACTIONS:
• Create purchase orders for low stock items
• Transfer stock from other locations
• Update reorder points if needed
• Consider adjusting par levels

View inventory: {{ inventory_url }}
Create purchase order: {{ purchase_orders_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| location_name | Store/warehouse name | Main Store |
| product_count | Number of low stock products | 5 |
| detected_at | When detected | February 15, 2026 at 3:45 PM |
| low_stock_items | Array of low stock products | [{product_name: 'iPhone Case', variant_name: 'Black', current_stock: 2, reorder_point: 10, sku: 'IPH-CASE-BLK'}] |
| inventory_url | Inventory management page | https://shop.com/en/admin/inventory |
| purchase_orders_url | Purchase order creation | https://shop.com/en/admin/purchase-orders/new |

## Notes

- Manager/admin notification
- Sent when product stock drops below reorder point
- Location-specific alert
- Lists all affected products with current quantities
- Actionable recommendations
- Links to inventory management
- Can be configured per-location threshold
