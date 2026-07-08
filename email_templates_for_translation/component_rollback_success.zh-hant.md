---
template_type: component_rollback_success
category: Component Updates
---

# Email Template: component_rollback_success

## Subject
✓ {{ component_name }} 回退至 v{{ previous_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dbeafe">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          ↩️ 回退完成
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          模組已恢復
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} 已成功回退到上一個版本。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              回退詳情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>模組：</strong> {{ component_name }}<br/>
              <strong>回退前版本：</strong> v{{ failed_version }}<br/>
              <strong>恢復版本：</strong> v{{ previous_version }}<br/>
              <strong>完成時間：</strong> {{ completed_at }}<br/>
              <strong>持續時間：</strong> {{ rollback_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rollback_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          回退原因：
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ rollback_reason }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ✓ 商店狀態
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              您的商店現在正在使用穩定版本 {{ previous_version }}。所有功能應已恢復。
            </mj-text>
          </mj-column>
        </mj-section>

        {% if data_restored %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>資料恢復：</strong> {{ data_restoration_message }}
        </mj-text>
        {% endif %}

        {% if next_steps %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          接下來的步驟：
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ component_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看模組詳情
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看事件報告
        </mj-button>
        {% endif %}

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          如果您繼續遇到問題，請聯繫支援。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
↩️ 回退完成

模組已恢復

{{ component_name }} 已成功回退到上一個版本。

回退詳情：
- 模組：{{ component_name }}
- 回退前版本：v{{ failed_version }}
- 恢復版本：v{{ previous_version }}
- 完成時間：{{ completed_at }}
- 持續時間：{{ rollback_duration }}

{% if rollback_reason %}
回退原因：
{{ rollback_reason }}
{% endif %}

✓ 商店狀態：
您的商店現在正在使用穩定版本 {{ previous_version }}。所有功能應已恢復。

{% if data_restored %}
資料恢復：{{ data_restoration_message }}
{% endif %}

{% if next_steps %}
接下來的步驟：
{{ next_steps }}
{% endif %}

查看模組詳情：{{ component_url }}
{% if incident_report_url %}查看事件報告：{{ incident_report_url }}{% endif %}

如果您繼續遇到問題，請聯繫支援。