---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
रिफंड प्रक्रिया में - आदेश #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          रिफंड प्रक्रिया में
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          आदेश #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपके आदेश <strong>#{{ order_number }}</strong> के लौटावट की जांच कर ली गई है और आपका रिफंड प्रक्रिया में है।
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              रिफंड विवरण
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>रिफंड राशि:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>पुनर्वितरण शुल्क:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>नोट:</strong> रिफंड आपके खाते में दिखाई देने में 5-10 व्यावसायिक दिन लग सकते हैं, आपके भुगतान प्रदाता पर निर्भर करते हुए।
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          अगर आपके रिफंड के बारे में कोई प्रश्न है, तो कृपया हमारी समर्थन टीम से संपर्क करें।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
रिफंड प्रक्रिया में - आदेश #{{ order_number }}

हेलो {{ customer_name }},

आपके आदेश #{{ order_number }} के लौटावट की जांच कर ली गई है और आपका रिफंड प्रक्रिया में है।

रिफंड विवरण:
- रिफंड राशि: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- पुनर्वितरण शुल्क: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

नोट: रिफंड आपके खाते में दिखाई देने में 5-10 व्यावसायिक दिन लग सकते हैं, आपके भुगतान प्रदाता पर निर्भर करते हुए।

अगर आपके रिफंड के बारे में कोई प्रश्न है, तो कृपया हमारी समर्थन टीम से संपर्क करें।