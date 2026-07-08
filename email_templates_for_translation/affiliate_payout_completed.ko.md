---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ 지급 완료: {{ payout_amount }}

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
          🎉 지급 완료!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ 성공적으로 지급됨
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          지급 ID: {{ payout_id }}
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
          {{ payout_amount }}의 지급이 성공적으로 완료되었습니다!
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          자금이 귀하의 지급 방법으로 전송되었습니다. 귀하의 은행 또는 지급 처리업체에 따라 계좌에 나타나는 데 1~2 영업일이 소요될 수 있습니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ shop_name }}을 홍보해 주셔서 감사합니다. 계속해서 훌륭한 성과를 거두세요!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          지급 세부 정보 보기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          질문이 있습니까? <a href="mailto:{{ support_email }}" style="color: #007bff;">
            지원 담당자에게 문의하기
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 지급 완료: {{ payout_amount }}

안녕하세요 {{ affiliate_name }},

{{ payout_amount }}의 지급이 성공적으로 완료되었습니다!

지급 세부 정보:
- 지급 ID: {{ payout_id }}
- 금액: {{ payout_amount }}
- 지급 방법: {{ payout_method }}

자금이 귀하의 지급 방법으로 전송되었습니다. 귀하의 은행 또는 지급 처리업체에 따라 계좌에 나타나는 데 1~2 영업일이 소요될 수 있습니다.

{{ shop_name }}을 홍보해 주셔서 감사합니다. 계속해서 훌륭한 성과를 거두세요!

지급 세부 정보 보기: {{ portal_url }}

{{ shop_name }}
질문이 있습니까? {{ support_email }}에 문의하세요