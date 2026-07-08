---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
कार्रवाई की आवश्यकता है: भुगतान विफल

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          ⚠️ भुगतान विफल
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          भुगतान ID: {{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          हेलो {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          हमारे द्वारा {{ payout_amount }} के आपके भुगतान के प्रक्रिया करते समय एक समस्या आई।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          यह आमतौर पर गलत भुगतान जानकारी या आपके भुगतान प्रदाता के साथ एक समस्या के कारण होता है।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          कृपया अपने भुगतान जानकारी को अपने अफिलिएट डैशबोर्ड में अपडेट करें और हमारे समर्थन टीम से संपर्क करें ताकि इस समस्या को हल किया जा सके।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          भुगतान जानकारी अपडेट करें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          सहायता की आवश्यकता है? <a href="mailto:{{ support_email }}" style="color: #007bff;">समर्थन से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
कार्रवाई की आवश्यकता है: भुगतान विफल

हेलो {{ affiliate_name }},

हमारे द्वारा {{ payout_amount }} के आपके भुगतान के प्रक्रिया करते समय एक समस्या आई (भुगतान ID: {{ payout_id }}).

यह आमतौर पर गलत भुगतान जानकारी या आपके भुगतान प्रदाता के साथ एक समस्या के कारण होता है।

कृपया अपने भुगतान जानकारी को अपने अफिलिएट डैशबोर्ड में अपडेट करें और हमारे समर्थन टीम से संपर्क करें ताकि इस समस्या को हल किया जा सके।

भुगतान जानकारी अपडेट करें: {{ portal_url }}

{{ shop_name }}
सहायता की आवश्यकता है? समर्थन से संपर्क करें {{ support_email }}