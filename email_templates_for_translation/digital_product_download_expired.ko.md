---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
다운로드 링크 만료 - 주문 #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          다운로드 링크 만료
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          안녕하세요, {{ customer_name }},
        </mj-text>
        <mj-text>
          주문 #{{ order_number }}에서 {{ product_name }}의 다운로드 링크가 만료되었습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          보안상 이유로 구매 후 {{ expiration_days }}일 후 다운로드 링크가 만료됩니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          새 다운로드 링크가 필요하신가요?
        </mj-text>
        <mj-text>
          계정에 로그인하거나 지원팀에 문의하여 새 다운로드 링크를 요청할 수 있습니다.
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          마이 계정으로 이동
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          궁금한 점이 있나요? {{ support_email }}로 문의해 주세요
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
다운로드 링크 만료

안녕하세요, {{ customer_name }},

주문 #{{ order_number }}에서 {{ product_name }}의 다운로드 링크가 만료되었습니다.

다운로드 링크는 보안상 이유로 구매 후 {{ expiration_days }}일 후 만료됩니다.

새 다운로드 링크가 필요하신가요?
계정에 로그인하거나 지원팀에 문의하여 새 다운로드 링크를 요청할 수 있습니다.

마이 계정으로 이동: {{ account_url }}

궁금한 점이 있나요? {{ support_email }}로 문의해 주세요