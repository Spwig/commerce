---
template_type: feed_validation_errors
category: Product Feeds
---

# Email Template: feed_validation_errors

## Subject
⚠️ {{ feed_name }}: {{ error_count }} 검증 오류 발견

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Feed 검증 오류
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          데이터 품질 문제 발견
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ error_count }}개의 검증 오류가 {{ feed_name }}에 발견되었습니다. 이 문제는 {{ platform_name }}에 상품이 나타나지 않도록 할 수 있습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              검증 요약:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
              <strong>Validated:</strong> {{ validated_at }}<br/>
              <strong>Total Products:</strong> {{ total_products }}<br/>
              <strong>Products with Errors:</strong> {{ affected_products }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          주요 오류:
        </mj-text>

        {% for error in top_errors %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              {{ error.type }}
            </mj-text>
            <mj-text font-size="13px" color="#991b1b">
              {{ error.count }}개의 상품{{ error.count|pluralize }} 영향을 받았습니다: {{ error.message }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          수정해야 할 사항:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ fix_instructions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ errors_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          모든 오류 보기
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          피드 관리
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          이 오류를 수정하여 {{ platform_name }}에 모든 상품이 나타나도록 해주세요.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 피드 검증 오류

데이터 품질 문제 발견

{{ error_count }}개의 검증 오류가 {{ feed_name }}에 발견되었습니다. 이 문제는 {{ platform_name }}에 상품이 나타나지 않도록 할 수 있습니다.

검증 요약:
- 피드: {{ feed_name }}
- 플랫폼: {{ platform_name }}
- 검증 일시: {{ validated_at }}
- 전체 상품 수: {{ total_products }}
- 오류가 있는 상품: {{ affected_products }}

주요 오류:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }}개의 상품{{ error.count|pluralize }} - {{ error.message }}
{% endfor %}

수정해야 할 사항:
{{ fix_instructions }}

모든 오류 보기: {{ errors_url }}
피드 관리: {{ admin_feed_url }}

이 오류를 수정하여 {{ platform_name }}에 모든 상품이 나타나도록 해주세요.