---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
환영합니다! 계정이 다시 활성화되었습니다

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
          🎉 계정이 다시 활성화되었습니다!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          환영합니다!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          귀하의 파트너 계정이 다시 활성화되었습니다
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
          기쁜 소식입니다! {{ shop_name }}의 파트너 계정이 다시 활성화되었습니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          즉시 저희 제품을 홍보하고 수수료를 받을 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          파트너 대시보드에 접속
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          궁금한 점이 있나요? <a href="mailto:{{ support_email }}" style="color: #007bff;">제결지을 입력하줍</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
환영합니다! 계정이 다시 활성화되었습니다

안녕하세요, {{ affiliate_name }},

기쁜 소식입니다! {{ shop_name }}의 파트너 계정이 다시 활성화되었습니다.

즉시 저희 제품을 홍보하고 수수료를 받을 수 있습니다.

파트너 대시보드에 접속: {{ portal_url }}

{{ shop_name }}
궁금한 점이 있나요? {{ support_email }}에 문의하세요.