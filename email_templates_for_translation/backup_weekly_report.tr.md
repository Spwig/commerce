---
template_type: backup_weekly_report
category: Backups
---

# Email Template: backup_weekly_report

## Subject
Haftalık Yedekleme Özeti - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Haftalık Yedekleme Özeti
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          {{ week_start }} - {{ week_end }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Yedekleme İstatistikleri:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Total Backups:</strong> {{ total_backups }}<br/>
              <strong>Başarılı:</strong> <span style="color: #059669;">{{ successful_backups }}</span><br/>
              <strong>Başarısız:</strong> <span style="color: #dc2626;">{{ failed_backups }}</span><br/>
              <strong>Ortalama Boyut:</strong> {{ average_size }}<br/>
              <strong>Kullanılan Toplam Depolama:</strong> {{ total_storage }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if failed_backups > 0 %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Tespiti Yapılan Sorunlar:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ failed_backups }} yedekleme(ler) bu hafta başarısız oldu. Lütfen inceleyin ve düzeltici önlemler alın.
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          En Son Yedekleme:
        </mj-text>

        {% for backup in recent_backups %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px" margin-bottom="8px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
              <strong>{{ backup.date }}</strong> - {{ backup.type }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Boyut: {{ backup.size }} | Süre: {{ backup.duration }} |
              {% if backup.status == 'success' %}
              <span style="color: #059669;">✓ Başarı</span>
              {% else %}
              <span style="color: #dc2626;">✗ Başarısız</span>
              {% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Tüm Yedeklemeleri Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
HAFTALIK YEDEKLEME ÖZETİ
{{ week_start }} - {{ week_end }}

YEDEKLEME İSTATİSTİKLERİ:
- Toplam Yedeklemeler: {{ total_backups }}
- Başarılı: {{ successful_backups }}
- Başarısız: {{ failed_backups }}
- Ortalama Boyut: {{ average_size }}
- Kullanılan Toplam Depolama: {{ total_storage }}

{% if failed_backups > 0 %}
⚠️ TESPİTİ YAPILAN SORUNLAR:
{{ failed_backups }} yedekleme(ler) bu hafta başarısız oldu. Lütfen inceleyin ve düzeltici önlemler alın.
{% endif %}

EN SON YEDEKLEME:
{% for backup in recent_backups %}
- {{ backup.date }} - {{ backup.type }}
  Boyut: {{ backup.size }} | Süre: {{ backup.duration }} | Durum: {{ backup.status }}
{% endfor %}

Tüm yedeklemeleri görüntüle: {{ admin_backup_url }}