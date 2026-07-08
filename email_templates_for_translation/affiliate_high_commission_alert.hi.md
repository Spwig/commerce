---
template_type: affiliate_high_commission_alert
category: Affiliate Program
---

# Email Template: affiliate_high_commission_alert

## Subject
⚠️ असामान्य कमीशन गतिविधि का पता चला - {{ affiliate_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ उच्च कमीशन चेतावनी
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          असामान्य गतिविधि का पता चला
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          एफिलिएट {{ affiliate_name }} द्वारा असामान्य रूप से उच्च कमीशन कमाया गया। यह धोखाधड़ की रोकथाम के लिए समीक्षा की आवश्यकता है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              चेतावनी विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>एफिलिएट:</strong> {{ affiliate_name }} ({{ affiliate_id }})<br/>
              <strong>कमीशन राशि:</strong> <span style="font-weight: bold; color: #dc2626;">{{ commission_amount }}</span><br/>
              <strong>आदेश मूल्य:</strong> {{ order_value }}<br/>
              <strong>आदेश संख्या:</strong> {{ order_number }}<br/>
              <strong>के द्वारा पता चला:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          क्यों यह चिह्नित किया गया था:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ flag_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सिफारिश की गई कार्रवाई:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • आदेश के विवरण की वैधता की जांच करें<br/>
          • एफिलिएट के संदर्भ इतिहास की जांच करें<br/>
          • ग्राहक की एफिलिएट के साथ संबंध नहीं होना जांचें<br/>
          • प्रशासन पैनल में कमीशन को मंजूरी या अस्वीकृत करें
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_commission_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          कमीशन की समीक्षा
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ affiliate_details_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          एफिलिएट विवरण देखें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          यह कमीशन समीक्षा के लिए अपेक्षा में है और मंजूरी तक भुगतान नहीं किया जाएगा।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ उच्च कमीशन चेतावनी

असामान्य गतिविधि का पता चला

एफिलिएट {{ affiliate_name }} द्वारा असामान्य रूप से उच्च कमीशन कमाया गया। यह धोखाधड़ की रोकथाम के लिए समीक्षा की आवश्यकता है।

चेतावनी विवरण:
- एफिलिएट: {{ affiliate_name }} ({{ affiliate_id }})
- कमीशन राशि: {{ commission_amount }}
- आदेश मूल्य: {{ order_value }}
- आदेश संख्या: {{ order_number }}
- के द्वारा पता चला: {{ detected_at }}

क्यों यह चिह्नित किया गया था:
{{ flag_reason }}

सिफारिश की गई कार्रवाई:
• आदेश के विवरण की वैधता की जांच करें
• एफिलिएट के संदर्भ इतिहास की जांच करें
• ग्राहक की एफिलिएट के साथ संबंध नहीं होना जांचें
• प्रशासन पैनल में कमीशन को मंजूरी या अस्वीकृत करें

कमीशन की समीक्षा: {{ review_commission_url }}
एफिलिएट विवरण देखें: {{ affiliate_details_url }}

यह कमीशन समीक्षा के लिए अपेक्षा में है और मंजूरी तक भुगतान नहीं किया जाएगा।