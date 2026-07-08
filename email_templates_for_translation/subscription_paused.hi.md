---
template_type: subscription_paused
category: Subscriptions
---

# Email Template: subscription_paused

## Subject
⏸️ आपका {{ plan_name }} सदस्यता रोक दी गई है - {{ shop_name }}

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
          ⏸️ सदस्यता रोक दी गई है
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          आपका {{ plan_name }} सदस्यता अब रोक दी गई है
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Pause Details Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#fff7ed" padding="30px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#9a3412" align="center" padding-bottom="15px">
                रोक जानकारी
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>योजना:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>रोक दिन:</strong> {{ pause_date|date:"F d, Y" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>स्थिति:</strong> रोक दी गई
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What This Means Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          यह क्या अर्थ है
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.warning|default:'#f59e0b' }}; font-size: 18px; margin-right: 8px;">•</span>
          आपकी सदस्यता भुगतान रोक दिया गया है - आप चुकाने नहीं जा रहे हैं
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.warning|default:'#f59e0b' }}; font-size: 18px; margin-right: 8px;">•</span>
          सदस्यता लाभों के अभिग्रहण की सीमा हो सकती है
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.warning|default:'#f59e0b' }}; font-size: 18px; margin-right: 8px;">•</span>
          आप कभी भी अपनी सदस्यता को जारी रख सकते हैं
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ resume_subscription_url }}" background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          सदस्यता जारी रखें
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ manage_subscription_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: underline;">
            सदस्यता प्रबंधित करें
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
⏸️ सदस्यता रोक दी गई है

आपका {{ plan_name }} सदस्यता अब रोक दी गई है

रोक जानकारी:
योजना: {{ plan_name }}
रोक दिन: {{ pause_date|date:"F d, Y" }}
स्थिति: रोक दी गई

यह क्या अर्थ है:
• आपकी सदस्यता भुगतान रोक दिया गया है - आप चुकाने नहीं जा रहे हैं
• सदस्यता लाभों के अभिग्रहण की सीमा हो सकती है
• आप कभी भी अपनी सदस्यता को जारी रख सकते हैं

सदस्यता जारी रखें: {{ resume_subscription_url }}
सदस्यता प्रबंधित करें: {{ manage_subscription_url }}

सहायता की आवश्यकता है? हमसे संपर्क करें {{ support_email }}

---
Spwig द्वारा संचालित - https://spwig.com