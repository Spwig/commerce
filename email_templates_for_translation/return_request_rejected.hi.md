---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
वापसी की अनुमति के अपडेट - आर्डर #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          वापसी की अनुमति के अपडेट
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
          आर्डर #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हमने आपकी आर्डर <strong>#{{ order_number }}</strong> के लिए वापसी की अनुमति के अनुरोध की जांच कर ली है और इस समय इसे अनुमोदित करने में असमर्थ हैं।
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कारण:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          यदि आप इस निर्णय के बारे में प्रश्न करते हैं या त्रुटि के बारे में संदेह करते हैं, तो कृपया हमारी समर्थन टीम से संपर्क करें।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
वापसी की अनुमति के अपडेट - आर्डर #{{ order_number }}

हेलो {{ customer_name }},

हमने आपकी आर्डर #{{ order_number }} के लिए वापसी की अनुमति के अनुरोध की जांच कर ली है और इस समय इसे अनुमोदित करने में असमर्थ हैं।

{% if rejection_reason %}कारण: {{ rejection_reason }}{% endif %}

यदि आप इस निर्णय के बारे में प्रश्न करते हैं या त्रुटि के बारे में संदेह करते हैं, तो कृपया हमारी समर्थन टीम से संपर्क करें।