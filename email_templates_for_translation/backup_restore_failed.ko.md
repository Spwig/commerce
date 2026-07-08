---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 비상: 백업 복원 실패 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 비상: 백업 복원 실패
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          안녕하세요 {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          중요한 백업 복원 작업이 실패했습니다. 귀하의 가게가 일관되지 않은 상태에 있을 수 있으므로 즉시 조치가 필요합니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              복원 세부 정보:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>백업 파일:</strong> {{ backup_filename }}<br/>
              <strong>시작 시간:</strong> {{ restore_started_at }}<br/>
              <strong>실패 시간:</strong> {{ restore_failed_at }}<br/>
              <strong>지속 시간:</strong> {{ restore_duration }}
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 즉시 조치가 필요한 사항:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>절대</strong> 가게에 변경 사항을 적용하지 마세요<br/>
              2. 데이터베이스 연결성 및 무결성을 확인하세요<br/>
              3. 상세한 스택 트레이스를 위해 오류 로그를 검토하세요<br/>
              4. 즉시 기술 지원에 연락하세요<br/>
              5. 마지막으로 확인된 정상 상태로 되돌아가는 것을 고려하세요
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          복원 로그 보기
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          긴급 기술 지원 연락
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 비상: 백업 복원 실패

안녕하세요 {{ admin_name }},

중요한 백업 복원 작업이 실패했습니다. 귀하의 가게가 일관되지 않은 상태에 있을 수 있으므로 즉시 조치가 필요합니다.

복원 세부 정보:
- 백업 파일: {{ backup_filename }}
- 시작 시간: {{ restore_started_at }}
- 실패 시간: {{ restore_failed_at }}
- 지속 시간: {{ restore_duration }}

오류 세부 정보:
{{ error_message }}

🚨 즉시 조치가 필요한 사항:
1. 절대 가게에 변경 사항을 적용하지 마세요
2. 데이터베이스 연결성 및 무결성을 확인하세요
3. 상세한 스택 트레이스를 위해 오류 로그를 검토하세요
4. 즉시 기술 지원에 연락하세요
5. 마지막으로 확인된 정상 상태로 되돌아가는 것을 고려하세요

복원 로그 보기: {{ admin_backup_url }}
긴급 기술 지원 연락: {{ support_url }}