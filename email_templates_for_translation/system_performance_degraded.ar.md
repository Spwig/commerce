---
template_type: system_performance_degraded
category: System Health
---

# Email Template: system_performance_degraded

## Subject
⚠️ تدهور الأداء - {{ affected_area }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ تدهور الأداء
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تم اكتشاف أوقات استجابة بطيئة
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          يعاني تثبيت Spwig الخاص بك من تدهور في الأداء.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              مشكلة الأداء:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المنطقة المتضررة:</strong> {{ affected_area }}<br/>
              <strong>وقت الاستجابة الحالي:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_response_time }}ms</span><br/>
              <strong>وقت الاستجابة الطبيعي:</strong> {{ normal_response_time }}ms<br/>
              <strong>التدهور:</strong> {{ degradation_percentage }}% أبطأ<br/>
              <strong>تم اكتشافه:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          التأثير:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الأسباب المحتملة:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ possible_causes }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          نقاط النهاية البطيئة:
        </mj-text>

        {% for endpoint in slow_endpoints %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ endpoint.path }}</strong> - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} طلبات)
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإجراءات المقترحة:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ performance_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض لوحة مراقبة الأداء
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ slow_queries_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          عرض الاستعلامات البطيئة
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          سنقوم بإعلامك عندما يعود الأداء إلى طبيعته.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ تدهور الأداء

تم اكتشاف أوقات استجابة بطيئة

يعاني تثبيت Spwig الخاص بك من تدهور في الأداء.

مشكلة الأداء:
- المنطقة المتضررة: {{ affected_area }}
- وقت الاستجابة الحالي: {{ current_response_time }}ms
- وقت الاستجابة الطبيعي: {{ normal_response_time }}ms
- التدهور: {{ degradation_percentage }}% أبطأ
- تم اكتشافه: {{ detected_at }}

التأثير:
{{ impact_description }}

الأسباب المحتملة:
{{ possible_causes }}

نقاط النهاية البطيئة:
{% for endpoint in slow_endpoints %}
{{ endpoint.path }} - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} طلبات)
{% endfor %}

الإجراءات المقترحة:
{{ recommended_actions }}

عرض لوحة مراقبة الأداء: {{ performance_dashboard_url }}
عرض الاستعلامات البطيئة: {{ slow_queries_url }}

سنقوم بإعلامك عندما يعود الأداء إلى طبيعته.