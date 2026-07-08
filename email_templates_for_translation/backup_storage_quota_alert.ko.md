---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 백업 저장소 할당량 비상 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 저장소 할당량 비상
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>긴급:</strong> 백업 저장소가 거의 가득 찼습니다. 저장 공간을 해제하지 않으면 향후 백업이 실패할 수 있습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              저장소 상태:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>사용량:</strong> {{ storage_used }} of {{ storage_total }}<br/>
              <strong>사용률:</strong> {{ storage_percentage }}%<br/>
              <strong>가용량:</strong> {{ storage_available }}<br/>
              <strong>상태:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              즉시 필요한 조치:
            </mj-text>
            <mj-text color="#92400e">
              1. 더 이상 필요하지 않은 오래된 백업 삭제<br/>
              2. 외부 저장소로 백업 아카이브<br/>
              3. 저장소 할당량/용량 증가<br/>
              4. 백업 보유 정책 검토<br/>
              5. 해결할 때까지 매일 저장소 모니터링
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          저장소 관리 바로 가기
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 저장소 할당량 비상

안녕하세요 {{ admin_name }},

긴급: 백업 저장소가 거의 가득 찼습니다. 저장 공간을 해제하지 않으면 향후 백업이 실패할 수 있습니다.

저장소 상태:
- 사용량: {{ storage_used }} of {{ storage_total }}
- 사용률: {{ storage_percentage }}%
- 가용량: {{ storage_available }}
- 상태: {{ storage_status }}

즉시 필요한 조치:
1. 더 이상 필요하지 않은 오래된 백업 삭제
2. 외부 저장소로 백업 아카이브
3. 저장소 할당량/용량 증가
4. 백업 보유 정책 검토
5. 해결할 때까지 매일 저장소 모니터링

저장소 관리 바로 가기: {{ admin_backup_url }}