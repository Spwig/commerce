---
template_type: feed_sync_success
category: Product Feeds
---

# Email Template: feed_sync_success

## Subject
✓ {{ feed_name }} đã được đồng bộ với {{ platform_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ Đồng bộ thành công
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Feed đã đồng bộ thành công
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Feed {{ feed_name }} của bạn đã được đồng bộ thành công với {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết đồng bộ:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Mặt trận:</strong> {{ platform_name }}<br/>
              <strong>Đã đồng bộ:</strong> {{ synced_at }}<br/>
              <strong>Sản phẩm đồng bộ:</strong> {{ products_synced }}<br/>
              <strong>Thời lượng:</strong> {{ sync_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tóm tắt thay đổi:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% if products_added > 0 %}• {{ products_added }} sản phẩm{{ products_added|pluralize }} được thêm<br/>{% endif %}
          {% if products_updated > 0 %}• {{ products_updated }} sản phẩm{{ products_updated|pluralize }} được cập nhật<br/>{% endif %}
          {% if products_removed > 0 %}• {{ products_removed }} sản phẩm{{ products_removed|pluralize }} bị xóa<br/>{% endif %}
        </mj-text>
        {% endif %}

        {% if sync_warnings %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Cảnh báo đồng bộ
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
          Xem trên {{ platform_name }}
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem chi tiết Feed
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ĐỒNG BỘ THÀNH CÔNG

Feed đã đồng bộ thành công

Feed {{ feed_name }} của bạn đã được đồng bộ thành công với {{ platform_name }}.

CHI TIẾT ĐỒNG BỘ:
- Feed: {{ feed_name }}
- Mặt trận: {{ platform_name }}
- Đã đồng bộ: {{ synced_at }}
- Sản phẩm đồng bộ: {{ products_synced }}
- Thời lượng: {{ sync_duration }}

{% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
TÓM TẮT THAY ĐỔI:
{% if products_added > 0 %}• {{ products_added }} sản phẩm{{ products_added|pluralize }} được thêm{% endif %}
{% if products_updated > 0 %}• {{ products_updated }} sản phẩm{{ products_updated|pluralize }} được cập nhật{% endif %}
{% if products_removed > 0 %}• {{ products_removed }} sản phẩm{{ products_removed|pluralize }} bị xóa{% endif %}
{% endif %}

{% if sync_warnings %}
⚠️ CẢNH BÁO ĐỒNG BỘ:
{{ sync_warnings }}
{% endif %}

{% if platform_url %}Xem trên {{ platform_name }}: {{ platform_url }}{% endif %}
Xem chi tiết feed: {{ admin_feed_url }}