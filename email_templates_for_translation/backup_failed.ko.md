---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 긴급: 백업 실패 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ 백업 실패
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          안녕하세요 {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          귀하의 {{ shop_name }} 상점에 대한 중요한 백업 작업이 실패했습니다. 데이터 보호를 위해 즉시 조치가 필요합니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              백업 세부 정보:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>백업 유형:</strong> {{ backup_type }}<br/>
              <strong>시작 시간:</strong> {{ backup_started_at }}<br/>
              <strong>실패 시간:</strong> {{ backup_failed_at }}<br/>
              <strong>지속 시간:</strong> {{ backup_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          오류 세부 정보:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          권장 조치:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. 서버의 가용 디스크 공간 확인<br/>
          2. 데이터베이스 연결 확인<br/>
          3. 상세한 스택 트레이스를 위해 오류 로그 검토<br/>
          4. 수동으로 백업 다시 시도하거나 다음 예약된 실행을 기다리세요<br/>
          5. 문제가 지속되면 지원팀에 문의하세요
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          백업 로그 보기
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          지금 백업 다시 시도
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>마지막 성공한 백업:</strong> {{ last_successful_backup }}<br/>
          <strong>다음 예약된 백업:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 긴급: 백업 실패

안녕하세요 {{ admin_name }},

귀하의 {{ shop_name }} 상점에 대한 중요한 백업 작업이 실패했습니다. 데이터 보호를 위해 즉시 조치가 필요합니다.

백업 세부 정보:
- 백업 유형: {{ backup_type }}
- 시작 시간: {{ backup_started_at }}
- 실패 시간: {{ backup_failed_at }}
- 지속 시간: {{ backup_duration }}

오류 세부 정보:
{{ error_message }}

권장 조치:
1. 서버의 가용 디스크 공간 확인
2. 데이터베이스 연결 확인
3. 상세한 스택 트레이스를 위해 오류 로그 검토
4. 수동으로 백업 다시 시도하거나 다음 예약된 실행을 기다리세요
5. 문제가 지속되면 지원팀에 문의하세요

백업 로그 보기: {{ admin_backup_url }}
지금 백업 다시 시도: {{ retry_backup_url }}

마지막 성공한 백업: {{ last_successful_backup }}
다음 예약된 백업: {{ next_scheduled_backup }}

---
{{ shop_name }} 관리자에게 중요한 시스템 경고입니다.