---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 紧急：{{ component_name }} 的安全更新

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 安全更新必需
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          重要安全补丁
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          在 {{ component_name }} 中发现了一个安全漏洞。请立即更新以保护您的商店。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ 安全信息
            </mj-text>
            <mj-text color="#991b1b">
              <strong>组件:</strong> {{ component_name }}<br/>
              <strong>当前版本:</strong> {{ current_version }}<br/>
              <strong>已修复版本:</strong> {{ patched_version }}<br/>
              <strong>严重性:</strong> {{ severity_level }}<br/>
              <strong>CVE ID:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          漏洞详情:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          潜在影响:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              临时缓解措施
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          需要采取行动：立即安装更新
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          安装安全补丁
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          阅读安全公告
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          如果您需要帮助，请立即联系 Spwig 支持。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 安全更新必需

重要安全补丁

在 {{ component_name }} 中发现了一个安全漏洞。请立即更新以保护您的商店。

⚠️ 安全信息：
- 组件：{{ component_name }}
- 当前版本：{{ current_version }}
- 已修复版本：{{ patched_version }}
- 严重性：{{ severity_level }}
- CVE ID：{{ cve_id }}

漏洞详情：
{{ vulnerability_description }}

潜在影响：
{{ impact_description }}

{% if mitigation_steps %}
临时缓解措施：
{{ mitigation_steps }}
{% endif %}

需要采取行动：立即安装更新

安装安全补丁：{{ update_url }}
阅读安全公告：{{ advisory_url }}

如果您需要帮助，请立即联系 Spwig 支持。