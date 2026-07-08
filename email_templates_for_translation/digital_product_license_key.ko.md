---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
소프트웨어 라이선스 키 - 주문 #{{ order_number }}

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
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          라이선스 키가 준비되었습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          안녕하세요, {{ customer_name }}!
        </mj-text>
        <mj-text>
          {{ product_name }} 구매 감사합니다! 여기가 활성화를 위한 라이선스 키입니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          라이선스 키
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          복사하거나 신중하게 기록하세요
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          라이선스 정보:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 제품: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 버전: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 라이선스 유형: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 최대 활성화: {{ max_activations }} 대상
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 유효 기간: 평생 라이선스
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 유효 기한: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          활성화 방법:
        </mj-text>
        <mj-text font-size="14px">
          1. 소프트웨어를 다운로드하고 설치하세요
        </mj-text>
        <mj-text font-size="14px">
          2. 애플리케이션을 엽니다
        </mj-text>
        <mj-text font-size="14px">
          3. 프롬프트가 나타날 때 라이선스 키를 입력하세요
        </mj-text>
        <mj-text font-size="14px">
          4. "활성화"를 클릭하여 절차를 완료하세요
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          소프트웨어 다운로드
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ 주의:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 이 이메일을 안전하게 보관하세요 - 재설치 시 라이선스 키가 필요합니다
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 라이선스 키를 다른 사람과 공유하지 마세요
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • 계정 대시보드에서 장치를 비활성화할 수 있습니다
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          활성화 도움이 필요하신가요? {{ support_email }}로 문의하세요
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
라이선스 키가 준비되었습니다

안녕하세요, {{ customer_name }}!

{{ product_name }} 구매 감사합니다! 여기가 활성화를 위한 라이선스 키입니다.

라이선스 키:
{{ license_key }}

라이선스 정보:
• 제품: {{ product_name }}
• 버전: {{ product_version }}
• 라이선스 유형: {{ license_type }}
• 최대 활성화: {{ max_activations }} 대상
{% if is_lifetime %}• 유효 기간: 평생 라이선스{% else %}• 유효 기한: {{ expiration_date }}{% endif %}

활성화 방법:
1. 소프트웨어를 다운로드하고 설치하세요
2. 애플리케이션을 엽니다
3. 프롬프트가 나타날 때 라이선스 키를 입력하세요
4. "활성화"를 클릭하여 절차를 완료하세요

{% if download_url %}소프트웨어 다운로드: {{ download_url }}

{% endif %}주의:
• 이 이메일을 안전하게 보관하세요 - 재설치 시 라이선스 키가 필요합니다
• 라이선스 키를 다른 사람과 공유하지 마세요
• 계정 대시보드에서 장치를 비활성화할 수 있습니다

활성화 도움이 필요하신가요? {{ support_email }}로 문의하세요