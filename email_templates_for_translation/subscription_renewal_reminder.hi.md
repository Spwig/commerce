---
template_type: subscription_renewal_reminder
category: Subscriptions
---

# Email Template: subscription_renewal_reminder

## Subject
🔔 {{ plan_name }} के नवीनीकरण में {{ days_until_renewal }} दिन शेष हैं - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🔔 नवीनीकरण संकेतक
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          आपका सदस्यता जल्दी ही नवीनीकृत होगा
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Info Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#f0f9ff" padding="30px" border="2px solid #0ea5e9" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#0c4a6e" align="center" padding-bottom="15px">
                आगामी शुल्क
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>योजना:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>राशि:</strong> {{ subscription_amount }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>नवीनीकरण तिथि:</strong> {{ next_billing_date|date:"F d, Y" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>भुगतान विधि:</strong> {{ payment_method }}
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- Action Needed Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px" line-height="1.6" align="center">
          कोई कार्रवाई आवश्यक नहीं है। आपकी सदस्यता {{ next_billing_date|date:"F d, Y" }} को स्वचालित रूप से नवीनीकृत होगी।
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding="15px 20px 0 20px" line-height="1.6" align="center">
          अपनी भुगतान विधि अपडेट करना या कोई बदलाव करना है? अपने खाता डैशबोर्ड पर जाएं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ manage_subscription_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          सदस्यता प्रबंधित करें
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ update_payment_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: underline;">
            भुगतान विधि अपडेट करें
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          सहायता की आवश्यकता है? हमसे संपर्क करें {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Spwig द्वारा संचालित
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔔 नवीनीकरण संकेतक

आपका सदस्यता जल्दी ही नवीनीकृत होगा

आगामी शुल्क:
योजना: {{ plan_name }}
राशि: {{ subscription_amount }}
नवीनीकरण तिथि: {{ next_billing_date|date:"F d, Y" }}
भुगतान विधि: {{ payment_method }}

कोई कार्रवाई आवश्यक नहीं है। आपकी सदस्यता {{ next_billing_date|date:"F d, Y" }} को स्वचालित रूप से नवीनीकृत होगी।

अपनी भुगतान विधि अपडेट करना या कोई बदलाव करना है? अपने खाता डैशबोर्ड पर जाएं।

सदस्यता प्रबंधित करें: {{ manage_subscription_url }}
भुगतान विधि अपडेट करें: {{ update_payment_url }}

सहायता की आवश्यकता है? हमसे संपर्क करें {{ support_email }}

---
Spwig द्वारा संचालित - https://spwig.com