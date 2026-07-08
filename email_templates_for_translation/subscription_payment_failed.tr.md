---
template_type: subscription_payment_failed
category: Subscriptions
---

# Email Template: subscription_payment_failed

## Subject
⚠️ {{ plan_name }} Ödemesi Başarısız - Eylem Gerekiyor - {{ shop_name }}

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
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}" align="center">
          ⚠️ Ödeme Başarısız
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Ödemenizi işlemek mümkün olmadı
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Failed Payment Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#fef2f2" padding="30px" border="2px solid {{ theme.color.error|default:'#ef4444' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#7f1d1d" align="center" padding-bottom="15px">
                Ödeme Bilgileri
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Plan:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Tutar:</strong> {{ subscription_amount }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Ödeme Yöntemi:</strong> {{ payment_method }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" padding="5px 0">
                <strong>Neden:</strong> {{ failure_reason }}
              </mj-text>

              <mj-divider border-color="#fecaca" border-width="1px" padding="15px 0" />

              <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" padding="5px 0" font-weight="600">
                {{ retry_date|date:"F d, Y" }} tarihine kadar ödeme yönteminizi güncelleyin, hizmet kesilmemesi için.
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What to Do Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Ne Yapmanız Gerekiyor?
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.error|default:'#ef4444' }}; font-size=18px; margin-right: 8px;">1.</span>
          Ödeme yönteminizin yeterli bakiyeye sahip olduğundan emin olun
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.error|default:'#ef4444' }}; font-size=18px; margin-right: 8px;">2.</span>
          Kartın son kullanma tarihi geçmişse ödeme yönteminizi güncelleyin
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.error|default:'#ef4444' }}; font-size=18px; margin-right: 8px;">3.</span>
          {{ retry_days }} gün içinde ödeme otomatik olarak tekrar denenecektir
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ update_payment_url }}" background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          Ödeme Yöntemini Güncelle
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ manage_subscription_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: underline;">
            Abonelik Göster
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Yardma mı gerekiyor? Bize {{ support_email }} adresinden ulaşın
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
⚠️ Ödeme Başarısız

Ödemenizi işlemek mümkün olmadı

ÖDEME BİLGİLERİ:
Plan: {{ plan_name }}
Tutar: {{ subscription_amount }}
Ödeme Yöntemi: {{ payment_method }}
Neden: {{ failure_reason }}

{{ retry_date|date:"F d, Y" }} tarihine kadar ödeme yönteminizi güncelleyin, hizmet kesilmemesi için.

Ne Yapmanız Gerekiyor?
1. Ödeme yönteminizin yeterli bakiyeye sahip olduğundan emin olun
2. Kartın son kullanma tarihi geçmişse ödeme yönteminizi güncelleyin
3. {{ retry_days }} gün içinde ödeme otomatik olarak tekrar denenecektir

Ödeme Yöntemini Güncelle: {{ update_payment_url }}
Abonelik Göster: {{ manage_subscription_url }}

Yardma mı gerekiyor? Bize {{ support_email }} adresinden ulaşın

---
Spwig Tarafından Güçlendirildi - https://spwig.com