---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ 예약 백업이 실행되지 않았습니다 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 예약 백업이 지나갔습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ shop_name }}의 예약 백업이 예상대로 실행되지 않았습니다. 데이터가 완전히 보호되지 않을 수 있습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              백업 일정 세부 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>예약 시간:</strong> {{ scheduled_time }}<br/>
              <strong>백업 유형:</strong> {{ backup_type }}<br/>
              <strong>마지막 성공적인 백업:</strong> {{ last_successful_backup }}<br/>
              <strong>마지막 백업 이후 경과 시간:</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          가능한 원인:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • 서버가 오프라인 또는 연결할 수 없음<br/>
          • 예약 작업 서비스가 실행 중이지 않음<br/>
          • 권한이 부족함<br/>
          • 저장 공간이 가득함<br/>
          • 데이터베이스 연결 문제
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          수동으로 백업 실행
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          시스템 로그 보기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 예약 백업이 지나갔습니다

안녕하세요 {{ admin_name }},

{{ shop_name }}의 예약 백업이 예상대로 실행되지 않았습니다. 데이터가 완전히 보호되지 않을 수 있습니다.

백업 일정 세부 정보:
- 예약 시간: {{ scheduled_time }}
- 백업 유형: {{ backup_type }}
- 마지막 성공적인 백업: {{ last_successful_backup }}
- 마지막 백업 이후 경과 시간: {{ time_since_last }}

가능한 원인:
• 서버가 오프라인 또는 연결할 수 없음
• 예약 작업 서비스가 실행 중이지 않음
• 권한이 부족함
• 저장 공간이 가득함
• 데이터베이스 연결 문제

수동으로 백업 실행: {{ admin_backup_url }}
시스템 로그 보기: {{ admin_logs_url }}