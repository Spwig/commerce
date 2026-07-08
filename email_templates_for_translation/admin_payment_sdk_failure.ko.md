---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
결제 제공업체 문제 - {{ provider_name }} SDK 로드 실패

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          결제 제공업체 문제
        </mj-text>
        <mj-text>
          체크아웃 중 고객의 {{ provider_name }} 결제 SDK가 로드에 실패했습니다. 이는 제공업체의 서비스 중단을 나타낼 수 있습니다.
        </mj-text>
        <mj-text>
          <strong>Provider:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>Error Type:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>Time:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>Failure Count (last hour):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          이 알림은 제공업체당 시간당 한 번으로 제한되어 있습니다. 문제가 지속되면 제공업체 대시보드를 확인하거나 지원팀에 문의하세요.
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          결제 설정 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
결제 제공업체 문제

체크아웃 중 고객의 {{ provider_name }} 결제 SDK가 로드에 실패했습니다. 이는 제공업체의 서비스 중단을 나타낼 수 있습니다.

Provider: {{ provider_name }}
Error Type: {{ error_type }}
Time: {{ timestamp }}
Failure Count (last hour): {{ failure_count }}

이 알림은 제공업체당 시간당 한 번으로 제한되어 있습니다. 문제가 지속되면 제공업체 대시보드를 확인하거나 지원팀에 문의하세요.

결제 설정 보기: {{ admin_url }}