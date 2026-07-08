---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ Yedekleme Geri Yükleme Tamamlandı - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Yedekleme Geri Yükleme Tamamlandı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Yedekleme geri yükleme işlemi başarıyla tamamlandı. Mağaza verileriniz geri yüklendi.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Geri Yükleme Detayları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Yedek Dosyası:</strong> {{ backup_filename }}<br/>
              <strong>Yedek Tarihi:</strong> {{ backup_date }}<br/>
              <strong>Başlatıldı:</strong> {{ restore_started_at }}<br/>
              <strong>Tamamlandı:</strong> {{ restore_completed_at }}<br/>
              <strong>Süre:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Önemli Bir Sonraki Adımlar:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. Mağazanızın düzgün çalıştığını doğrulayın<br/>
              2. Ana verileri kontrol edin (ürünler, siparişler, müşteriler)<br/>
              3. Gerekirse önbelleği temizleyin<br/>
              4. Kritik iş akışlarını test edin (ödeme, yönetici erişimi)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Yönetici Paneline Git
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ YEDEKLEME GERİ YÜKLEME TAMAMLANDI

Merhaba {{ admin_name }},

Yedekleme geri yükleme işlemi başarıyla tamamlandı. Mağaza verileriniz geri yüklendi.

GERİ YÜKLEME DETAYLARI:
- Yedek Dosyası: {{ backup_filename }}
- Yedek Tarihi: {{ backup_date }}
- Başlatıldı: {{ restore_started_at }}
- Tamamlandı: {{ restore_completed_at }}
- Süre: {{ restore_duration }}

⚠️ ÖNEMLİ BİR SONRAKİ ADIMLAR:
1. Mağazanızın düzgün çalıştığını doğrulayın
2. Ana verileri kontrol edin (ürünler, siparişler, müşteriler)
3. Gerekirse önbelleği temizleyin
4. Kritik iş akışlarını test edin (ödeme, yönetici erişimi)

Yönetici paneline git: {{ admin_dashboard_url }}