---
template_type: affiliate_program_approved
category: Affiliate Program
---

# Email Template: affiliate_program_approved

## Subject
승인됨 {{ program_name }}!

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
          ✓ 프로그램 승인됨!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          {{ program_name }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          승인되었습니다!
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
          기쁜 소식이 있습니다! {{ program_name }}을 홍보할 수 있는 자격을 얻었습니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          이 프로그램을 공유하여 수수료를 얻을 수 있습니다!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          협력업체 링크 받기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          질문이 있으십니까? <a href="mailto:{{ support_email }}" style="color: #007bff;">지원 담당자에게 문의</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
승인됨 {{ program_name }}!

안녕하세요 {{ affiliate_name }},

기쁜 소식이 있습니다! {{ program_name }}을 홍보할 수 있는 자격을 얻었습니다.

이 프로그램을 공유하여 수수료를 얻을 수 있습니다!

협력업체 링크 받기: {{ portal_url }}

{{ shop_name }}
질문이 있으십니까? {{ support_email }}에 문의하세요