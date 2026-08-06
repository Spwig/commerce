---
template_type: subscription_payment_failed
category: Subscriptions
---

# Email Template: subscription_payment_failed

## Subject
⚠️ {{ plan_name }} için Ödeme Başarısızı - Eylem Gerekli - {{ shop_name }}

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
          Ödemenizi işlemek için yeterli değil
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
                Ödeme Bilgisi
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

              {% if retry_date %}
              <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" padding="5px 0" font-weight="600">
                {{ retry_date|date:"F d, Y" }} tarihine kadar ödeme yöntemini güncellemelisiniz, aksi takdirde hizmet kesintisine uğrayabilirsiniz.
              </mj-text>
              {% endif %}
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What to Do Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Ne Yapmalısınız?
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.error|default:'#ef4444' }}; font-size=18px; margin-right: 8px;">1.</span>
          Ödeme yönteminde yeterli bakiye olup olmadığını kontrol edin
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.error|default:'#ef4444' }}; font-size=18px; margin-right: 8px;">2.</span>
          Kartınızın süresi dolmuşsa ödeme yöntemini güncelleyin
        </mj-text>

        {% if retry_days %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.error|default:'#ef4444' }}; font-size=18px; margin-right: 8px;">3.</span>
          {{ retry_days }} gün içinde otomatik olarak ödeme denenecektir
        </mj-text>
        {% endif %}
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
            Aboneliği Görüntüle
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Yardıma mı ihtiyacınız var? {{ support_email }} adresinden bize ulaşın
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
            Spwig tarafından desteklenmektedir
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ Ödeme Başarısızı

Ödemenizi işlemek için yeterli değil

ÖDEME BİLGİSİ:
Plan: {{ plan_name }}
Tutar: {{ subscription_amount }}
Ödeme Yöntemi: {{ payment_method }}
Neden: {{ failure_reason }}

{% if retry_date %}{{ retry_date|date:"F d, Y" }} tarihine kadar ödeme yöntemini güncellemelisiniz, aksi takdirde hizmet kesintisine uğrayabilirsiniz.{% endif %}

Ne Yapmalısınız?
1. Ödeme yönteminde yeterli bakiye olup olmadığını kontrol edin
2. Kartınızın süresi dolmuşsa ödeme yöntemini güncelleyin
{% if retry_days %}3. {{ retry_days }} gün içinde otomatik olarak ödeme denenecektir{% endif %}

Ödeme Yöntemini Güncelle: {{ update_payment_url }}
Aboneliği Görüntüle: {{ manage_subscription_url }}

Yardıma mı ihtiyacınız var? {{ support_email }} adresinden bize ulaşın

---
Spwig tarafından desteklenmektedir - https://spwig.com