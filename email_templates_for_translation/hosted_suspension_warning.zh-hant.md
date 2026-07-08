---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
需採取行動 - {{ store_name }}

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
          懸掛警告
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          需採取行動：{{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          您的 {{ plan_name }} 計劃付款已逾期。若在 {{ grace_end_date }} 前未解決，您的商店將被設為唯讀模式。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          懸掛的意義
        </mj-text>
        <mj-text font-size="14px">
          如果您的商店被暫停，它將對訪客仍然可見，但您將無法進行任何更改。新訂單將會暫停，直到結清所有欠款。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          請更新您的付款方式，以避免對您的商店造成任何中斷。
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
懸掛警告 - {{ store_name }}

Hi {{ name|default:'there' }},

您的 {{ plan_name }} 付款已逾期。若在 {{ grace_end_date }} 前未解決，您的商店將被設為唯讀模式。

懸掛的意義：
如果您的商店被暫停，它將對訪客仍然可見，但您將無法進行任何更改。新訂單將會暫停，直到結清所有欠款。

請更新您的付款方式，以避免對您的商店造成任何中斷。

更新付款方式：https://spwig.com/account

需要幫助嗎？請聯繫 {{ support_email }}