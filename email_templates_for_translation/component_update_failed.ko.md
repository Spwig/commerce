---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ 업데이트 실패: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ 업데이트 실패
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          설치 오류
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }}을(를) {{ target_version }} 버전으로 업데이트하는 데 실패했습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              실패 세부 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>성분:</strong> {{ component_name }}<br/>
              <strong>대상 버전:</strong> {{ target_version }}<br/>
              <strong>실패 시간:</strong> {{ failed_at }}<br/>
              <strong>에러 코드:</strong> {{ error_code }}
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

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>전체 오류 로그:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:50 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          해법:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 시스템 요구 사항 및 의존성을 확인하세요<br/>
          2. 오류 로그를 검토하여 세부 정보를 확인하세요<br/>
          3. 다시 설치를 시도하거나 지원팀에 문의하세요<br/>
          4. 귀하의 가게는 여전히 {{ current_version }}에서 실행되고 있습니다
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          다시 설치 시도
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          지원팀 문의
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ 업데이트 실패

설치 오류

{{ component_name }}을(를) {{ target_version }} 버전으로 업데이트하는 데 실패했습니다.

실패 세부 정보:
- 성분: {{ component_name }}
- 대상 버전: {{ target_version }}
- 실패 시간: {{ failed_at }}
- 에러 코드: {{ error_code }}

오류 메시지:
{{ error_message }}

{% if error_log %}
전체 오류 로그:
{{ error_log|truncatewords:50 }}
{% endif %}

해법:
1. 시스템 요구 사항 및 의존성을 확인하세요
2. 오류 로그를 검토하여 세부 정보를 확인하세요
3. 다시 설치를 시도하거나 지원팀에 문의하세요
4. 귀하의 가게는 여전히 {{ current_version }}에서 실행되고 있습니다

다시 설치 시도: {{ retry_url }}
지원팀 문의: {{ support_url }}