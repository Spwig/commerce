---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ 翻譯工作失敗：{{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ 翻譯工作失敗
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          翻譯錯誤
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          您的批量翻譯工作遇到了錯誤，無法完成。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              工作詳情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>工作 ID：</strong> {{ job_id }}<br/>
              <strong>內容類型：</strong> {{ content_type }}<br/>
              <strong>目標語言：</strong> {{ target_languages }}<br/>
              <strong>失敗時間：</strong> {{ failed_at }}<br/>
              <strong>錯誤代碼：</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          錯誤訊息：
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
              在錯誤發生之前，{{ items_completed }} 個 {{ total_items }} 個項目已成功翻譯。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          常見原因：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 翻譯服務 API 連接問題<br/>
          • 翻譯信用額度不足<br/>
          • 無效或損壞的源內容<br/>
          • 不支持的語言對
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建議操作：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 檢查您的翻譯服務設置<br/>
          2. 確認翻譯信用額度可用<br/>
          3. 檢查錯誤訊息以了解具體問題<br/>
          4. 重試翻譯工作
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          重試翻譯
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          檢查設置
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          如果問題仍然存在，請聯繫支援並提供錯誤代碼 {{ error_code }}。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ 翻譯工作失敗

翻譯錯誤

您的批量翻譯工作遇到了錯誤，無法完成。

工作詳情：
- 工作 ID：{{ job_id }}
- 內容類型：{{ content_type }}
- 目標語言：{{ target_languages }}
- 失敗時間：{{ failed_at }}
- 錯誤代碼：{{ error_code }}

錯誤訊息：
{{ error_message }}

{% if partial_completion %}
部分完成：
{{ items_completed }} 個 {{ total_items }} 個項目在錯誤發生前已成功翻譯。
{% endif %}

常見原因：
• 翻譯服務 API 連接問題
• 翻譯信用額度不足
• 無效或損壞的源內容
• 不支持的語言對

建議操作：
1. 檢查您的翻譯服務設置
2. 確認翻譯信用額度可用
3. 檢查錯誤訊息以了解具體問題
4. 重試翻譯工作

重試翻譯：{{ retry_url }}
檢查設置：{{ settings_url }}

如果問題仍然存在，請聯繫支援並提供錯誤代碼 {{ error_code }}。