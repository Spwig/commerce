---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
중요: 계정이 일시 중지되었습니다

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          계정이 일시 중지되었습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          안녕하세요, {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ shop_name }}의 파트너 계정이 일시 중지되었습니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          이는 일반적으로 파트너 프로그램의 이용 약관을 위반한 경우입니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          이 결정이 오류라고 생각하거나 논의하고자 한다면, 지원 팀에 연락해 주세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          질문이 있으십니까? <a href="mailto:{{ support_email }}" style="color: #007bff;">지원팀에 문의하기</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
중요: 계정이 일시 중지되었습니다

안녕하세요, {{ affiliate_name }},

{{ shop_name }}의 파트너 계정이 일시 중지되었습니다.

이것은 일반적으로 파트너 프로그램의 이용 약관 위반으로 인한 것입니다.

이 결정이 오류라고 생각하거나 논의하고 싶으시면, 지원팀에 연락 주세요.

{{ shop_name }}
질문이 있으십니까? {{ support_email }}에 문의하세요.