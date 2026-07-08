---
template_type: affiliate_payout_processing
category: Affiliate Program
---

# Email Template: affiliate_payout_processing

## Subject
지급 금액 {{ payout_amount }}이 처리 중입니다

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
          💸 지급 처리 중
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#17a2b8" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          지급 처리 중
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
          안녕하세요 {{ affiliate_name }}님,
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          기쁜 소식이에요! {{ payout_amount }} 금액의 지급이 지금 처리 중입니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          자금은 귀하의 계좌에 3~5 영업일 내에 입금될 예정입니다. 지급이 완료되면 다시 이메일을 보내드릴게요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>지급 ID:</strong> {{ payout_id }}<br/>
          <strong>금액:</strong> {{ payout_amount }}<br/>
          <strong>결제 수단:</strong> {{ payout_method }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          지급 내역 보기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          궁금한 점이 있으면 <a href="mailto:{{ support_email }}" style="color: #007bff;">고객 지원에 문의하세요</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
지급 금액 {{ payout_amount }}이 처리 중입니다

안녕하세요 {{ affiliate_name }}님,

기쁜 소식이에요! {{ payout_amount }} 금액의 지급이 지금 처리 중입니다.

지급 세부 정보:
- 지급 ID: {{ payout_id }}
- 금액: {{ payout_amount }}
- 결제 수단: {{ payout_method }}

자금은 귀하의 계좌에 3~5 영업일 내에 입금될 예정입니다. 지급이 완료되면 다시 이메일을 보내드릴게요.

지급 내역 보기: {{ portal_url }}

{{ shop_name }}
궁금한 점이 있으면 {{ support_email }}에 문의하세요