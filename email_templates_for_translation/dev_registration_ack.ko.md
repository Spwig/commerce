---
template_type: dev_registration_ack
category: Developer Portal
---

# Email Template: dev_registration_ack

## Subject
개발자 신청서를 받았습니다, {{ developer_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          신청서 수신!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          개발자 신청서를 검토 중입니다
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
          Spwig 개발자 프로그램에 지원해 주셔서 감사합니다. 신청서를 받았으며, 팀이 곧 검토할 예정입니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          다음 단계는 무엇인가요?
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> 팀이 신청서를 검토합니다 (보통 2~3 영업일)
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> 결정을 담은 이메일을 받게 됩니다
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>3.</strong> 승인되면 개발자 대시보드에 대한 전체 접근 권한을 얻게 됩니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ portal_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          개발자 포털 보기
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
          질문이 있으신가요? 개발자 지원팀에 문의해 주세요
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
안녕하세요, {{ developer_name }},

Spwig 개발자 프로그램에 지원해 주셔서 감사합니다. 신청서를 받았으며, 팀이 곧 검토할 예정입니다.

다음 단계는 무엇인가요?
1. 팀이 신청서를 검토합니다 (보통 2~3 영업일)
2. 결정을 담은 이메일을 받게 됩니다
3. 승인되면 개발자 대시보드에 대한 전체 접근 권한을 얻게 됩니다

개발자 포털 보기: {{ portal_url }}

---
Spwig 개발자 포털