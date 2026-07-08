---
template_type: backup_size_warning
category: Backups
---

# Email Template: backup_size_warning

## Subject
⚠️ Yedekleme Boyutu Uyarısı - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Yedekleme Boyutu Uyarısı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ shop_name }} için son yedeklemeniz, önerilen boyut eşiğini aştı. Bu, veri depolama ihtiyaçlarınızın arttığını gösterebilir.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Yedekleme Bilgisi:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Mevcut Boyut:</strong> {{ backup_size }}<br/>
              <strong>Uyarı Eşiği:</strong> {{ size_threshold }}<br/>
              <strong>Bir Hafta Öncesi Büyüme:</strong> {{ size_increase }}<br/>
              <strong>Yedekleme Tarihi:</strong> {{ backup_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Önerilen Eylemler:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Yedekleme saklama politikasını gözden geçirin<br/>
          2. Eski yedeklemeleri arşivlemeyi değerlendirin<br/>
          3. Medya kütüphanesinde gereksiz büyük dosyaları inceleyin<br/>
          4. Depolama kapasite ihtiyaçlarını değerlendirin<br/>
          5. Yedekleme büyümesi eğilimini izleyin
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Yedeklemeleri Yönet
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ YEDEKLEME BOYUTU UYARISI

Merhaba {{ admin_name }},

{{ shop_name }} için son yedeklemeniz, önerilen boyut eşiğini aştı. Bu, veri depolama ihtiyaçlarınızın arttığını gösterebilir.

YEDEKLEME BİLGİSİ:
- Mevcut Boyut: {{ backup_size }}
- Uyarı Eşiği: {{ size_threshold }}
- Bir Hafta Öncesi Büyüme: {{ size_increase }}
- Yedekleme Tarihi: {{ backup_date }}

ÖNERİLEN EYLEMLER:
1. Yedekleme saklama politikasını gözden geçirin
2. Eski yedeklemeleri arşivlemeyi değerlendirin
3. Medya kütüphanesinde gereksiz büyük dosyaları inceleyin
4. Depolama kapasite ihtiyaçlarını değerlendirin
5. Yedekleme büyümesi eğilimini izleyin

Yedeklemeleri yönet: {{ admin_backup_url }}