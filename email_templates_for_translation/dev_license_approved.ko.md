---
template_type: dev_license_approved
category: Developer Portal
---

# Email Template: dev_license_approved

## Subject
Spwig 개발자 라이선스가 준비되었습니다!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Success Accent -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          라이선스 승인됨!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          개발용 라이선스가 준비되었습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          안녕하세요, {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          개발자 라이선스 요청이 승인되었습니다. 이 라이선스를 사용하여 개발 및 테스트용으로 로컬 Spwig 설치를 실행할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          귀하의 라이선스 키
        </mj-text>
        <mj-text font-size="18px" font-family="monospace" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding="20px" background-color="{{ theme.color.background|default:'#ffffff' }}" border="2px solid {{ theme.color.success|default:'#10b981' }}">
          {{ license_key }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>라이선스 유형:</strong> {{ license_type }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>만료일:</strong> {{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Important Notice -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.warning|default:'#f59e0b' }}">
          <strong>중요:</strong> 이 라이선스는 개발 용도로만 사용할 수 있습니다. 프로덕션 환경에서 사용하거나 다른 사람과 공유하지 마세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          대시보드로 이동
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Spwig 개발자 포털</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          질문이 있으십니까? 개발자 지원팀에 문의하세요
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
안녕하세요, {{ developer_name }},

개발자 라이선스 요청이 승인되었습니다. 이 라이선스를 사용하여 개발 및 테스트용으로 로컬 Spwig 설치를 실행할 수 있습니다.

귀하의 라이선스 키:
{{ license_key }}

라이선스 유형: {{ license_type }}{% if expires_at %}
만료일: {{ expires_at }}{% endif %}

중요: 이 라이선스는 개발 용도로만 사용할 수 있습니다. 프로덕션 환경에서 사용하거나 다른 사람과 공유하지 마세요.

대시보드로 이동: {{ dashboard_url }}

---
Spwig 개발자 포털