---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
需要操作 - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          暂停警告
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          需要操作 {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          你好 {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          你的 {{ plan_name }} 计划付款已逾期。如果在 {{ grace_end_date }} 之前未解决，你的商店将被设置为只读模式。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          暂停意味着什么
        </mj-text>
        <mj-text font-size="14px">
          如果你的商店被暂停，它对访客仍然可见，但你将无法进行更改。新订单将暂停，直到未结余额结清。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          请更新你的付款方式，以避免对商店造成任何干扰。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="更新付款方式" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
暂停警告 - {{ store_name }}

你好 {{ name|default:'there' }},

你的 {{ plan_name }} 付款已逾期。如果在 {{ grace_end_date }} 之前未解决，你的商店将被设置为只读模式。

暂停意味着什么：
如果商店被暂停，它对访客仍然可见，但你将无法进行更改。新订单将暂停，直到未结余额结清。

请更新你的付款方式，以避免对商店造成任何干扰。

更新付款方式：https://spwig.com/account

需要帮助？请联系 {{ support_email }}