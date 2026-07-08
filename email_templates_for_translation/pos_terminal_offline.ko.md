---
template_type: pos_terminal_offline
category: POS
---

# Email Template: pos_terminal_offline

## Subject
⚠️ POS 터미널 오프라인: {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ 터미널 연결 끊김
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          POS 터미널 오프라인
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }}이 오프라인 상태가 되었으며 더 이상 응답하지 않습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              터미널 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>터미널:</strong> {{ terminal_name }}<br/>
              <strong>위치:</strong> {{ location }}<br/>
              <strong>최근 본 시간:</strong> {{ last_seen }}<br/>
              <strong>오프라인 시작 시간:</strong> {{ offline_since }}<br/>
              <strong>지속 시간:</strong> {{ offline_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          일반적인 원인:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 네트워크 연결 문제<br/>
          • 터미널이 꺼져 있거나 재시작됨<br/>
          • 소프트웨어 충돌 또는 동결<br/>
          • 인터넷 서비스 중단
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          권장 조치:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 터미널 전원 및 네트워크 연결 확인<br/>
          2. 터미널 장치 재시작<br/>
          3. 인터넷 연결 확인<br/>
          4. 방화벽 및 보안 설정 확인
        </mj-text>

        {% if active_shift %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 활성 시프트 경고
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              이 터미널에는 활성 시프트가 있습니다. 다시 연결될 때까지 판매 데이터가 동기화되지 않을 수 있습니다.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_terminals_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          터미널 상태 보기
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          터미널이 다시 연결되면 다른 알림을 받을 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 터미널 연결 끊김

POS 터미널 오프라인

{{ terminal_name }}이 오프라인 상태가 되었으며 더 이상 응답하지 않습니다.

터미널 정보:
- 터미널: {{ terminal_name }}
- 위치: {{ location }}
- 최근 본 시간: {{ last_seen }}
- 오프라인 시작 시간: {{ offline_since }}
- 지속 시간: {{ offline_duration }}

일반적인 원인:
• 네트워크 연결 문제
• 터미널이 꺼져 있거나 재시작됨
• 소프트웨어 충돌 또는 동결
• 인터넷 서비스 중단

권장 조치:
1. 터미널 전원 및 네트워크 연결 확인
2. 터미널 장치 재시작
3. 인터넷 연결 확인
4. 방화벽 및 보안 설정 확인

{% if active_shift %}
⚠️ 활성 시프트 경고:
이 터미널에는 활성 시프트가 있습니다. 다시 연결될 때까지 판매 데이터가 동기화되지 않을 수 있습니다.
{% endif %}

터미널 상태 보기: {{ admin_terminals_url }}

터미널이 다시 연결되면 다른 알림을 받을 수 있습니다.