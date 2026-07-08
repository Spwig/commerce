---
template_type: translation_quality_review_needed
category: Translation Service
---

# Email Template: translation_quality_review_needed

## Subject
⚠️ 检测到低质量翻译：{{ content_type }} - {{ low_quality_count }} 项需要审核

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 翻译质量提醒
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建议审核
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          您的翻译任务已完成，但 {{ low_quality_count }} 个翻译得分低于质量阈值，发布前需要审核。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              任务摘要：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>任务 ID：</strong> {{ job_id }}<br/>
              <strong>内容类型：</strong> {{ content_type }}<br/>
              <strong>总项目数：</strong> {{ total_items }}<br/>
              <strong>平均质量：</strong> {{ average_quality }}%<br/>
              <strong>低质量：</strong> {{ low_quality_count }} 个项目 ({{ low_quality_percentage }}%)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          质量分析：
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>优秀 (95-100%)：</strong> {{ excellent_count }} 个项目<br/>
              <strong>良好 (85-94%)：</strong> {{ good_count }} 个项目<br/>
              <strong>一般 (70-84%)：</strong> {{ fair_count }} 个项目<br/>
              <strong>差 (&lt;70%)：</strong> <span style="color: #dc2626; font-weight: bold;">{{ poor_count }} 个项目</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          常见质量问题：
        </mj-text>

        {% for issue in quality_issues %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ issue.type }}：</strong> {{ issue.count }} 次出现
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建议操作：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 在管理面板中审核标记的翻译<br/>
          2. 手动编辑低质量的翻译<br/>
          3. 考虑重新翻译质量差的项目<br/>
          4. 审核完成后再发布
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          审核翻译
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ low_quality_url }}" background-color="#dc2626" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看低质量项目
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 提示：低于 85% 的质量得分可能表明存在语法、上下文或准确性方面的问题。发布前强烈建议进行人工审核。
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 翻译质量提醒

建议审核

您的翻译任务已完成，但 {{ low_quality_count }} 个翻译得分低于质量阈值，发布前需要审核。

任务摘要：
- 任务 ID：{{ job_id }}
- 内容类型：{{ content_type }}
- 总项目数：{{ total_items }}
- 平均质量：{{ average_quality }}%
- 低质量：{{ low_quality_count }} 个项目 ({{ low_quality_percentage }}%)

质量分析：
- 优秀 (95-100%)：{{ excellent_count }} 个项目
- 良好 (85-94%)：{{ good_count }} 个项目
- 一般 (70-84%)：{{ fair_count }} 个项目
- 差 (<70%)：{{ poor_count }} 个项目

常见质量问题：
{% for issue in quality_issues %}
{{ issue.type }}：{{ issue.count }} 次出现
{% endfor %}

建议操作：
1. 在管理面板中审核标记的翻译
2. 手动编辑低质量的翻译
3. 考虑重新翻译质量差的项目
4. 审核完成后再发布

审核翻译：{{ review_url }}
查看低质量项目：{{ low_quality_url }}

💡 提示：低于 85% 的质量得分可能表明存在语法、上下文或准确性方面的问题。发布前强烈建议进行人工审核。