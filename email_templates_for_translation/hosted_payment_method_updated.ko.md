---
template_type: hosted_payment_method_updated
category: License
---

# Email Template: hosted_payment_method_updated

## Subject
결제 수단이 업데이트되었습니다 - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          결제 수단이 업데이트되었습니다
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          안녕하세요,
        </mj-text>
        <mj-text>
          {{ store_name }}의 <strong>{{ plan_name }}</strong> 플랜에 대한 결제 수단이 성공적으로 업데이트되었습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Security Notice -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          이 변경을 하지 않았나요?
        </mj-text>
        <mj-text font-size="14px">
          결제 수단을 업데이트하지 않았다면, 계정을 보호하기 위해 즉시 지원팀에 연락해 주세요.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
결제 수단이 업데이트되었습니다 - {{ store_name }}

안녕하세요,

{{ store_name }}의 {{ plan_name }} 플랜에 대한 결제 수단이 성공적으로 업데이트되었습니다.

이 변경을 하지 않았나요?
결제 수단을 업데이트하지 않았다면, 계정을 보호하기 위해 즉시 지원팀에 연락해 주세요.

Go to Your Store: {{ admin_url }}

Need help? Contact {{ support_email }}