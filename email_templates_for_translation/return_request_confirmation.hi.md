---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
वापसी की अनुरोध प्राप्त - आदेश #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          वापसी की अनुरोध प्राप्त
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
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
          हमने आपके द्वारा आदेश <strong>#{{ order_number }}</strong> के लिए वापसी के अनुरोध को प्राप्त कर लिया है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              वापसी के विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कारण:</strong> {{ return_reason }}<br/>
              <strong>आइटम:</strong> {{ items_count }} आइटम(स)<br/>
              <strong>स्थिति:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अगला क्या होता है?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. हमारी टीम 24-48 घंटों के भीतर आपके वापसी के अनुरोध की जांच करेगी<br/>
          2. एक बार अनुमोदित, हम आपको एक वापसी शिपिंग लेबल ईमेल के माध्यम से भेज देंगे<br/>
          3. आइटम को सुरक्षित ढंग से पैक करें और वापसी लेबल लगाएं<br/>
          4. अपने निकटतम शिपिंग स्थान पर पैकेज छोड़ दें<br/>
          5. हम आइटम प्राप्त और जांच करने के बाद आपके रिफंड को प्रक्रिया में रख देंगे
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          यदि आपके पास कोई प्रश्न है, तो कृपया हमसे संपर्क करने में संकोच न करें।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
वापसी की अनुरोध प्राप्त
आदेश #{{ order_number }}

हेलो {{ customer_name }},

हमने आपके द्वारा आदेश #{{ order_number }} के लिए वापसी के अनुरोध को प्राप्त कर लिया है।

वापसी के विवरण:
- कारण: {{ return_reason }}
- आइटम: {{ items_count }} आइटम(स)
- स्थिति: {{ return_status }}

अगला क्या होता है?
1. हमारी टीम 24-48 घंटों के भीतर आपके वापसी के अनुरोध की जांच करेगी
2. एक बार अनुमोदित, हम आपको एक वापसी शिपिंग लेबल ईमेल के माध्यम से भेज देंगे
3. आइटम को सुरक्षित ढंग से पैक करें और वापसी लेबल लगाएं
4. अपने निकटतम शिपिंग स्थान पर पैकेज छोड़ दें
5. हम आइटम प्राप्त और जांच करने के बाद आपके रिफंड को प्रक्रिया में रख देंगे

यदि आपके पास कोई प्रश्न है, तो कृपया हमसे संपर्क करने में संकोच न करें।