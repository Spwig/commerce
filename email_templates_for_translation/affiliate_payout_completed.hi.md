---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ भुगतान पूरा: {{ payout_amount }}

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
          🎉 भुगतान पूरा हो गया!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ सफलतापूर्वक भुगतान किया गया
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
          हाय {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          आपका भुगतान {{ payout_amount }} सफलतापूर्वक पूरा कर दिया गया है!
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          धनराशि आपके भुगतान विधि के लिए भेज दी गई है। अपने बैंक या भुगतान प्रोसेसर के आधार पर, यह आपके खाते में दिखाई देने में 1-2 व्यावसायिक दिन ले सकता है।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ shop_name }} के विपणन के लिए धन्यवाद। अच्छा काम करते रहिए!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          भुगतान विवरण देखें
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
✓ भुगतान पूरा: {{ payout_amount }}

हाय {{ affiliate_name }},

आपका भुगतान {{ payout_amount }} सफलतापूर्वक पूरा कर दिया गया है!

भुगतान विवरण:
- भुगतान ID: {{ payout_id }}
- राशि: {{ payout_amount }}
- भुगतान विधि: {{ payout_method }}

धनराशि आपके भुगतान विधि के लिए भेज दी गई है। अपने बैंक या भुगतान प्रोसेसर के आधार पर, यह आपके खाते में दिखाई देने में 1-2 व्यावसायिक दिन ले सकता है।

{{ shop_name }} के विपणन के लिए धन्यवाद। अच्छा काम करते रहिए!

भुगतान विवरण देखें: {{ portal_url }}

{{ shop_name }}
सवाल हैं? {{ support_email }} से संपर्क करें