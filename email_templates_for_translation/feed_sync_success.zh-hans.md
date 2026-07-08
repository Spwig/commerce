---
template_type: feed_sync_success
category: Product Feeds
---

# Email Template: feed_sync_success

## Subject
✓ {{ feed_name }} 已与 {{ platform_name }} 同步

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ 同步成功
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          馈源已成功同步
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          您的 {{ feed_name }} 已成功同步到 {{ platform_name }}。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              同步详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
              <strong>Synced:</strong> {{ synced_at }}<br/>
              <strong>Products Synced:</strong> {{ products_synced }}<br/>
              <strong>Duration:</strong> {{ sync_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          变更摘要：
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% if products_added > 0 %}• {{ products_added }} 产品{{ products_added|pluralize }} 已添加<br/>{% endif %}
          {% if products_updated > 0 %}• {{ products_updated }} 产品{{ products_updated|pluralize }} 已更新<br/>{% endif %}
          {% if products_removed > 0 %}• {{ products_removed }} 产品{{ products_removed|pluralize }} 已移除<br/>{% endif %}
        </mj-text>
        {% endif %}

        {% if sync_warnings %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 同步警告
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
          在 {{ platform_name }} 上查看
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看馈源详情
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 同步成功

馈源已成功同步

您的 {{ feed_name }} 已成功同步到 {{ platform_name }}。

同步详情：
- Feed: {{ feed_name }}
- Platform: {{ platform_name }}
- Synced: {{ synced_at }}
- Products Synced: {{ products_synced }}
- Duration: {{ sync_duration }}

{% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
变更摘要：
{% if products_added > 0 %}• {{ products_added }} 产品{{ products_added|pluralize }} 已添加{% endif %}
{% if products_updated > 0 %}• {{ products_updated }} 产品{{ products_updated|pluralize }} 已更新{% endif %}
{% if products_removed > 0 %}• {{ products_removed }} 产品{{ products_removed|pluralize }} 已移除{% endif %}
{% endif %}

{% if sync_warnings %}
⚠️ 同步警告：
{{ sync_warnings }}
{% endif %}

{% if platform_url %}在 {{ platform_name }} 上查看：{{ platform_url }}{% endif %}
查看馈源详情：{{ admin_feed_url }}