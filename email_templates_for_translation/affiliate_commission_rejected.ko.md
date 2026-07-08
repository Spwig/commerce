---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
커미션 상태 업데이트 - 주문 #{{ order_number }}

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
          커미션 상태 업데이트
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
          주문 #{{ order_number }} ({{ commission_amount }})의 커미션이 승인되지 않았음을 알려드립니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          이는 일반적으로 커미션 기간이 끝나기 전에 주문이 취소되거나 환불되었을 때 발생합니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          이 커미션에 대해 궁금한 점이 있는 경우 지원팀에 문의해 주세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          대시보드 보기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          질문이 있습니까? <a href="mailto:{{ support_email }}" style="color: #007bff;">지원팀에 문의</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
커미션 상태 업데이트 - 주문 #{{ order_number }}

안녕하세요 {{ affiliate_name }},

주문 #{{ order_number }} ({{ commission_amount }})의 커미션이 승인되지 않았음을 알려드립니다.

이것은 일반적으로 커미션 기간이 끝나기 전에 주문이 취소되거나 환불되었을 때 발생합니다.

이 커미션에 대해 궁금한 점이 있는 경우 지원팀에 문의해 주세요.

대시보드 보기: {{ portal_url }}

{{ shop_name }}
질문이 있습니까? {{ support_email }}에 문의하세요.