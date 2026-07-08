---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
작업 필요: 지급 실패

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
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          ⚠️ 지급 실패
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          지급 ID: {{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          안녕하세요 {{ affiliate_name }}",
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ payout_amount }} 지급을 처리하는 데 문제가 발생했습니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          이는 일반적으로 잘못된 결제 정보 또는 결제 제공업체의 문제로 인해 발생합니다.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          협력업체 대시보드에서 결제 정보를 업데이트하고 지원팀에 문의하여 이 문제를 해결해 주세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          결제 정보 업데이트
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          도움이 필요하신가요? <a href="mailto:{{ support_email }}" style="color: #007bff;">지원팀에 문의</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
작업 필요: 지급 실패

안녕하세요 {{ affiliate_name }},

{{ payout_amount }} 지급을 처리하는 데 문제가 발생했습니다 (지급 ID: {{ payout_id }}).

이것은 일반적으로 잘못된 결제 정보 또는 결제 제공업체의 문제로 인해 발생합니다.

협력업체 대시보드에서 결제 정보를 업데이트하고 지원팀에 문의하여 이 문제를 해결해 주세요.

결제 정보 업데이트: {{ portal_url }}

{{ shop_name }}
도움이 필요하신가요? {{ support_email }}에 문의하세요.