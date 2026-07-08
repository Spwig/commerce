---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 번역 작업 시작: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 번역 작업 시작
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          대량 번역 진행 중
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          대량 번역 작업이 시작되어 처리 중입니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              작업 세부 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>작업 ID:</strong> {{ job_id }}<br/>
              <strong>내용 유형:</strong> {{ content_type }}<br/>
              <strong>원본 언어:</strong> {{ source_language }}<br/>
              <strong>대상 언어:</strong> {{ target_languages }}<br/>
              <strong>번역할 항목:</strong> {{ item_count }}<br/>
              <strong>시작 시간:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          예상 완료 시간:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              ({{ word_count }} 단어 기준)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          다음 단계:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. AI 번역 서비스가 내용을 처리합니다.<br/>
          2. 번역본은 검토를 위해 초안으로 저장됩니다.<br/>
          3. 작업이 완료되면 이메일을 받게 됩니다.<br/>
          4. 관리자 패널에서 번역본을 검토하고 게시합니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          작업 상태 보기
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          이 이메일을 닫으셔도 됩니다. 번역이 완료되면 알림을 드리겠습니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 번역 작업 시작

대량 번역 진행 중

대량 번역 작업이 시작되어 처리 중입니다.

작업 세부 정보:
- 작업 ID: {{ job_id }}
- 내용 유형: {{ content_type }}
- 원본 언어: {{ source_language }}
- 대상 언어: {{ target_languages }}
- 번역할 항목: {{ item_count }}
- 시작 시간: {{ started_at }}

예상 완료 시간:
{{ estimated_completion }}
({{ word_count }} 단어 기준)

다음 단계:
1. AI 번역 서비스가 내용을 처리합니다.
2. 번역본은 검토를 위해 초안으로 저장됩니다.
3. 작업이 완료되면 이메일을 받게 됩니다.
4. 관리자 패널에서 번역본을 검토하고 게시합니다.

작업 상태 보기: {{ job_status_url }}

이 이메일을 닫으셔도 됩니다. 번역이 완료되면 알림을 드리겠습니다.