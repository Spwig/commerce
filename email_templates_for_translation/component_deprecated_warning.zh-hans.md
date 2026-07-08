---
template_type: component_deprecated_warning
category: Component Updates
---

# Email Template: component_deprecated_warning

## Subject
⚠️ {{ component_name }} 将于 {{ deprecation_date }} 停用

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 停用通知
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          组件即将停用
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} 将被停用，不再推荐使用。请计划迁移至其他解决方案。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              停用时间表：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>组件：</strong> {{ component_name }}<br/>
              <strong>当前版本：</strong> {{ current_version }}<br/>
              <strong>停用日期：</strong> {{ deprecation_date }}<br/>
              <strong>支持结束日期：</strong> {{ end_of_support_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          停用原因：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ deprecation_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          这意味着：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 该组件将在 {{ end_of_support_date }} 前继续正常工作<br/>
          • 不会添加新功能<br/>
          • 支持结束前将提供安全更新<br/>
          • 支持结束后，该组件将不再接收更新
        </mj-text>

        {% if recommended_alternative %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          推荐替代方案：
        </mj-text>
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              {{ alternative_name }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ alternative_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if migration_guide %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ migration_guide }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">查看迁移指南</a>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        {% if alternative_url %}
        <mj-button href="{{ alternative_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看替代方案
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          联系支持
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 停用通知

组件即将停用

{{ component_name }} 将被停用，不再推荐使用。请计划迁移至其他解决方案。

停用时间表：
- 组件：{{ component_name }}
- 当前版本：{{ current_version }}
- 停用日期：{{ deprecation_date }}
- 支持结束日期：{{ end_of_support_date }}

停用原因：
{{ deprecation_reason }}

这意味着：
• 该组件将在 {{ end_of_support_date }} 前继续正常工作
• 不会添加新功能
• 支持结束前将提供安全更新
• 支持结束后，该组件将不再接收更新

{% if recommended_alternative %}
推荐替代方案：
{{ alternative_name }}
{{ alternative_description }}
{% endif %}

{% if migration_guide %}查看迁移指南： {{ migration_guide }}{% endif %}
{% if alternative_url %}查看替代方案： {{ alternative_url }}{% endif %}
联系支持： {{ support_url }}