---
template_type: system_health_recovered
category: System Health
---

# Email Template: system_health_recovered

## Subject
✓ 已解決：{{ metric_name }} 已恢復正常

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ 已解決問題
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          系統健康狀況已恢復
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          好消息！{{ metric_name }} 的系統健康問題已經解決。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              恢復詳情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>指標：</strong> {{ metric_name }}<br/>
              <strong>目前值：</strong> <span style="color: #059669; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>正常閾值：</strong> {{ normal_threshold }}<br/>
              <strong>發現問題：</strong> {{ issue_detected_at }}<br/>
              <strong>已恢復：</strong> {{ recovered_at }}<br/>
              <strong>持續時間：</strong> {{ issue_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              ✓ 系統狀態：正常
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ metric_name }} 已恢復到正常水平，並在可接受的參數範圍內運行。
            </mj-text>
          </mj-column>
        </mj-section>

        {% if resolution_summary %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          解決方案摘要：
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ resolution_summary }}
        </mj-text>
        {% endif %}

        {% if actions_taken %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          已採取的措施：
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ actions_taken }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if preventive_measures %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          預防措施：
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ preventive_measures }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看系統儀表板
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看事故報告
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 已解決

系統健康狀況已恢復

好消息！{{ metric_name }} 的系統健康問題已經解決。

恢復詳情：
- 指標：{{ metric_name }}
- 目前值：{{ current_value }}
- 正常閾值：{{ normal_threshold }}
- 發現問題：{{ issue_detected_at }}
- 已恢復：{{ recovered_at }}
- 持續時間：{{ issue_duration }}

✓ 系統狀態：正常
{{ metric_name }} 已恢復到正常水平，並在可接受的參數範圍內運行。

{% if resolution_summary %}
解決方案摘要：
{{ resolution_summary }}
{% endif %}

{% if actions_taken %}
已採取的措施：
{{ actions_taken }}
{% endif %}

{% if preventive_measures %}
預防措施：
{{ preventive_measures }}
{% endif %}

查看系統儀表板：{{ dashboard_url }}
{% if incident_report_url %}查看事故報告：{{ incident_report_url }}{% endif %}