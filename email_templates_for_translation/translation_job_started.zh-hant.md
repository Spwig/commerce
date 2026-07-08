---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 翻譯工作開始：{{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 翻譯工作開始
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          批量翻譯正在處理中
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          您的批量翻譯工作已經開始並正在處理中。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              工作細節：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>工作 ID：</strong>{{ job_id }}<br/>
              <strong>內容類型：</strong>{{ content_type }}<br/>
              <strong>來源語言：</strong>{{ source_language }}<br/>
              <strong>目標語言：</strong>{{ target_languages }}<br/>
              <strong>待翻譯項目：</strong>{{ item_count }}<br/>
              <strong>開始時間：</strong>{{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          預計完成時間：
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (基於 {{ word_count }} 個字)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          接下來會發生什麼：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. AI 翻譯服務處理您的內容<br/>
          2. 翻譯內容會以草稿形式保存供審閱<br/>
          3. 工作完成後您將收到一封電郵<br/>
          4. 從您的管理員面板審閱並發布翻譯
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看工作狀態
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          您可以關閉這封郵件。我們會在翻譯完成後通知您。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 翻譯工作開始

批量翻譯正在處理中

您的批量翻譯工作已經開始並正在處理中。

工作細節：
- 工作 ID：{{ job_id }}
- 內容類型：{{ content_type }}
- 來源語言：{{ source_language }}
- 目標語言：{{ target_languages }}
- 待翻譯項目：{{ item_count }}
- 開始時間：{{ started_at }}

預計完成時間：
{{ estimated_completion }}
(基於 {{ word_count }} 個字)

接下來會發生什麼：
1. AI 翻譯服務處理您的內容
2. 翻譯內容會以草稿形式保存供審閱
3. 工作完成後您將收到一封電郵
4. 從您的管理員面板審閱並發布翻譯

查看工作狀態：{{ job_status_url }}

您可以關閉這封郵件。我們會在翻譯完成後通知您。