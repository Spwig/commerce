---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ 翻译任务失败: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ 翻译任务失败
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          翻译错误
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          您的批量翻译任务遇到错误，无法完成。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              任务详情:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>任务 ID:</strong> {{ job_id }}<br/>
              <strong>内容类型:</strong> {{ content_type }}<br/>
              <strong>目标语言:</strong> {{ target_languages }}<br/>
              <strong>失败时间:</strong> {{ failed_at }}<br/>
              <strong>错误代码:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          错误信息:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              部分完成
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              在发生错误之前，{{ items_completed }} 个 {{ total_items }} 个项目已成功翻译。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          常见原因:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 翻译服务 API 连接问题<br/>
          • 翻译积分不足<br/>
          • 无效或损坏的源内容<br/>
          • 不支持的语言对
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建议操作:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 检查翻译服务设置<br/>
          2. 确认有可用的翻译积分<br/>
          3. 查看错误信息以了解具体问题<br/>
          4. 重试翻译任务
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          重试翻译
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          检查设置
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          如果问题仍然存在，请使用错误代码 {{ error_code }} 联系支持。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ 翻译任务失败

翻译错误

您的批量翻译任务遇到错误，无法完成。

任务详情:
- 任务 ID: {{ job_id }}
- 内容类型: {{ content_type }}
- 目标语言: {{ target_languages }}
- 失败时间: {{ failed_at }}
- 错误代码: {{ error_code }}

错误信息:
{{ error_message }}

{% if partial_completion %}
部分完成:
{{ items_completed }} 个 {{ total_items }} 个项目已成功翻译。
{% endif %}

常见原因:
• 翻译服务 API 连接问题
• 翻译积分不足
• 无效或损坏的源内容
• 不支持的语言对

建议操作:
1. 检查翻译服务设置
2. 确认有可用的翻译积分
3. 查看错误信息以了解具体问题
4. 重试翻译任务

重试翻译: {{ retry_url }}
检查设置: {{ settings_url }}

如果问题仍然存在，请使用错误代码 {{ error_code }} 联系支持。