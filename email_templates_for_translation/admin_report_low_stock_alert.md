---
template_type: admin_report_low_stock_alert
category: Admin Reports
---

# Email Template: admin_report_low_stock_alert

## Subject
📦 Low Stock Alert - {{ product_count }} products need reordering

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 Low Stock Alert
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Reorder Needed
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} products are below reorder point.
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Stock:</strong> <span style="color: #dc2626;">{{ item.current_stock }}</span> / Reorder at: {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Inventory
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 LOW STOCK ALERT

Reorder Needed

{{ product_count }} products are below reorder point.

LOW STOCK ITEMS:
{% for item in low_stock_items %}
{{ item.product_name }}
Stock: {{ item.current_stock }} / Reorder at: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

View inventory: {{ inventory_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| product_count | Number of low stock products | 15 |
| low_stock_items | Low stock products array | [{product_name: 'iPhone Case', current_stock: 2, reorder_point: 10, sku: 'IPH-CASE-BLK'}] |
| inventory_url | Inventory page | https://shop.com/en/admin/inventory |

## Notes

- Admin/merchant alert
- Sent when products hit reorder point
- Actionable inventory management
- Can be scheduled (e.g., daily)
