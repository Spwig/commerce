---
template_type: subscription_trial_ending
category: Subscriptions
---

# Email Template: subscription_trial_ending

## Subject
⏰ {{ plan_name }} Deneme Süreniz {{ days_remaining }} Gün Kaldı - {{ shop_name }}

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
          ⏰ Deneme Yakında Bitiyor
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          {{ plan_name }} denemeniz {{ trial_end_date|date:"F d, Y" }} tarihinde sona erecek
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Trial Info Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#fff7ed" padding="30px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="48px" font-weight="bold" color="#ea580c" align="center" padding-bottom="10px">
                {{ days_remaining }}
              </mj-text>
              <mj-text font-size="16px" color="#9a3412" align="center" text-transform="uppercase" letter-spacing="1px">
                Kalan Gün Sayısı
              </mj-text>

              <mj-divider border-color="#fed7aa" border-width="1px" padding="20px 0" />

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Deneme Bitiş Tarihi:</strong> {{ trial_end_date|date:"F d, Y at g:i A" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Birinci Ödeme:</strong> {{ subscription_amount }} {{ trial_end_date|date:"F d, Y" }} tarihinde
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Ödeme Yöntemi:</strong> {{ payment_method }}
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What Happens Next -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Sonrasında Ne Olur?
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">•</span>
          Deneme süresi bittikten sonra abonelik otomatik olarak devam edecektir
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">•</span>
          {{ subscription_amount }} tutarı {{ payment_method }}'ınıza otomatik olarak tahsil edilecektir
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.info|default:'#3b82f6' }}; font-size: 18px; margin-right: 8px;">•</span>
          {{ trial_end_date|date:"F d, Y" }} tarihinden önce herhangi bir ücret olmadan iptal edebilirsiniz
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ manage_subscription_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          Abonelik Yönetimi
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ cancel_subscription_url }}" style="color: {{ theme.color.error|default:'#ef4444' }}; text-decoration: underline;">
            Deneme Bitmeden Önce İptal Et
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Yardıma mı ihtiyacınız var? Bize {{ support_email }} adresinden ulaşın
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
            Spwig Tarafından Güçlendirildi
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ Deneme Yakında Bitiyor

{{ plan_name }} denemeniz {{ trial_end_date|date:"F d, Y" }} tarihinde sona erecek

DENEME BİLGİLERİ:
{{ days_remaining }} Kalan Gün Sayısı

Deneme Bitiş Tarihi: {{ trial_end_date|date:"F d, Y at g:i A" }}
Birinci Ödeme: {{ subscription_amount }} {{ trial_end_date|date:"F d, Y" }} tarihinde
Ödeme Yöntemi: {{ payment_method }}

Sonrasında Ne Olur?
• Deneme süresi bittikten sonra abonelik otomatik olarak devam edecektir
• {{ subscription_amount }} tutarı {{ payment_method }}'ınıza otomatik olarak tahsil edilecektir
• {{ trial_end_date|date:"F d, Y" }} tarihinden önce herhangi bir ücret olmadan iptal edebilirsiniz

Abonelik Yönetimi: {{ manage_subscription_url }}
Deneme Bitmeden Önce İptal Et: {{ cancel_subscription_url }}

Yardıma mı ihtiyacınız var? Bize {{ support_email }} adresinden ulaşın

---
Spwig Tarafından Güçlendirildi - https://spwig.com