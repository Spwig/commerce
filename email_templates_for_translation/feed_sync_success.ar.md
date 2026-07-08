---
template_type: feed_sync_success
category: Product Feeds
---

# Email Template: feed_sync_success

## Subject
✓ تم تزامن {{ feed_name }} مع {{ platform_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ تم التزامن بنجاح
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تم تزامن المغذي بنجاح
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          تم تزامن {{ feed_name }} بنجاح مع {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل التزامن:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المغذي:</strong> {{ feed_name }}<br/>
              <strong>المنصة:</strong> {{ platform_name }}<br/>
              <strong>تم التزامن:</strong> {{ synced_at }}<br/>
              <strong>المنتجات المزامنة:</strong> {{ products_synced }}<br/>
              <strong>المدة:</strong> {{ sync_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملخص التغييرات:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% if products_added > 0 %}• {{ products_added }} منتج{{ products_added|pluralize }} تم إضافته<br/>{% endif %}
          {% if products_updated > 0 %}• {{ products_updated }} منتج{{ products_updated|pluralize }} تم تحديثه<br/>{% endif %}
          {% if products_removed > 0 %}• {{ products_removed }} منتج{{ products_removed|pluralize }} تم حذفه<br/>{% endif %}
        </mj-text>
        {% endif %}

        {% if sync_warnings %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ تحذيرات التزامن
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ sync_warnings }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if platform_url %}
        <mj-button href="{{ platform_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          الاطلاع على {{ platform_name }}
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          الاطلاع على تفاصيل المغذي
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ تم التزامن بنجاح

تم تزامن المغذي بنجاح

تم تزامن {{ feed_name }} بنجاح مع {{ platform_name }}.

تفاصيل التزامن:
- المغذي: {{ feed_name }}
- المنصة: {{ platform_name }}
- تم التزامن: {{ synced_at }}
- المنتجات المزامنة: {{ products_synced }}
- المدة: {{ sync_duration }}

{% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
ملخص التغييرات:
{% if products_added > 0 %}• {{ products_added }} منتج{{ products_added|pluralize }} تم إضافته{% endif %}
{% if products_updated > 0 %}• {{ products_updated }} منتج{{ products_updated|pluralize }} تم تحديثه{% endif %}
{% if products_removed > 0 %}• {{ products_removed }} منتج{{ products_removed|pluralize }} تم حذفه{% endif %}
{% endif %}

{% if sync_warnings %}
⚠️ تحذيرات التزامن:
{{ sync_warnings }}
{% endif %}

{% if platform_url %}الاطلاع على {{ platform_name }}: {{ platform_url }}{% endif %}
الاطلاع على تفاصيل المغذي: {{ admin_feed_url }}