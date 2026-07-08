---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ SON UYARI: Abonelikiniz {{ days_until_cancellation }} gün sonra iptal edilecek

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ SON UYARI
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Abonelik İptali Yaklaşmakta
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bu son uyarınız. {{ plan_name }} abonelikiniz için ödeme işlemini gerçekleştiremeyiz. Ödemenin {{ days_until_cancellation }} gün içinde alınması durumunda abonelikiniz iptal edilecektir.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Ödeme Başarısız - Eylem Gerekiyor
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Abonelik:</strong> {{ plan_name }}<br/>
              <strong>Tahsilat Gerekli:</strong> {{ amount_due }}<br/>
              <strong>Başarısız Denemeler:</strong> {{ retry_count }}<br/>
              <strong>Son Deneme:</strong> {{ last_retry_date }}<br/>
              <strong>Iptal Tarihi:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ödeme Hatası:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ne Olacak:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ cancellation_date }} tarihine kadar ödeme alınmazsa:<br/>
          • Abonelikiniz iptal edilecektir<br/>
          • Abonelik faydalarına erişiminiz kalmayacaktır<br/>
          • Verileriniz silinebilir (tutulma politikasına bakınız)<br/>
          • Erişim kazanmak için yeniden abone olmanız gerekir
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Ödeme Yönteminizi Şimdi Güncelleyin
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ödeme Yöntemini Güncelle
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ortak Sorunlar & Çözümler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>Geçersiz kart:</strong> Mevcut kredi kartı ile güncelleyin<br/>
          • <strong>Yetersiz bakiye:</strong> Yeterli bakiye olduğundan emin olun<br/>
          • <strong>Kart reddedildi:</strong> Bankanızla iletişime geçin veya farklı bir kart kullanın<br/>
          • <strong>Adres uyuşmazlığı:</strong> Faturalandırma adresinin kart ile eşleştiğini doğrulayın
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              Yardım mı lazımsınız?
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              Ödeme sorunları yaşıyorsanız veya yardım almanız gerekiyorsa, lütfen destek ekibimizle hemen iletişime geçin.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Destek ile İletişime Geçin
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Abonelik iptali isterseniz, hesap ayarlarınızda bunu yapabilirsiniz.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ SON UYARI

Abonelik İptali Yaklaşmakta

Merhaba {{ customer_name }},

Bu son uyarınız. {{ plan_name }} abonelikiniz için ödeme işlemini gerçekleştiremeyiz. Ödemenin {{ days_until_cancellation }} gün içinde alınması durumunda abonelikiniz iptal edilecektir.

⚠️ ÖDEME BAŞARISIZ - EYLEM GEREKİYOR:
- Abonelik: {{ plan_name }}
- Tahsilat Gerekli: {{ amount_due }}
- Başarısız Denemeler: {{ retry_count }}
- Son Deneme: {{ last_retry_date }}
- İptal Tarihi: {{ cancellation_date }}

ÖDEME HATASI:
{{ payment_error_message }}

NE OLACAK:
{{ cancellation_date }} tarihine kadar ödeme alınmazsa:
• Abonelikiniz iptal edilecektir
• Abonelik faydalarına erişiminiz kalmayacaktır
• Verileriniz silinebilir (tutulma politikasına bakınız)
• Erişim kazanmak için yeniden abone olmanız gerekir

ÖDEME YÖNTEMİNİZİ ŞİMDİ GÜNCELLEYİN

Ortak Sorunlar & Çözümler:
• Geçersiz kart: Mevcut kredi kartı ile güncelleyin
• Yetersiz bakiye: Yeterli bakiye olduğundan emin olun
• Kart reddedildi: Bankanızla iletişime geçin veya farklı bir kart kullanın
• Adres uyuşmazlığı: Faturalandırma adresinin kart ile eşleştiğini doğrulayın

YARDIM MI LAZIM?
Ödeme sorunları yaşıyorsanız veya yardım almanız gerekiyorsa, lütfen destek ekibimizle hemen iletişime geçin.

Ödeme yöntemi güncellemek için: {{ update_payment_url }}
Destek ile iletişime geçmek için: {{ support_url }}

Abonelik iptali isterseniz, hesap ayarlarınızda bunu yapabilirsiniz.