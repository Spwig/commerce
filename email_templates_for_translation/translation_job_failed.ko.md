---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ 번역 작업 실패: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ 번역 작업 실패
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          번역 오류
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          대량 번역 작업 중 오류가 발생하여 완료되지 않았습니다.
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
              <strong>대상 언어:</strong> {{ target_languages }}<br/>
              <strong>실패 시간:</strong> {{ failed_at }}<br/>
              <strong>오류 코드:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          오류 메시지:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              부분 완료
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              오류 발생 이전에 {{ items_completed }}개의 {{ total_items }}개 항목이 성공적으로 번역되었습니다.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          일반적인 원인:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 번역 서비스 API 연결 문제<br/>
          • 번역 크레딧 부족<br/>
          • 유효하지 않거나 손상된 원본 콘텐츠<br/>
          • 지원되지 않는 언어 쌍
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          권장 조치:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 번역 서비스 설정 확인<br/>
          2. 번역 크레딧이 사용 가능한지 확인<br/>
          3. 오류 메시지에서 구체적인 문제 확인<br/>
          4. 번역 작업 다시 시도
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          번역 다시 시도
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          설정 확인
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          문제가 지속되면 오류 코드 {{ error_code }}와 함께 지원팀에 문의하십시오.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ 번역 작업 실패

번역 오류

대량 번역 작업 중 오류가 발생하여 완료되지 않았습니다.

작업 세부 정보:
- 작업 ID: {{ job_id }}
- 내용 유형: {{ content_type }}
- 대상 언어: {{ target_languages }}
- 실패 시간: {{ failed_at }}
- 오류 코드: {{ error_code }}

오류 메시지:
{{ error_message }}

{% if partial_completion %}
부분 완료:
{{ items_completed }}개의 {{ total_items }}개 항목이 오류 발생 이전에 성공적으로 번역되었습니다.
{% endif %}

일반적인 원인:
• 번역 서비스 API 연결 문제
• 번역 크레딧 부족
• 유효하지 않거나 손상된 원본 콘텐츠
• 지원되지 않는 언어 쌍

권장 조치:
1. 번역 서비스 설정 확인
2. 번역 크레딧이 사용 가능한지 확인
3. 오류 메시지에서 구체적인 문제 확인
4. 번역 작업 다시 시도

번역 다시 시도: {{ retry_url }}
설정 확인: {{ settings_url }}

문제가 지속되면 오류 코드 {{ error_code }}와 함께 지원팀에 문의하십시오.