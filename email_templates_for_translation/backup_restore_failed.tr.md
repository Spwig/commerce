---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 KRİTİK: Yedekleme Geri Yükleme Başarısız Oldu - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 KRİTİK: Yedekleme Geri Yükleme Başarısız Oldu
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          Merhaba {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          KRİTİK bir yedekleme geri yükleme işlemi başarısız oldu. Mağazanız tutarsız bir durumda olabilir ve derhal dikkat gerektiriyor.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Geri Yükleme Detayları:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Yedek Dosyası:</strong> {{ backup_filename }}<br/>
              <strong>Başlatıldı:</strong> {{ restore_started_at }}<br/>
              <strong>Başarısız Oldu:</strong> {{ restore_failed_at }}<br/>
              <strong>Süre:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Hata Detayları:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 DERHAL EYLEM GEREKLİ:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>DEĞİL</strong> mağazaya herhangi bir değişiklik yapın<br/>
              2. Veritabanı bağlantısını ve bütünlüğünü kontrol edin<br/>
              3. Ayrıntılı hata ayıklama için hata günlüklerini inceleyin<br/>
              4. Teknik destekle derhal iletişime geçin<br/>
              5. Bilinen iyi duruma geri dönmeyi düşünün
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Geri Yükleme Günlüklerini Görüntüle
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Acil Destekle İletişime Geç
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 KRİTİK: YEDEKLEME GERİ YÜKLEME BAŞARISIZ OLDU

Merhaba {{ admin_name }},

KRİTİK bir yedekleme geri yükleme işlemi başarısız oldu. Mağazanız tutarsız bir durumda olabilir ve derhal dikkat gerektiriyor.

GERİ YÜKLEME DETAYLARI:
- Yedek Dosyası: {{ backup_filename }}
- Başlatıldı: {{ restore_started_at }}
- Başarısız Oldu: {{ restore_failed_at }}
- Süre: {{ restore_duration }}

HATA DETAYLARI:
{{ error_message }}

🚨 DERHAL EYLEM GEREKLİ:
1. DEĞİL mağazaya herhangi bir değişiklik yapın
2. Veritabanı bağlantısını ve bütünlüğünü kontrol edin
3. Ayrıntılı hata ayıklama için hata günlüklerini inceleyin
4. Teknik destekle derhal iletişime geçin
5. Bilinen iyi duruma geri dönmeyi düşünün

Geri yükleme günlüklerini görüntüleyin: {{ admin_backup_url }}
Acil destekle iletişime geçin: {{ support_url }}
