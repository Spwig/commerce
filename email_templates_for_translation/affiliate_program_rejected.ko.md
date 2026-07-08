---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
프로그램 신청 상태 변경

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
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          신청 상태 변경
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          안녕하세요 {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ program_name }}을(를) 홍보하기 위해 신청해 주셔서 감사합니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          신청서를 검토한 후, 현재는 승인하지 않기로 결정했습니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          우리 파트너 네트워크의 다른 프로그램을 계속 홍보할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          다른 프로그램 보기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          궁금한 점이 있나요? <a href="mailto:{{ support_email }}" style="color: #007bff;">지원팀에 문의</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
프로그램 신청 상태 변경

안녕하세요 {{ affiliate_name }},

{{ program_name }}을(를) 홍보하기 위해 신청해 주셔서 감사합니다.

신청서를 검토한 후, 현재는 승인하지 않기로 결정했습니다.

우리 파트너 네트워크의 다른 프로그램을 계속 홍보할 수 있습니다.

다른 프로그램 보기: {{ portal_url }}

{{ shop_name }}
궁금한 점이 있나요? {{ support_email }}에 문의하세요