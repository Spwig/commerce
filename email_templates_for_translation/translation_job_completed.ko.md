---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ 번역 완료: {{ content_type }} ({{ language_count }} 개의 언어)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ 번역 완료!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          번역이 준비되었습니다
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          훌륭한 소식입니다! 대량 번역 작업이 성공적으로 완료되었습니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              작업 요약:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>작업 ID:</strong> {{ job_id }}<br/>
              <strong>내용 유형:</strong> {{ content_type }}<br/>
              <strong>언어:</strong> {{ target_languages }}<br/>
              <strong>번역된 항목:</strong> {{ items_translated }}<br/>
              <strong>총 단어 수:</strong> {{ word_count }}<br/>
              <strong>완료 시간:</strong> {{ completed_at }}<br/>
              <strong>지속 시간:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          번역 품질:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>평균 품질 점수:</strong> {{ quality_score }}%<br/>
              <strong>고품질:</strong> {{ high_quality_count }} 항목<br/>
              <strong>검토 권장:</strong> {{ review_needed_count }} 항목
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 검토 권장
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} 번역이 85% 미만의 점수를 받았으며, 게시하기 전에 검토해야 합니다.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          다음 단계:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 관리자 패널에서 번역을 검토하세요<br/>
          2. 개선이 필요한 번역을 편집하세요<br/>
          3. 번역을 게시하여 사용 가능하게 하세요<br/>
          4. 다국어 콘텐츠가 고객에게 제공될 것입니다
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          번역 검토
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          모두 게시
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 번역 완료!

번역이 준비되었습니다

좋은 소식입니다! 대량 번역 작업이 성공적으로 완료되었습니다.

작업 요약:
- 작업 ID: {{ job_id }}
- 내용 유형: {{ content_type }}
- 언어: {{ target_languages }}
- 번역된 항목: {{ items_translated }}
- 총 단어 수: {{ word_count }}
- 완료 시간: {{ completed_at }}
- 지속 시간: {{ job_duration }}

번역 품질:
- 평균 품질 점수: {{ quality_score }}%
- 고품질: {{ high_quality_count }} 항목
- 검토 권장: {{ review_needed_count }} 항목

{% if review_needed_count > 0 %}
⚠️ 검토 권장:
{{ review_needed_count }} 번역이 85% 미만의 점수를 받았으며, 게시하기 전에 검토해야 합니다.
{% endif %}

다음 단계:
1. 관리자 패널에서 번역을 검토하세요
2. 개선이 필요한 번역을 편집하세요
3. 번역을 게시하여 사용 가능하게 하세요
4. 다국어 콘텐츠가 고객에게 제공될 것입니다

번역 검토: {{ review_url }}
{% if can_publish_all %}모두 게시: {{ publish_all_url }}{% endif %}