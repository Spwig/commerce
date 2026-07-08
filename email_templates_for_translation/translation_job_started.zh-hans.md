---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 批量翻译任务已开始: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 批量翻译任务已开始
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          批量翻译正在进行中
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          您的批量翻译任务已经开始并正在处理中。
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
              <strong>源语言:</strong> {{ source_language }}<br/>
              <strong>目标语言:</strong> {{ target_languages }}<br/>
              <strong>待翻译项目:</strong> {{ item_count }}<br/>
              <strong>开始时间:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          预计完成时间:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (基于 {{ word_count }} 个词)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          接下来会发生什么:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. AI 翻译服务将处理您的内容<br/>
          2. 翻译内容将作为草稿保存以供审核<br/>
          3. 当任务完成后，您将收到一封电子邮件<br/>
          4. 通过您的管理面板审核并发布翻译内容
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看任务状态
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          您可以关闭这封邮件。当翻译完成时，我们会通知您。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 批量翻译任务已开始

批量翻译正在进行中

您的批量翻译任务已经开始并正在处理中。

任务详情:
- 任务 ID: {{ job_id }}
- 内容类型: {{ content_type }}
- 源语言: {{ source_language }}
- 目标语言: {{ target_languages }}
- 待翻译项目: {{ item_count }}
- 开始时间: {{ started_at }}

预计完成时间:
{{ estimated_completion }}
(基于 {{ word_count }} 个词)

接下来会发生什么:
1. AI 翻译服务将处理您的内容
2. 翻译内容将作为草稿保存以供审核
3. 当任务完成后，您将收到一封电子邮件
4. 通过您的管理面板审核并发布翻译内容

查看任务状态: {{ job_status_url }}

您可以关闭这封邮件。当翻译完成时，我们会通知您。