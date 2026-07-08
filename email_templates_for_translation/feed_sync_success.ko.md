---
template_type: feed_sync_success
category: Product Feeds
---

# Email Template: feed_sync_success

## Subject
✓ {{ feed_name }}을 {{ platform_name }}과 동기화했습니다

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#065f46" align="center">
          ✓ 동기화 성공
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          피드가 성공적으로 동기화되었습니다
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ feed_name }}이(가) {{ platform_name }}과 성공적으로 동기화되었습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              동기화 세부 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>피드:</strong> {{ feed_name }}<br/>
              <strong>플랫폼:</strong> {{ platform_name }}<br/>
              <strong>동기화 시간:</strong> {{ synced_at }}<br/>
              <strong>동기화된 상품:</strong> {{ products_synced }}<br/>
              <strong>소요 시간:</strong> {{ sync_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          변경 사항 요약:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% if products_added > 0 %}• {{ products_added }} 개의 상품{{ products_added|pluralize }}이 추가되었습니다.<br/>{% endif %}
          {% if products_updated > 0 %}• {{ products_updated }} 개의 상품{{ products_updated|pluralize }}이 수정되었습니다.<br/>{% endif %}
          {% if products_removed > 0 %}• {{ products_removed }} 개의 상품{{ products_removed|pluralize }}이 제거되었습니다.<br/>{% endif %}
        </mj-text>
        {% endif %}

        {% if sync_warnings %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 동기화 경고
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
          {{ platform_name }}에서 보기
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          피드 세부 정보 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 동기화 성공

피드가 성공적으로 동기화되었습니다

{{ feed_name }}이(가) {{ platform_name }}과 성공적으로 동기화되었습니다.

동기화 세부 정보:
- 피드: {{ feed_name }}
- 플랫폼: {{ platform_name }}
- 동기화 시간: {{ synced_at }}
- 동기화된 상품: {{ products_synced }}
- 소요 시간: {{ sync_duration }}

{% if products_added > 0 or products_updated > 0 or products_removed > 0 %}
변경 사항 요약:
{% if products_added > 0 %}• {{ products_added }} 개의 상품{{ products_added|pluralize }}이 추가되었습니다.{% endif %}
{% if products_updated > 0 %}• {{ products_updated }} 개의 상품{{ products_updated|pluralize }}이 수정되었습니다.{% endif %}
{% if products_removed > 0 %}• {{ products_removed }} 개의 상품{{ products_removed|pluralize }}이 제거되었습니다.{% endif %}
{% endif %}

{% if sync_warnings %}
⚠️ 동기화 경고:
{{ sync_warnings }}
{% endif %}

{% if platform_url %}{{ platform_name }}에서 보기: {{ platform_url }}{% endif %}
피드 세부 정보 보기: {{ admin_feed_url }}