---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 تقرير مغذٍ لمنتج الأسبوع - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 أداء التغذية الأسبوعية
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملخص أداء التغذية
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          إليك أداء تغذية منتجاتك من {{ week_range }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإحصائيات العامة:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>إجمالي التغذيات:</strong> {{ total_feeds }}<br/>
              <strong>التغذيات النشطة:</strong> {{ active_feeds }}<br/>
              <strong>إجمالي التزامنات:</strong> {{ total_syncs }}<br/>
              <strong>التزامنات الناجحة:</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>التزامنات الفاشلة:</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          أداء التغذية حسب كل تغذية:
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              منصة: {{ feed.platform }}<br/>
              التزامنات: {{ feed.sync_count }} ({{ feed.success_count }} ناجحة)<br/>
              المنتجات: {{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}الخطأ: {{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          المشكلات الأكثر شيوعًا:
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }}:</strong> {{ error.count }} مرات
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}
        {% endif %}

        <mj-spacer height="30px" />

        {% if recommendations %}
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              💡 التوصيات
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض لوحة التغذية
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 أداء التغذية الأسبوعية

ملخص أداء التغذية

إليك أداء تغذية منتجاتك من {{ week_range }}.

الإحصائيات العامة:
- إجمالي التغذيات: {{ total_feeds }}
- التغذيات النشطة: {{ active_feeds }}
- إجمالي التزامنات: {{ total_syncs }}
- التزامنات الناجحة: {{ successful_syncs }} ({{ success_rate }}%)
- التزامنات الفاشلة: {{ failed_syncs }}

أداء التغذية حسب كل تغذية:
{% for feed in feed_stats %}
{{ feed.name }}
منصة: {{ feed.platform }}
الالتزامنات: {{ feed.sync_count }} ({{ feed.success_count }} ناجحة)
المنتجات: {{ feed.product_count }}
{% if feed.errors > 0 %}الخطأ: {{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
المشكلات الأكثر شيوعًا:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} مرات
{% endfor %}
{% endif %}

{% if recommendations %}
💡 التوصيات:
{{ recommendations }}
{% endif %}

عرض لوحة التغذية: {{ feeds_dashboard_url }}