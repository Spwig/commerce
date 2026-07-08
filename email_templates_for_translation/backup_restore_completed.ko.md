---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ 백업 복원 완료 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ 백업 복원 완료
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          백업 복원 작업이 성공적으로 완료되었습니다. 스토어 데이터가 복원되었습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              복원 세부 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>백업 파일:</strong> {{ backup_filename }}<br/>
              <strong>백업 날짜:</strong> {{ backup_date }}<br/>
              <strong>시작 시간:</strong> {{ restore_started_at }}<br/>
              <strong>완료 시간:</strong> {{ restore_completed_at }}<br/>
              <strong>지속 시간:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 중요한 다음 단계:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. 스토어가 올바르게 작동하는지 확인하세요<br/>
              2. 주요 데이터(상품, 주문, 고객)를 확인하세요<br/>
              3. 필요시 캐시를 지우세요<br/>
              4. 주요 워크플로(체크아웃, 관리자 액세스)를 테스트하세요
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          관리자 대시보드로 이동
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 백업 복원 완료

안녕하세요 {{ admin_name }},

백업 복원 작업이 성공적으로 완료되었습니다. 스토어 데이터가 복원되었습니다.

복원 세부 정보:
- 백업 파일: {{ backup_filename }}
- 백업 날짜: {{ backup_date }}
- 시작 시간: {{ restore_started_at }}
- 완료 시간: {{ restore_completed_at }}
- 지속 시간: {{ restore_duration }}

⚠️ 중요한 다음 단계:
1. 스토어가 올바르게 작동하는지 확인하세요
2. 주요 데이터(상품, 주문, 고객)를 확인하세요
3. 필요시 캐시를 지우세요
4. 주요 워크플로(체크아웃, 관리자 액세스)를 테스트하세요

관리자 대시보드로 이동: {{ admin_dashboard_url }}