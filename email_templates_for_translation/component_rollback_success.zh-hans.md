---
template_type: component_rollback_success
category: Component Updates
---

# Email Template: component_rollback_success

## Subject
✓ {{ component_name }} 回滚至 v{{ previous_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dbeafe">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          ↩️ 回滚完成
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          组件已恢复
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} 已成功回滚到上一个版本。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              回滚详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>组件：</strong> {{ component_name }}<br/>
              <strong>回滚来源：</strong> v{{ failed_version }}<br/>
              <strong>恢复至：</strong> v{{ previous_version }}<br/>
              <strong>完成时间：</strong> {{ completed_at }}<br/>
              <strong>持续时间：</strong> {{ rollback_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rollback_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          回滚原因：
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ rollback_reason }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ✓ 商店状态
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              您的商店现在正在使用稳定的版本 {{ previous_version }}。所有功能应该已恢复。
            </mj-text>
          </mj-column>
        </mj-section>

        {% if data_restored %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>数据恢复：</strong> {{ data_restoration_message }}
        </mj-text>
        {% endif %}

        {% if next_steps %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          下一步：
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ component_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看组件详情
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看事故报告
        </mj-button>
        {% endif %}

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          如果您继续遇到问题，请联系支持。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
↩️ 回滚完成

组件已恢复

{{ component_name }} 已成功回滚到上一个版本。

回滚详情：
- 组件： {{ component_name }}
- 回滚来源： v{{ failed_version }}
- 恢复至： v{{ previous_version }}
- 完成时间： {{ completed_at }}
- 持续时间： {{ rollback_duration }}

{% if rollback_reason %}
回滚原因：
{{ rollback_reason }}
{% endif %}

✓ 商店状态：
您的商店现在正在使用稳定的版本 {{ previous_version }}。所有功能应该已恢复。

{% if data_restored %}
数据恢复： {{ data_restoration_message }}
{% endif %}

{% if next_steps %}
下一步：
{{ next_steps }}
{% endif %}

查看组件详情： {{ component_url }}
{% if incident_report_url %}查看事故报告： {{ incident_report_url }}{% endif %}

如果您继续遇到问题，请联系支持。