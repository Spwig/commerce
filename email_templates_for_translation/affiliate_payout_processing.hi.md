---
template_type: affiliate_payout_processing
category: Affiliate Program
---

# Email Template: affiliate_payout_processing

## Subject
आपका {{ payout_amount }} भुगतान प्रक्रिया में है

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
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          💸 भुगतान प्रक्रिया में
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#17a2b8" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          आपका भुगतान प्रक्रिया में है
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
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
          अच्छी खबर! आपके {{ payout_amount }} भुगतान अब प्रक्रिया में है।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          धनराशि आपके खाते में 3-5 व्यावसायिक दिनों के भीतर पहुंच जाएगी। भुगतान पूरा होने पर आपको एक अन्य ईमेल मिलेगा।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>भुगतान ID:</strong> {{ payout_id }}<br/>
          <strong>राशि:</strong> {{ payout_amount }}<br/>
          <strong>भुगतान विधि:</strong> {{ payout_method }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          भुगतान इतिहास देखें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          सवाल हैं? <a href="mailto:{{ support_email }}" style="color: #007bff;">समर्थन से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आपका {{ payout_amount }} भुगतान प्रक्रिया में है

हेलो {{ affiliate_name }},

अच्छी खबर! आपके {{ payout_amount }} भुगतान अब प्रक्रिया में है।

भुगतान विवरण:
- भुगतान ID: {{ payout_id }}
- राशि: {{ payout_amount }}
- भुगतान विधि: {{ payout_method }}

धनराशि आपके खाते में 3-5 व्यावसायिक दिनों के भीतर पहुंच जाएगी। भुगतान पूरा होने पर आपको एक अन्य ईमेल मिलेगा।

भुगतान इतिहास देखें: {{ portal_url }}

{{ shop_name }}
सवाल हैं? {{ support_email }} से संपर्क करें
