---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
需要操作 - {{ store_name }} 的商店設置問題

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
          商店設置問題
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
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          我們在設置您的商店 <strong>{{ store_name }}</strong> 時遇到了問題。我們的團隊已經收到通知，正在處理中。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          發生了什麼
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
          接下來會發生什麼？
        </mj-text>
        <mj-text font-size="14px">
          我們的支援團隊已經自動收到此問題的通知。您不需要採取任何行動 - 一旦問題解決，我們會聯繫您。
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          如果您有任何問題，請隨時聯繫我們。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
商店設置問題 - {{ store_name }}

Hi {{ name|default:'there' }},

我們在設置您的商店 {{ store_name }} 時遇到了問題。我們的團隊已經收到通知，正在處理中。

發生了什麼：
{{ provision_error }}

接下來會發生什麼？
我們的支援團隊已經自動收到此問題的通知。您不需要採取任何行動 - 一旦問題解決，我們會聯繫您。

如果您有任何問題，請隨時聯繫我們。

需要幫助嗎？請聯繫 {{ support_email }}