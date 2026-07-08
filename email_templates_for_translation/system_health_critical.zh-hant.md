---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 關鍵警報：{{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 關鍵系統警報
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          需立即處理
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          在您的 Spwig 安裝上偵測到關鍵的系統健康問題。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 關鍵問題
            </mj-text>
            <mj-text color="#991b1b">
              <strong>指標：</strong> {{ metric_name }}<br/>
              <strong>目前值：</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>關鍵門檻：</strong> {{ critical_threshold }}<br/>
              <strong>偵測時間：</strong> {{ detected_at }}<br/>
              <strong>嚴重程度：</strong> 關鍵
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          影響：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          需立即採取的措施：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          趨勢：
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ trend_data }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 服務降級警告
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              這個問題可能會導致服務中斷或性能降級。立即處理以防止對客戶造成影響。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看系統儀表板
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          查看系統日誌
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 關鍵系統警報

需立即處理

在您的 Spwig 安裝上偵測到關鍵的系統健康問題。

🚨 關鍵問題：
- 指標：{{ metric_name }}
- 目前值：{{ current_value }}
- 關鍵門檻：{{ critical_threshold }}
- 偵測時間：{{ detected_at }}
- 嚴重程度：關鍵

影響：
{{ impact_description }}

需立即採取的措施：
{{ recommended_actions }}

{% if trend_data %}
趨勢：
{{ trend_data }}
{% endif %}

⚠️ 服務降級警告：
這個問題可能會導致服務中斷或性能降級。立即處理以防止對客戶造成影響。

查看系統儀表板：{{ dashboard_url }}
查看系統日誌：{{ logs_url }}