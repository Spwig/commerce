---
template_type: system_health_warning
category: System Health
---

# Email Template: system_health_warning

## Subject
⚠️ Sistem Sağlığı Uyarısı: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Sistem Sağlığı Uyarısı
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Uyarı Eşiği Aşıldı
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Spwig kurulumunuzda bir sistem sağlığı ölçümü uyarı eşiğini aştı.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Uyarı Ayrıntıları:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Metric:</strong> {{ metric_name }}<br/>
              <strong>Mevcut Değer:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Uyarı Eşiği:</strong> {{ warning_threshold }}<br/>
              <strong>Kritik Eşiği:</strong> {{ critical_threshold }}<br/>
              <strong>Tespit Edildi:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Potansiyel Etki:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Önerilen Eylemler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Eğilim Analizi:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ trend_data }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Eylem Gerekiyor: Şimdilik kritik değil, ancak bu uyarıyı şimdi çözmek gelecekteki hizmet sorunlarını önlemeye yardımcı olabilir.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Sistem Panelini Görüntüle
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ metrics_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ayrıntılı Ölçümleri Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ SİSTEM SAĞLIĞI UYARISI

Uyarı Eşiği Aşıldı

Spwig kurulumunuzda bir sistem sağlığı ölçümü uyarı eşiğini aştı.

UYARI AYRINTILARI:
- Metric: {{ metric_name }}
- Mevcut Değer: {{ current_value }}
- Uyarı Eşiği: {{ warning_threshold }}
- Kritik Eşiği: {{ critical_threshold }}
- Tespit Edildi: {{ detected_at }}

POTANSİYEL ETKİ:
{{ impact_description }}

ÖNERİLEN EYLEMLER:
{{ recommended_actions }}

{% if trend_data %}
EĞİLİM ANALİZİ:
{{ trend_data }}
{% endif %}

💡 EYLEM GEREKİYOR: Şimdilik kritik değil, ancak bu uyarıyı şimdi çözmek gelecekteki hizmet sorunlarını önlemeye yardımcı olabilir.

Sistem panelini görüntüle: {{ dashboard_url }}
Ayrıntılı ölçümleri görüntüle: {{ metrics_url }}