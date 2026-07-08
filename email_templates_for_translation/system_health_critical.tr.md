---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 KRİTİK UYARI: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 KRİTİK SİSTEM UYARI
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Hemen Dikkat Gerekiyor
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Spwig kurulumunuzda kritik bir sistem sağlığı sorunu tespit edildi.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 KRİTİK SORUN
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Metric:</strong> {{ metric_name }}<br/>
              <strong>Current Value:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Kritik Seviye:</strong> {{ critical_threshold }}<br/>
              <strong>Tespit Edildi:</strong> {{ detected_at }}<br/>
              <strong>Ağırılık:</strong> KRİTİK
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Etki:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Hemen Gerekli Eylemler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Eğilim:
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Hizmet Kalitesi Uyarısı
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Bu sorun, hizmet kesilmesine veya performans düşmesine neden olabilir. Müşteri etkisini önlemek için hemen çözüme kavuşturun.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Sistem Panosu'nu Görüntüle
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Sistem Günlüklerini Görüntüle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 KRİTİK SİSTEM UYARI

Hemen Dikkat Gerekiyor

Spwig kurulumunuzda kritik bir sistem sağlığı sorunu tespit edildi.

🚨 KRİTİK SORUN:
- Metric: {{ metric_name }}
- Current Value: {{ current_value }}
- Kritik Seviye: {{ critical_threshold }}
- Tespit Edildi: {{ detected_at }}
- Ağırılık: KRİTİK

ETKİ:
{{ impact_description }}

Hemen Gerekli Eylemler:
{{ recommended_actions }}

{% if trend_data %}
EĞİLİM:
{{ trend_data }}
{% endif %}

⚠️ HİZMET KALİTESİ UYARISI:
Bu sorun, hizmet kesilmesine veya performans düşmesine neden olabilir. Müşteri etkisini önlemek için hemen çözüme kavuşturun.

Sistem panosu'nu görüntüle: {{ dashboard_url }}
Sistem günlüklerini görüntüle: {{ logs_url }}