---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
중요: 7일 내 데이터 삭제 - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          데이터 삭제 경고
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
          안녕하세요, {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          귀하의 스토어 <strong>{{ store_name }}</strong> 및 관련된 모든 데이터는 <strong>{{ termination_date }}</strong>에 영구적으로 삭제됩니다. 이 작업은 되돌릴 수 없습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          할 수 있는 일
        </mj-text>
        <mj-text font-size="14px">
          데이터를 보관하고 싶으시면, 이 날짜 이전에 데이터를 내보내거나 구독을 재활성화하여 삭제를 방지할 수 있습니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="구독 재활성화" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
데이터 삭제 경고 - {{ store_name }}

안녕하세요, {{ name|default:'there' }},

귀하의 스토어 {{ store_name }} 및 관련된 모든 데이터는 {{ termination_date }}에 영구적으로 삭제됩니다. 이 작업은 되돌릴 수 없습니다.

할 수 있는 일:
데이터를 보관하고 싶으시면, 이 날짜 이전에 데이터를 내보내거나 구독을 재활성화하여 삭제를 방지할 수 있습니다.

구독 재활성화: https://spwig.com/account

도움이 필요하신가요? {{ support_email }}로 문의해 주세요.