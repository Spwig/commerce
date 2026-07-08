---
template_type: hosted_terminated
category: License
---

# Email Template: hosted_terminated

## Subject
店铺已移除 - {{ store_name }}

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
    <mj-section background-color="#374151" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          店铺已移除
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
          你的店铺 <strong>{{ store_name }}</strong> 已被永久移除。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Data Backup Info -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          数据备份
        </mj-text>
        <mj-text font-size="14px">
          你可以在请求后 90 天内获取数据备份。如需数据导出，请联系 <strong>support@spwig.com</strong>。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Thank You -->
    <mj-section>
      <mj-column>
        <mj-text>
          感谢您成为 Spwig 的客户。希望未来还能再次见到您。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
店铺已移除 - {{ store_name }}

你好 {{ name|default:'there' }},

你的店铺 {{ store_name }} 已被永久移除。

数据备份：
你可以在请求后 90 天内获取数据备份。如需数据导出，请联系 support@spwig.com。

感谢您成为 Spwig 的客户。希望未来还能再次见到您。

需要帮助？请联系 {{ support_email }}