---
template_type: backup_size_warning
category: Backups
---

# Email Template: backup_size_warning

## Subject
⚠️ 백업 크기 경고 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 백업 크기 경고
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ shop_name }}에 대한 최근 백업이 권장 크기 임계값을 초과했습니다. 이는 데이터 저장 공간의 증가를 나타낼 수 있습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              백업 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Current Size:</strong> {{ backup_size }}<br/>
              <strong>Warning Threshold:</strong> {{ size_threshold }}<br/>
              <strong>Growth Since Last Week:</strong> {{ size_increase }}<br/>
              <strong>Backup Date:</strong> {{ backup_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          권장 조치:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. 백업 보존 정책 검토<br/>
          2. 오래된 백업의 아카이빙을 고려하세요<br/>
          3. 미디어 라이브러리에서 불필요한 대용량 파일 확인<br/>
          4. 저장 용량 요구 사항 평가<br/>
          5. 백업 성장 추세 모니터링
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          백업 관리
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 백업 크기 경고

안녕하세요 {{ admin_name }},

{{ shop_name }}에 대한 최근 백업이 권장 크기 임계값을 초과했습니다. 이는 데이터 저장 공간의 증가를 나타낼 수 있습니다.

백업 정보:
- Current Size: {{ backup_size }}
- Warning Threshold: {{ size_threshold }}
- Growth Since Last Week: {{ size_increase }}
- Backup Date: {{ backup_date }}

권장 조치:
1. 백업 보존 정책 검토
2. 오래된 백업의 아카이빙을 고려하세요
3. 미디어 라이브러리에서 불필요한 대용량 파일 확인
4. 저장 용량 요구 사항 평가
5. 백업 성장 추세 모니터링

백업 관리: {{ admin_backup_url }}
