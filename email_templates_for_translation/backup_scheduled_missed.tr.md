---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ Planlanan Yedekleme Gerçekleşmedi - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Planlanan Yedekleme Kaçırıldı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ shop_name }} için planlanan yedekleme beklenen şekilde çalışmamıştır. Verileriniz tam olarak korunmamış olabilir.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Yedekleme Planı Ayrıntıları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Zamanlanmış Zaman:</strong> {{ scheduled_time }}<br/>
              <strong>Yedekleme Türü:</strong> {{ backup_type }}<br/>
              <strong>Son Başarılı Yedekleme:</strong> {{ last_successful_backup }}<br/>
              <strong>Son Yedekten Geçen Süre:</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Olası Nedenler:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • Sunucu çevrimdışıydi veya erişilebilir değildi<br/>
          • Zamanlanmış görev hizmeti çalışmıyor<br/>
          • Yetersiz izinler<br/>
          • Depolama alanı dolu<br/>
          • Veritabanı bağlantısı sorunları
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Manuel Yedekleme Yap
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Sistem Günlüklerini Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ PLANLANAN YEDEKLEME KAÇIRILDI

Merhaba {{ admin_name }},

{{ shop_name }} için planlanan yedekleme beklenen şekilde çalışmamıştır. Verileriniz tam olarak korunmamış olabilir.

YEDEKLEME PLANI AYRINTILARI:
- Zamanlanmış Zaman: {{ scheduled_time }}
- Yedekleme Türü: {{ backup_type }}
- Son Başarılı Yedekleme: {{ last_successful_backup }}
- Son Yedekten Geçen Süre: {{ time_since_last }}

OLASI NEDENLER:
• Sunucu çevrimdışıydi veya erişilebilir değildi
• Zamanlanmış görev hizmeti çalışmıyor
• Yetersiz izinler
• Depolama alanı dolu
• Veritabanı bağlantısı sorunları

Manuel yedekleme yap: {{ admin_backup_url }}
Sistem günlüklerini görüntüle: {{ admin_logs_url }}