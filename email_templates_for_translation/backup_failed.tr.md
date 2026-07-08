---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 Acil: Yedekleme Başarısız - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ Yedekleme Başarısız
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          Merhaba {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ shop_name }} mağazanız için kritik bir yedekleme işlemi başarısız oldu. Veri koruma için acil müdahale gerekir.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Yedekleme Ayrıntıları:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Yedekleme Türü:</strong> {{ backup_type }}<br/>
              <strong>Başladı:</strong> {{ backup_started_at }}<br/>
              <strong>Başarısız Oldu:</strong> {{ backup_failed_at }}<br/>
              <strong>Süre:</strong> {{ backup_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Hata Ayrıntıları:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Önerilen Eylemler:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Sunucunuzda kullanılabilir disk alanı kontrol edin<br/>
          2. Veritabanı bağlantısını doğrulayın<br/>
          3. Ayrıntılı stack trace için hata günlüğünü inceleyin<br/>
          4. Manuel olarak yedeklemeyi tekrarlayın veya bir sonraki planlanan çalışmayı bekleyin<br/>
          5. Sorun devam ederse destek ile iletişime geçin
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Yedekleme Günlüklerini Görüntüle
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Şimdi Yedeklemeyi Tekrar Dene
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Son Başarılı Yedekleme:</strong> {{ last_successful_backup }}<br/>
          <strong>Bir Sonraki Planlanan Yedekleme:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 Acil: YEDEKLEME BAŞARISIZ

Merhaba {{ admin_name }},

{{ shop_name }} mağazanız için kritik bir yedekleme işlemi başarısız oldu. Veri koruma için acil müdahale gerekir.

YEDEKLEME AYRINTILARI:
- Yedekleme Türü: {{ backup_type }}
- Başladı: {{ backup_started_at }}
- Başarısız Oldu: {{ backup_failed_at }}
- Süre: {{ backup_duration }}

HATA AYRINTILARI:
{{ error_message }}

ÖNERİLEN EYLEMLER:
1. Sunucunuzda kullanılabilir disk alanı kontrol edin
2. Veritabanı bağlantısını doğrulayın
3. Ayrıntılı stack trace için hata günlüğünü inceleyin
4. Manuel olarak yedeklemeyi tekrarlayın veya bir sonraki planlanan çalışmayı bekleyin
5. Sorun devam ederse destek ile iletişime geçin

Yedekleme günlüklerini görüntüle: {{ admin_backup_url }}
Şimdi yedeklemeyi tekrar dene: {{ retry_backup_url }}

Son Başarılı Yedekleme: {{ last_successful_backup }}
Bir Sonraki Planlanan Yedekleme: {{ next_scheduled_backup }}

---
{{ shop_name }} yöneticileri için kritik bir sistem uyarısı.