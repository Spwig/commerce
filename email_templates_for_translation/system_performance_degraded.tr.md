---
template_type: system_performance_degraded
category: System Health
---

# Email Template: system_performance_degraded

## Subject
⚠️ Performans Düşüşü Tespit Edildi - {{ affected_area }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Performans Düşüşü
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Yavaş Yanıt Süreleri Tespit Edildi
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Spwig kurulumunuzda performans düşüşü yaşanıyor.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Performans Sorunu:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Etkilenen Alan:</strong> {{ affected_area }}<br/>
              <strong>Mevcut Yanıt Süresi:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_response_time }}ms</span><br/>
              <strong>Normal Yanıt Süresi:</strong> {{ normal_response_time }}ms<br/>
              <strong>Düşüş:</strong> {{ degradation_percentage }}% daha yavaş<br/>
              <strong>Tespit Edildi:</strong> {{ detected_at }}
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
          Muhtemel Nedenler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ possible_causes }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          En Yavaş Son Noktalar:
        </mj-text>

        {% for endpoint in slow_endpoints %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ endpoint.path }}</strong> - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} istek)
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Önerilen Eylemler:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ performance_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Performans Panosunu Görüntüle
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ slow_queries_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Yavaş Sorguları Görüntüle
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Performansın normal seviyeye döndüğünde size haber vereceğiz.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ PERFORMANS DÜŞÜŞÜ

Yavaş Yanıt Süreleri Tespit Edildi

Spwig kurulumunuzda performans düşüşü yaşanıyor.

PERFORMANS SORUNU:
- Etkilenen Alan: {{ affected_area }}
- Mevcut Yanıt Süresi: {{ current_response_time }}ms
- Normal Yanıt Süresi: {{ normal_response_time }}ms
- Düşüş: {{ degradation_percentage }}% daha yavaş
- Tespit Edildi: {{ detected_at }}

ETKİ:
{{ impact_description }}

MUHTEMEL NEDENLER:
{{ possible_causes }}

EN YAVAŞ SON NOKTALAR:
{% for endpoint in slow_endpoints %}
{{ endpoint.path }} - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} istek)
{% endfor %}

ÖNERİLEN EYLEMLER:
{{ recommended_actions }}

Performans panosunu görüntüle: {{ performance_dashboard_url }}
Yavaş sorguları görüntüle: {{ slow_queries_url }}

Performansın normal seviyeye döndüğünde size haber vereceğiz.