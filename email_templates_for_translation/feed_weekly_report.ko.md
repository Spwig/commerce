---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 주간 제품 피드 보고서 - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 주간 피드 성과
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          피드 성과 요약
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ week_range }} 기간 동안 제품 피드의 성과는 다음과 같습니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          전체 통계:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>총 피드 수:</strong> {{ total_feeds }}<br/>
              <strong>활성 피드 수:</strong> {{ active_feeds }}<br/>
              <strong>총 동기화 수:</strong> {{ total_syncs }}<br/>
              <strong>성공한 동기화 수:</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>실패한 동기화 수:</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          피드별 성과:
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              플랫폼: {{ feed.platform }}<br/>
              동기화: {{ feed.sync_count }} ({{ feed.success_count }} 성공)<br/>
              제품: {{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}에러: {{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          가장 흔한 문제:
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }}:</strong> {{ error.count }} 회 발생
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
              💡 추천 사항
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          피드 대시보드 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 주간 피드 성과

피드 성과 요약

{{ week_range }} 기간 동안 제품 피드의 성과는 다음과 같습니다.

전체 통계:
- 총 피드 수: {{ total_feeds }}
- 활성 피드 수: {{ active_feeds }}
- 총 동기화 수: {{ total_syncs }}
- 성공한 동기화 수: {{ successful_syncs }} ({{ success_rate }}%)
- 실패한 동기화 수: {{ failed_syncs }}

피드별 성과:
{% for feed in feed_stats %}
{{ feed.name }}
플랫폼: {{ feed.platform }}
동기화: {{ feed.sync_count }} ({{ feed.success_count }} 성공)
제품: {{ feed.product_count }}
{% if feed.errors > 0 %}에러: {{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
가장 흔한 문제:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} 회 발생
{% endfor %}
{% endif %}

{% if recommendations %}
💡 추천 사항:
{{ recommendations }}
{% endif %}

피드 대시보드 보기: {{ feeds_dashboard_url }}