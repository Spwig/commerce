---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
Ödeme Sağlayıcısı Sorunu - {{ provider_name }} SDK Yükleme Başarısız

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          Ödeme Sağlayıcısı Sorunu
        </mj-text>
        <mj-text>
          Müşteri, ödeme sırasında {{ provider_name }} ödeme SDK'sı yüklenemedi. Bu, sağlayıcıyla ilgili bir hizmet kesilmesi olabilir.
        </mj-text>
        <mj-text>
          <strong>Provider:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>Hata Türü:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>Zaman:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>Başarısızlık Sayısı (son saat):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Bu bildirim, sağlayıcı başına saatte bir kez olacak şekilde oranla sınırlanmıştır. Sorun devam ederse, sağlayıcının kontrol panelini inceleyin veya destek ile iletişime geçin.
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Ödeme Ayarlarını Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ödeme Sağlayıcısı Sorunu

Müşteri, ödeme sırasında {{ provider_name }} ödeme SDK'sı yüklenemedi. Bu, sağlayıcıyla ilgili bir hizmet kesilmesi olabilir.

Provider: {{ provider_name }}
Hata Türü: {{ error_type }}
Zaman: {{ timestamp }}
Başarısızlık Sayısı (son saat): {{ failure_count }}

Bu bildirim, sağlayıcı başına saatte bir kez olacak şekilde oranla sınırlanmıştır. Sorun devam ederse, sağlayıcının kontrol panelini inceleyin veya destek ile iletişime geçin.

Ödeme ayarlarını görüntüle: {{ admin_url }}