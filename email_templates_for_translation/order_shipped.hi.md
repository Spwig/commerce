---
template_type: order_shipped
category: Core E-commerce
---

# Email Template: order_shipped

## Subject
आपका आर्डर #{{ order_number }} भेज दिया गया है!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          📦 आर्डर भेज दिया गया!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          रास्ते में है!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          अच्छी खबर! आपका आर्डर भेज दिया गया है और आपके पास रास्ते में है।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              शिपिंग विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>आर्डर #:</strong> {{ order_number }}<br/>
              <strong>ट्रैकिंग #:</strong> {{ tracking_number }}<br/>
              <strong>कैरियर:</strong> {{ carrier_name }}<br/>
              <strong>अनुमानित डिलीवरी:</strong> {{ estimated_delivery }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अपना पैकेट ट्रैक करें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 आर्डर भेज दिया गया!

रास्ते में है!

हेलो {{ customer_name }},

अच्छी खबर! आपका आर्डर भेज दिया गया है और आपके पास रास्ते में है।

शिपिंग विवरण:
- आर्डर #: {{ order_number }}
- ट्रैकिंग #: {{ tracking_number }}
- कैरियर: {{ carrier_name }}
- अनुमानित डिलीवरी: {{ estimated_delivery }}

अपना पैकेट ट्रैक करें: {{ tracking_url }}