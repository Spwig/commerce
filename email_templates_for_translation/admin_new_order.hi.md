---
template_type: admin_new_order
category: Admin Notifications
---

# Email Template: admin_new_order

## Subject
नई आदेश प्राप्त - आदेश #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold">
          नई आदेश प्राप्त
        </mj-text>
        <mj-text>
          आपके स्टोर पर एक नई आदेश रखी गई है।
        </mj-text>
        <mj-text>
          <strong>आदेश संख्या:</strong> {{ order_number }}
        </mj-text>
        <mj-text>
          <strong>ग्राहक:</strong> {{ customer_name }}
        </mj-text>
        <mj-text>
          <strong>कुल:</strong> {{ order_total }}
        </mj-text>
        <mj-button href="{{ admin_order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          प्रशासन में देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
नई आदेश प्राप्त

आपके स्टोर पर एक नई आदेश रखी गई है।

आदेश संख्या: {{ order_number }}
ग्राहक: {{ customer_name }}
कुल: {{ order_total }}

प्रशासन में देखें: {{ admin_order_url }}