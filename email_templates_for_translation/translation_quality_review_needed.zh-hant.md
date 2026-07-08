---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ 發現低品質翻譯：{{ content_type }} - {{ low_quality_count }} 項需要審核

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 翻譯品質警示
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建議審核
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          您的翻譯工作已完成，但 {{ low_quality_count }} 個翻譯分數低於品質門檻，應在發布前進行審核。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              工作摘要：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>工作 ID：</strong> {{ job_id }}<br/>
              <strong>內容類型：</strong> {{ content_type }}<br/>
              <strong>總項目數：</strong> {{ total_items }}<br/>
              <strong>平均品質：</strong> {{ average_quality }}%<br/>
              <strong>低品質：</strong> {{ low_quality_count }} 個項目（{{ low_quality_percentage }}%）
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          品質分佈：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>優秀 (95-100%)：</strong> {{ excellent_count }} 個項目<br/>
              <strong>良好 (85-94%)：</strong> {{ good_count }} 個項目<br/>
              <strong>普通 (70-84%)：</strong> {{ fair_count }} 個項目<br/>
              <strong>劣質 (&lt;70%)：</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} 個項目</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          常見品質問題：
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}：</strong> {{ issue.count }} 次數
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建議措施：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 在管理面板中審核標記的翻譯<br/>
          2. 手動編輯低品質翻譯<br/>
          3. 考慮重新翻譯品質差的項目<br/>
          4. 審核完成後再發布
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          審核翻譯
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看低品質項目
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 小提示：品質分數低於 85% 表示可能存在語法、語境或準確性方面的問題。發布前強烈建議進行人工審核。
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 翻譯品質警示

建議審核

您的翻譯工作已完成，但 {{ low_quality_count }} 個翻譯分數低於品質門檻，應在發布前進行審核。

JOB SUMMARY:
- 工作 ID：{{ job_id }}
- 內容類型：{{ content_type }}
- 總項目數：{{ total_items }}
- 平均品質：{{ average_quality }}%
- 低品質：{{ low_quality_count }} 個項目 ({{ low_quality_percentage }}%)

QUALITY BREAKDOWN:
- 優秀 (95-100%)：{{ excellent_count }} 個項目
- 良好 (85-94%)：{{ good_count }} 個項目
- 普通 (70-84%)：{{ fair_count }} 個項目
- 劣質 (<70%)：{{ poor_count }} 個項目

COMMON QUALITY ISSUES:
{% for issue in quality_issues %}
{{ issue.type }}：{{ issue.count }} 次數
{% endfor %}

RECOMMENDED ACTIONS:
1. 在管理面板中審核標記的翻譯
2. 手動編輯低品質翻譯
3. 考慮重新翻譯品質差的項目
4. 審核完成後再發布

審核翻譯：{{ review_url }}
查看低品質項目：{{ low_quality_url }}

💡 小提示：品質分數低於 85% 表示可能存在語法、語境或準確性方面的問題。發布前強烈建議進行人工審核。