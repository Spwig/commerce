---
template_type: system_health_daily_report
category: System Health
---

# Email Template: system_health_daily_report

## Subject
📊 تقرير صحة النظام اليومي - {{ report_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 تقرير صحة النظام اليومي
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملخص صحة النظام
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          تقرير صحة يومي لـ {{ report_date }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الحالة العامة: {{ overall_status }}
        </mj-text>

        <mj-section background-color="{{ status_color }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#ffffff" font-weight="bold" align="center">
              {{ status_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          معايير النظام:
        </mj-text>

        {% for metric in metrics %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ metric.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الحالي:</strong> {{ metric.current_value }}<br/>
              <strong>المتوسط (24 ساعة):</strong> {{ metric.average }}<br/>
              <strong>الذروة:</strong> {{ metric.peak }}<br/>
              <strong>الحالة:</strong> <span style="color: {{ metric.status_color }};">{{ metric.status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if warnings_count > 0 or critical_count > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          التحذيرات (24 ساعة):
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الخطيرة:</strong> <span style="color: #dc2626;">{{ critical_count }}</span><br/>
              <strong>تحذيرات:</strong> <span style="color: #d97706;">{{ warnings_count }}</span><br/>
              <strong>المُستأنفة:</strong> <span style="color: #059669;">{{ resolved_count }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملخص الأداء:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>وقت التشغيل:</strong> {{ uptime_percentage }}%<br/>
              <strong>متوسط وقت الاستجابة:</strong> {{ avg_response_time }}ms<br/>
              <strong>الطلبات البطيئة:</strong> {{ slow_requests_count }}<br/>
              <strong>الأخطاء (500):</strong> {{ errors_500_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if recommendations %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          التوصيات:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض التقرير الكامل
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 تقرير صحة النظام اليومي

ملخص صحة النظام

تقرير صحة يومي لـ {{ report_date }}.

الحالة العامة: {{ overall_status }}
{{ status_message }}

معايير النظام:
{% for metric in metrics %}
{{ metric.name }}:
- الحالي: {{ metric.current_value }}
- المتوسط (24h): {{ metric.average }}
- الذروة: {{ metric.peak }}
- الحالة: {{ metric.status }}

{% endfor %}

{% if warnings_count > 0 or critical_count > 0 %}
التحذيرات (24H):
- الخطيرة: {{ critical_count }}
- التحذيرات: {{ warnings_count }}
- المُستأنفة: {{ resolved_count }}
{% endif %}

ملخص الأداء:
- وقت التشغيل: {{ uptime_percentage }}%
- متوسط وقت الاستجابة: {{ avg_response_time }}ms
- الطلبات البطيئة: {{ slow_requests_count }}
- الأخطاء (500): {{ errors_500_count }}

{% if recommendations %}
التوصيات:
{{ recommendations }}
{% endif %}

عرض التقرير الكامل: {{ full_report_url }}