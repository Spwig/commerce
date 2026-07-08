---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ 품질이 낮은 번역 감지됨: {{ content_type }} - {{ low_quality_count }}개 항목 검토 필요

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 번역 품질 경고
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          검토 권장
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          번역 작업이 완료되었지만 {{ low_quality_count }}개의 번역이 품질 임계값 미만으로 평가되어 출판 전에 검토해야 합니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              작업 요약:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>작업 ID:</strong> {{ job_id }}<br/>
              <strong>내용 유형:</strong> {{ content_type }}<br/>
              <strong>총 항목:</strong> {{ total_items }}<br/>
              <strong>평균 품질:</strong> {{ average_quality }}%<br/>
              <strong>저품질:</strong> {{ low_quality_count }}개 항목 ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          품질 분석:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>우수 (95-100%):</strong> {{ excellent_count }}개 항목<br/>
              <strong>양호 (85-94%):</strong> {{ good_count }}개 항목<br/>
              <strong>보통 (70-84%):</strong> {{ fair_count }}개 항목<br/>
              <strong>부족 (&lt;70%):</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }}개 항목</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          일반적인 품질 문제:
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}:</strong> {{ issue.count }}회 발생
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          권장 조치:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 관리자 패널에서 표시된 번역 검토<br/>
          2. 저품질 번역을 수동으로 편집<br/>
          3. 품질이 낮은 항목을 재번역 고려<br/>
          4. 검토 완료 후에만 출판
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          번역 검토
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          저품질 항목 보기
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 팁: 85% 미만의 품질 점수는 문법, 맥락 또는 정확성에 잠재적 문제가 있음을 나타냅니다. 출판 전에 인간 검토를 강력히 권장합니다.
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 번역 품질 경고

검토 권장

번역 작업이 완료되었지만 {{ low_quality_count }}개의 번역이 품질 임계값 미만으로 평가되어 출판 전에 검토해야 합니다.

작업 요약:
- 작업 ID: {{ job_id }}
- 내용 유형: {{ content_type }}
- 총 항목: {{ total_items }}
- 평균 품질: {{ average_quality }}%
- 저품질: {{ low_quality_count }}개 항목 ({{ low_quality_percentage }}%)

품질 분석:
- 우수 (95-100%): {{ excellent_count }}개 항목
- 양호 (85-94%): {{ good_count }}개 항목
- 보통 (70-84%): {{ fair_count }}개 항목
- 부족 (<70%): {{ poor_count }}개 항목

일반적인 품질 문제:
{% for issue in quality_issues %}
{{ issue.type }}: {{ issue.count }}회 발생
{% endfor %}

권장 조치:
1. 관리자 패널에서 표시된 번역 검토
2. 저품질 번역을 수동으로 편집
3. 품질이 낮은 항목을 재번역 고려
4. 검토 완료 후에만 출판

번역 검토: {{ review_url }}
저품질 항목 보기: {{ low_quality_url }}

💡 팁: 85% 미만의 품질 점수는 문법, 맥락 또는 정확성에 잠재적 문제가 있음을 나타냅니다. 출판 전에 인간 검토를 강력히 권장합니다.