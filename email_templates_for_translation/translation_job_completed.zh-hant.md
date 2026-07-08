---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ 翻譯完成：{{ content_type }} ({{ language_count }} 種語言)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ 翻譯完成！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          您的翻譯已準備好
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          好消息！您的批量翻譯工作已成功完成。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              工作摘要：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>工作 ID：</strong> {{ job_id }}<br/>
              <strong>內容類型：</strong> {{ content_type }}<br/>
              <strong>語言：</strong> {{ target_languages }}<br/>
              <strong>已翻譯項目：</strong> {{ items_translated }}<br/>
              <strong>總字數：</strong> {{ word_count }}<br/>
              <strong>完成時間：</strong> {{ completed_at }}<br/>
              <strong>持續時間：</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          翻譯品質：
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>平均品質分數：</strong> {{ quality_score }}%<br/>
              <strong>高品質：</strong> {{ high_quality_count }} 個項目<br/>
              <strong>建議審核：</strong> {{ review_needed_count }} 個項目
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 建議審核
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} 個翻譯得分低於 85%，發佈前應進行審核。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          下一步：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 在您的管理面板中審核翻譯<br/>
          2. 編輯需要改進的翻譯<br/>
          3. 發佈翻譯以使其生效<br/>
          4. 您的多語言內容將對客戶可用
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          審核翻譯
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          全部發佈
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 翻譯完成！

您的翻譯已準備好

好消息！您的批量翻譯工作已成功完成。

工作摘要：
- 工作 ID：{{ job_id }}
- 內容類型：{{ content_type }}
- 語言：{{ target_languages }}
- 已翻譯項目：{{ items_translated }}
- 總字數：{{ word_count }}
- 完成時間：{{ completed_at }}
- 持續時間：{{ job_duration }}

翻譯品質：
- 平均品質分數：{{ quality_score }}%
- 高品質：{{ high_quality_count }} 個項目
- 建議審核：{{ review_needed_count }} 個項目

{% if review_needed_count > 0 %}
⚠️ 建議審核：
{{ review_needed_count }} 個翻譯得分低於 85%，發佈前應進行審核。
{% endif %}

下一步：
1. 在您的管理面板中審核翻譯
2. 編輯需要改進的翻譯
3. 發佈翻譯以使其生效
4. 您的多語言內容將對客戶可用

審核翻譯：{{ review_url }}
{% if can_publish_all %}全部發佈：{{ publish_all_url }}{% endif %}