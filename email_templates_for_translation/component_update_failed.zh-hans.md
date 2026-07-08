---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ 更新失败：{{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ 更新失败
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          安装错误
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          将 {{ component_name }} 更新到版本 {{ target_version }} 的安装失败。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              故障详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>组件：</strong> {{ component_name }}<br/>
              <strong>目标版本：</strong> {{ target_version }}<br/>
              <strong>失败时间：</strong> {{ failed_at }}<br/>
              <strong>错误代码：</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          错误信息：
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>完整错误日志：</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:50 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          应该怎么做：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 检查系统要求和依赖项<br/>
          2. 查看错误日志以获取详细信息<br/>
          3. 再次尝试安装，或联系支持<br/>
          4. 您的商店仍在使用 {{ current_version }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          重试安装
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          联系支持
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ 更新失败

安装错误

将 {{ component_name }} 更新到版本 {{ target_version }} 的安装失败。

故障详情：
- 组件：{{ component_name }}
- 目标版本：{{ target_version }}
- 失败时间：{{ failed_at }}
- 错误代码：{{ error_code }}

错误信息：
{{ error_message }}

{% if error_log %}
完整错误日志：
{{ error_log|truncatewords:50 }}
{% endif %}

应该怎么做：
1. 检查系统要求和依赖项
2. 查看错误日志以获取详细信息
3. 再次尝试安装，或联系支持
4. 您的商店仍在使用 {{ current_version }}

重试安装：{{ retry_url }}
联系支持：{{ support_url }}