---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
당신은 {{ commission_amount }}의 수수료를 얻었습니다!

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
          💰 수수료를 얻었습니다!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          {{ shop_name }}에서 좋은 소식이 있어요
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 귀하의 수수료
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          주문 번호 #{{ order_number }}에서
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
          축하합니다! 주문 번호 #{{ order_number }}에서 {{ commission_amount }}의 수수료를 얻으셨습니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ shop_name }}을 계속해서 홍보하여 더 많은 수수료를 얻으세요. 판매가 많을수록 더 많이 얻을 수 있습니다!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Order Number:</strong> #{{ order_number }}<br/>
          <strong>Commission Amount:</strong> {{ commission_amount }}<br/>
          <strong>Commission Rate:</strong> {{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          마케터 대시보드 보기
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          궁금한 점이 있나요? <a href="mailto:{{ support_email }}" style="color: #007bff;">지원팀에 문의하기</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
당신은 {{ commission_amount }}의 수수료를 얻었습니다!

안녕하세요 {{ affiliate_name }}님,

축하합니다! 주문 번호 #{{ order_number }}에서 {{ commission_amount }}의 수수료를 얻으셨습니다.

수수료 정보:
- 주문 번호: #{{ order_number }}
- 수수료 금액: {{ commission_amount }}
- 수수료 비율: {{ commission_rate }}%

{{ shop_name }}을 계속해서 홍보하여 더 많은 수수료를 얻으세요.

대시보드 보기: {{ portal_url }}

{{ shop_name }}
궁금한 점이 있나요? {{ support_email }}에 문의하세요