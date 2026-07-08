---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
지급 취소 - {{ payout_amount }}

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
          지급이 취소되었습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          안녕하세요, {{ affiliate_name }}님,
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ payout_amount }} (지급 ID: {{ payout_id }})의 지급이 취소되었습니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          이 지급이 취소된 이유에 대해 궁금하신 점이 있으면 지원 팀에 문의해 주세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          파트너 대시보드 보기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          궁금한 점이 있으면 <a href="mailto:{{ support_email }}" style="color: #007bff;">지원팀에 문의하세요</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
지급 취소 - {{ payout_amount }}

안녕하세요, {{ affiliate_name }}님,

{{ payout_amount }} (지급 ID: {{ payout_id }})의 지급이 취소되었습니다.

이 지급이 취소된 이유에 대해 궁금하신 점이 있으면 지원 팀에 문의해 주세요.

대시보드 보기: {{ portal_url }}

{{ shop_name }}
궁금한 점이 있으면 {{ support_email }}에 문의하세요