---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
有更新：{{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 有更新
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          新版本可用
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          您的 Spwig 商店可以使用 {{ component_name }} 的新版本。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              更新详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>组件：</strong> {{ component_name }}<br/>
              <strong>当前版本：</strong> {{ current_version }}<br/>
              <strong>新版本：</strong> {{ new_version }}<br/>
              <strong>发布日期：</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          新增功能：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 重大变更
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          安装更新
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">
            查看完整更新日志
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 更新可用

新版本可用

您的 Spwig 商店可以使用 {{ component_name }} 的新版本。

更新详情：
- 组件：{{ component_name }}
- 当前版本：{{ current_version }}
- 新版本：{{ new_version }}
- 发布日期：{{ release_date }}

新增功能：
{{ changelog }}

{% if breaking_changes %}
⚠️ 重大变更：
{{ breaking_changes }}
{% endif %}

安装更新：{{ update_url }}
查看完整更新日志：{{ changelog_url }}