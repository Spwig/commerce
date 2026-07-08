---
template_type: affiliate_commission_approved
category: Affiliate Program
---

# Email Template: affiliate_commission_approved

## Subject
수수료 승인됨: {{ commission_amount }}

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
          ✓ 수수료 승인됨!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Approval Display -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          지급 대기 중
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
          주문 #{{ order_number }}에서 발생한 수수료 {{ commission_amount }}이 승인되었으며, 다음 지급에 포함될 예정입니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          지급은 지불 일정에 따라 처리됩니다. 지급이 처리되면 이메일을 다시 받게 됩니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          수수료 보기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          질문이 있으십니까? <a href="mailto:{{ support_email }}" style="color: #007bff;">지원팀에 문의</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
수수료 승인됨: {{ commission_amount }}

안녕하세요 {{ affiliate_name }},

주문 #{{ order_number }}에서 발생한 수수료 {{ commission_amount }}이 승인되었으며, 다음 지급에 포함될 예정입니다.

지급은 지불 일정에 따라 처리됩니다. 지급이 처리되면 이메일을 다시 받게 됩니다.

수수료 보기: {{ portal_url }}

{{ shop_name }}
질문이 있으십니까? {{ support_email }}에 문의하세요