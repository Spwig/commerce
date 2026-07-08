---
template_type: digital_product_delivery
category: Digital Products
---

# Email Template: digital_product_delivery

## Subject
디지털 제품이 준비되었습니다 - 주문 #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          디지털 제품이 준비되었습니다!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          안녕하세요 {{ customer_name }},
        </mj-text>
        <mj-text>
          구매 감사합니다! 디지털 제품이 이제 다운로드할 준비가 되었습니다.
        </mj-text>
        <mj-text font-weight="bold">
          주문 #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Product Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Version: {{ product_version }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          File Size: {{ file_size }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          지금 다운로드
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Important Information -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          <strong>중요 정보:</strong>
        </mj-text>
        {% if download_limit %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 이 제품을 {{ download_limit }}회 다운로드할 수 있습니다
        </mj-text>
        {% endif %}
        {% if expiration_days %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 다운로드 링크는 {{ expiration_days }}일 후 만료됩니다
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 향후 참조를 위해 이 이메일을 보관해 주세요
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          도움이 필요하시면 지원팀에 연락주세요: {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
디지털 제품이 준비되었습니다!

안녕하세요 {{ customer_name }},

구매 감사합니다! 디지털 제품이 이제 다운로드할 준비가 되었습니다.

주문 #{{ order_number }}

제품: {{ product_name }}
버전: {{ product_version }}
파일 크기: {{ file_size }}

제품을 여기에서 다운로드하세요:
{{ download_url }}

중요 정보:
{% if download_limit %}• 이 제품을 {{ download_limit }}회 다운로드할 수 있습니다
{% endif %}{% if expiration_days %}• 다운로드 링크는 {{ expiration_days }}일 후 만료됩니다
{% endif %}• 향후 참조를 위해 이 이메일을 보관해 주세요

도움이 필요하시면 지원팀에 연락주세요: {{ support_email }}