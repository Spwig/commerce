---
template_type: order_confirmation
category: Core E-commerce
---

# Email Template: order_confirmation

## Subject
आर्डर पुष्टि #{{ order_number }} - धन्यवाद!

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
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          आपके आर्डर के लिए धन्यवाद!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          आर्डर #{{ order_number }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ order_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Timeline -->
    {% include 'email_system/mjml_components/order_timeline.mjml' with stages=timeline_stages %}

    <!-- Order Items -->
    {% include 'email_system/mjml_components/order_items_table.mjml' with items=items %}

    <!-- Payment Summary -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        {% include 'email_system/mjml_components/payment_summary.mjml' with subtotal=subtotal shipping=shipping tax=tax total=total %}
      </mj-column>
    </mj-section>

    <!-- Delivery Estimate -->
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          <strong>अनुमानित डिलीवरी:</strong> {{ estimated_delivery_start }} - {{ estimated_delivery_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Shipping Address -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        {% include 'email_system/mjml_components/address_block.mjml' with address=shipping_address title="Shipping Address" %}
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=order_url text="View Order Status" %}

    {% if activation_url %}
    <!-- Guest Account Creation CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          अपना अकाउंट बनाएं
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          अपने आर्डर की ट्रैकिंग करें, अगली बार तेजी से चेकआउट करें, और अपने पसंद को प्रबंधित करें।
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}
    {% endif %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
आपके आर्डर के लिए धन्यवाद!

आर्डर #{{ order_number }}
{{ order_date }}

अनुमानित डिलीवरी: {{ estimated_delivery_start }} - {{ estimated_delivery_end }}

आर्डर आइटम:
{% for item in items %}
- {{ item.name }} (Qty: {{ item.quantity }}) - {{ item.subtotal }}
{% endfor %}

सबटोटल: {{ subtotal }}
शिपिंग: {{ shipping }}
कर: {{ tax }}
कुल: {{ total }}

शिपिंग पता:
{{ shipping_address.full_address }}

आर्डर स्थिति देखें: {{ order_url }}
{% if activation_url %}

अपना अकाउंट बनाएं
अपने आर्डर की ट्रैकिंग करें, अगली बार तेजी से चेकआउट करें, और अपने पसंद को प्रबंधित करें।
अपना अकाउंट बनाएं: {{ activation_url }}
{% endif %}

मदद की आवश्यकता है?
ईमेल: {{ support_email }}
फोन: {{ support_phone }}