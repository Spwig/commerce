---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ 翻译完成：{{ content_type }} ({{ language_count }} 种语言)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ 翻译完成！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          您的翻译已完成
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          好消息！您的批量翻译任务已成功完成。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              任务摘要：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>任务 ID：</strong> {{ job_id }}<br/>
              <strong>内容类型：</strong> {{ content_type }}<br/>
              <strong>语言：</strong> {{ target_languages }}<br/>
              <strong>已翻译项目：</strong> {{ items_translated }}<br/>
              <strong>总字数：</strong> {{ word_count }}<br/>
              <strong>完成时间：</strong> {{ completed_at }}<br/>
              <strong>耗时：</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          翻译质量：
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>平均质量评分：</strong> {{ quality_score }}%<br/>
              <strong>高质量：</strong> {{ high_quality_count }} 项<br/>
              <strong>建议审阅：</strong> {{ review_needed_count }} 项
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 建议审阅
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} 个翻译评分低于 85%，在发布前应进行审阅。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          下一步操作：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 在您的管理面板中审阅翻译<br/>
          2. 编辑需要改进的任何翻译<br/>
          3. 发布翻译以使其生效<br/>
          4. 您的多语言内容将向客户开放
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          审阅翻译
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          全部发布
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 翻译完成！

您的翻译已完成

好消息！您的批量翻译任务已成功完成。

任务摘要：
- 任务 ID：{{ job_id }}
- 内容类型：{{ content_type }}
- 语言：{{ target_languages }}
- 已翻译项目：{{ items_translated }}
- 总字数：{{ word_count }}
- 完成时间：{{ completed_at }}
- 耗时：{{ job_duration }}

翻译质量：
- 平均质量评分：{{ quality_score }}%
- 高质量：{{ high_quality_count }} 项
- 建议审阅：{{ review_needed_count }} 项

{% if review_needed_count > 0 %}
⚠️ 建议审阅：
{{ review_needed_count }} 个翻译评分低于 85%，在发布前应进行审阅。
{% endif %}

下一步操作：
1. 在您的管理面板中审阅翻译
2. 编辑需要改进的任何翻译
3. 发布翻译以使其生效
4. 您的多语言内容将向客户开放

审阅翻译：{{ review_url }}
{% if can_publish_all %}全部发布：{{ publish_all_url }}{% endif %}