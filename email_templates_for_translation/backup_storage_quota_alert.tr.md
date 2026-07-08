---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 {{ shop_name }} için Depolama Kotası Kritik

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 Depolama Kotası Kritik
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>ACİL:</strong> Yedekleme depolamanız kritik düzeyde düşük. Depolama alanı boşaltılmazsa gelecekteki yedeklemeler başarısız olabilir.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Depolama Durumu:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Kullanılan:</strong> {{ storage_used }} of {{ storage_total }}<br/>
              <strong>Kullanım:</strong> {{ storage_percentage }}%<br/>
              <strong>Mevcut:</strong> {{ storage_available }}<br/>
              <strong>Durum:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Acil Olarak Yapılacak İşlemler:
            </mj-text>
            <mj-text color="#92400e">
              1. Kullanım dışı olan eski yedeklemeleri silin<br/>
              2. Yedeklemeleri harici depolama alanına arşivleyin<br/>
              3. Depolama kotası/ kapasitesini artırın<br/>
              4. Yedekleme saklama politikasını gözden geçirin<br/>
              5. Sorun çözülene kadar günlük olarak depolamayı izleyin
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Şimdi Depolamayı Yönetin
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 DEPOLAMA KOTASI KRİTİK

Merhaba {{ admin_name }},

ACİL: Yedekleme depolamanız kritik düzeyde düşük. Depolama alanı boşaltılmazsa gelecekteki yedeklemeler başarısız olabilir.

DEPOLAMA DURUMU:
- Kullanılan: {{ storage_used }} of {{ storage_total }}
- Kullanım: {{ storage_percentage }}%
- Mevcut: {{ storage_available }}
- Durum: {{ storage_status }}

ACİL OLARAK YAPILACAK İŞLEMLER:
1. Kullanım dışı olan eski yedeklemeleri silin
2. Yedeklemeleri harici depolama alanına arşivleyin
3. Depolama kotası/ kapasitesini artırın
4. Yedekleme saklama politikasını gözden geçirin
5. Sorun çözülene kadar günlük olarak depolamayı izleyin

Depolamayı şimdi yönetin: {{ admin_backup_url }}