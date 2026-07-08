---
template_type: subscription_canceled
category: Subscriptions
---

# Email Template: subscription_canceled

## Subject
❌ {{ plan_name }} Aboneliğiniz İptal Edildi - {{ shop_name }}

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
          Gitmekten Üzgünüz
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Aboneliğiniz iptal edildi
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Cancellation Details Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px" border="2px solid {{ theme.color.text_muted|default:'#6b7280' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
                İptal Özeti
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Plan:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>İptal Tarihi:</strong> {{ cancellation_date|date:"F d, Y" }}
              </mj-text>

              {% if access_until %}
              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Erişim Süresi:</strong> {{ access_until|date:"F d, Y" }}
              </mj-text>
              <mj-text font-size="13px" color="{{ theme.color.success|default:'#10b981' }}" padding="10px 0 5px 0">
                ✓ {{ access_until|date:"F d, Y" }} tarihine kadar faydalarınıza erişim hakkınız devam edecektir
              </mj-text>
              {% else %}
              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Durum:</strong> Anında iptal edildi
              </mj-text>
              {% endif %}
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- What This Means Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Bu Ne Demek?
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          Sizden başka ücret alınmayacak
        </mj-text>

        {% if access_until %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          {{ access_until|date:"F d, Y" }} tarihine kadar faydalarınıza erişim hakkınız devam edecektir
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          Erişiminiz anında sona erdi
        </mj-text>
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="8px 20px" line-height="1.6">
          <span style="color: {{ theme.color.text_muted|default:'#6b7280' }}; font-size: 18px; margin-right: 8px;">•</span>
          Her zaman tekrar etkinleştirebilirsiniz
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Feedback Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px 15px 20px" line-height="1.6" align="center">
          Geri bildirimlerinizi almak bizi geliştirmemize yardımcı olur.
        </mj-text>
        <mj-button href="{{ feedback_url }}" background-color="{{ theme.color.text_muted|default:'#6b7280' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="14px" font-weight="600" border-radius="6px" padding="12px 28px">
          Geri Bildirim Gönder
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Reactivate CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px 15px 20px" line-height="1.6" align="center">
          Fikrinizi değiştirdiniz mi? Aboneliğinizi her zaman tekrar etkinleştirebilirsiniz.
        </mj-text>
        <mj-button href="{{ reactivate_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          Aboneliği Etkinleştir
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Yardıma mı ihtiyacınız var? Bize {{ support_email }} adresinden ulaşabilirsiniz.
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
Gitmekten Üzgünüz

Aboneliğiniz iptal edildi

İPTAL ÖZETİ:
Plan: {{ plan_name }}
İptal Tarihi: {{ cancellation_date|date:"F d, Y" }}
{% if access_until %}Erişim Süresi: {{ access_until|date:"F d, Y" }}

✓ {{ access_until|date:"F d, Y" }} tarihine kadar faydalarınıza erişim hakkınız devam edecektir
{% else %}Durum: Anında iptal edildi
{% endif %}

Bu Ne Demek:
• Sizden başka ücret alınmayacak
{% if access_until %}• {{ access_until|date:"F d, Y" }} tarihine kadar faydalarınıza erişim hakkınız devam edecektir
{% else %}• Erişiminiz anında sona erdi
{% endif %}• Her zaman tekrar etkinleştirebilirsiniz

Geri bildirimlerinizi almak bizi geliştirmemize yardımcı olur.
Geri Bildirim Gönder: {{ feedback_url }}

Fikrinizi değiştirdiniz mi? Aboneliğinizi her zaman tekrar etkinleştirebilirsiniz.
Aboneliği Etkinleştir: {{ reactivate_url }}

Yardıma mı ihtiyacınız var? Bize {{ support_email }} adresinden ulaşabilirsiniz.

---
Spwig Tarafından Güçlendirildi - https://spwig.com