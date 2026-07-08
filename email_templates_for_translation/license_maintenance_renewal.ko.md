---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
유지보수 갱신 - 주문 #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          유지보수 갱신!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          주문 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          안녕하세요, {{ customer_name }}!
        </mj-text>
        <mj-text>
          귀하의 Spwig 유지보수 구독이 성공적으로 갱신되었습니다. 플랫폼 업데이트, 보안 패치, 새 기능을 계속 받아보실 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          갱신 요약
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          라이선스 키: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          유지보수 유효 기한: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          주문 번호: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          포함 사항
        </mj-text>
        <mj-text font-size="14px">
          활성 유지보수는 다음과 같은 항목에 대한 접근을 제공합니다:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - 플랫폼 기능 업데이트 및 개선
        </mj-text>
        <mj-text font-size="14px">
          - 보안 패치 및 버그 수정
        </mj-text>
        <mj-text font-size="14px">
          - 업그레이드 서버를 통해 새 구성 요소 출시
        </mj-text>
        <mj-text font-size="14px">
          - 기술 지원
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          귀하의 조치는 필요 없습니다. 업데이트는 관리자 패널의 구성 요소 업데이트 시스템을 통해 계속 제공됩니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
유지보수 갱신!

주문 #{{ order_number }}

안녕하세요, {{ customer_name }}!

귀하의 Spwig 유지보수 구독이 성공적으로 갱신되었습니다. 플랫폼 업데이트, 보안 패치, 새 기능을 계속 받아보실 수 있습니다.

갱신 요약:
- 라이선스 키: {{ license_key }}
- 유지보수 유효 기한: {{ renewal_expires_at }}
- 주문 번호: {{ order_number }}

포함 사항:
- 플랫폼 기능 업데이트 및 개선
- 보안 패치 및 버그 수정
- 업그레이드 서버를 통해 새 구성 요소 출시
- 기술 지원

귀하의 조치는 필요 없습니다. 업데이트는 관리자 패널의 구성 요소 업데이트 시스템을 통해 계속 제공됩니다.

도움이 필요하신가요? {{ support_email }}에 문의해 주세요.