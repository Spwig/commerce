---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 आपने न्यूनतम भुगतान थ्रेशहोल्ड प्राप्त कर लिया है!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 भुगतान थ्रेशहोल्ड प्राप्त कर लिया गया!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अच्छी खबर!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हैलो {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          बधाई हो! आपका अफिलिएट बैलेंस न्यूनतम भुगतान थ्रेशहोल्ड तक पहुंच गया है। अब आप भुगतान की अनुमति मांग सकते हैं।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              आपका बैलेंस:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>उपलब्ध बैलेंस:</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>न्यूनतम भुगतान:</strong> {{ minimum_payout }}<br/>
              <strong>लेट बैलेंस:</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अगला कदम:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • अपने अफिलिएट डैशबोर्ड से भुगतान की अनुमति मांगें<br/>
          • भुगतान {{ payout_schedule }} पर प्रोसेस किया जाएगा<br/>
          • राशि {{ payment_method }} के माध्यम से भेजी जाएगी
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          भुगतान की अनुमति मांगें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          डैशबोर्ड देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 भुगतान थ्रेशहोल्ड प्राप्त कर लिया गया!

अच्छी खबर!

हैलो {{ affiliate_name }},

बधाई हो! आपका अफिलिएट बैलेंस न्यूनतम भुगतान थ्रेशहोल्ड तक पहुंच गया है। अब आप भुगतान की अनुमति मांग सकते हैं।

आपका बैलेंस:
- उपलब्ध बैलेंस: {{ available_balance }}
- न्यूनतम भुगतान: {{ minimum_payout }}
- लेट बैलेंस: {{ pending_balance }}

अगला कदम:
• अपने अफिलिएट डैशबोर्ड से भुगतान की अनुमति मांगें
• भुगतान {{ payout_schedule }} पर प्रोसेस किया जाएगा
• राशि {{ payment_method }} के माध्यम से भेजी जाएगी

भुगतान की अनुमति मांगें: {{ request_payout_url }}
डैशबोर्ड देखें: {{ portal_url }}