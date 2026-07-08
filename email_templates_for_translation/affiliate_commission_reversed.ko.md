---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
커미션 환불 - 주문 #{{ order_number }}

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
          커미션 환불
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
          고객의 환불로 인해 주문 #{{ order_number }} ({{ commission_amount }})의 커미션이 환불되었습니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          고객이 환불을 요청할 경우, 관련된 커미션은 정확한 회계를 위해 자동으로 환불됩니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          이는 아フィ리에이트 프로세스의 일반적인 부분입니다. {{ shop_name }}을 계속해서 홍보하여 새로운 커미션을 얻으세요!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          대시보드 보기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          문의 사항이 있으시면 <a href="mailto:{{ support_email }}" style="color: #007bff;">지원팀에 연락하세요</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
커미션 환불 - 주문 #{{ order_number }}

안녕하세요 {{ affiliate_name }},

고객의 환불로 인해 주문 #{{ order_number }} ({{ commission_amount }})의 커미션이 환불되었습니다.

고객이 환불을 요청할 경우, 관련된 커미션은 정확한 회계를 위해 자동으로 환불됩니다.

이것은 아피리에이트 프로세스의 일반적인 부분입니다. {{ shop_name }}을 계속해서 홍보하여 새로운 커미션을 얻으세요!

대시보드 보기: {{ portal_url }}

{{ shop_name }}
문의 사항이 있으시면 {{ support_email }}에 연락하세요