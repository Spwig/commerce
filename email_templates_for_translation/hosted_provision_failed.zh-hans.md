---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
需要操作 - {{ store_name }} 的商店设置问题

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
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          商店设置问题
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
          你好 {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          在设置你的商店 <strong>{{ store_name }}</strong> 时，我们遇到了一个问题。我们的团队已经收到通知，并正在处理。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          发生了什么
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          接下来会发生什么？
        </mj-text>
        <mj-text font-size="14px">
          我们的支持团队已自动收到此问题的通知。你不需要采取任何操作 - 问题解决后，我们会联系你。
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          如果你有任何问题，请随时联系我们。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
商店设置问题 - {{ store_name }}

你好 {{ name|default:'there' }},

在设置你的商店 {{ store_name }} 时，我们遇到了一个问题。我们的团队已经收到通知，并正在处理。

发生了什么：
{{ provision_error }}

接下来会发生什么？
我们的支持团队已自动收到此问题的通知。你不需要采取任何操作 - 问题解决后，我们会联系你。

如果你有任何问题，请随时联系我们。

需要帮助？请联系 {{ support_email }}