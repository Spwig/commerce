---
template_type: pos_terminal_offline
category: POS
---

# Email Template: pos_terminal_offline

## Subject
⚠️ POS 繫統終端機離線：{{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ 繫統終端機離線
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          POS 繫統終端機離線
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} 已離線，且不再回應。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              繫統資訊：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>繫統：</strong> {{ terminal_name }}<br/>
              <strong>位置：</strong> {{ location }}<br/>
              <strong>最後見到時間：</strong> {{ last_seen }}<br/>
              <strong>離線時間：</strong> {{ offline_since }}<br/>
              <strong>持續時間：</strong> {{ offline_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          常見原因：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 網絡連線問題<br/>
          • 繫統關機或重新啟動<br/>
          • 軟體當機或凍結<br/>
          • 網際網路服務中斷
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建議措施：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 檢查繫統電源和網絡連線<br/>
          2. 重新啟動繫統設備<br/>
          3. 確認網際網路連線<br/>
          4. 檢查防火牆和安全設定
        </mj-text>

        {% if active_shift %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 有活動班次警告
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              這個繫統目前有活動班次。重新連線之前，銷售資料可能不會同步。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_terminals_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看繫統狀態
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          繫統重新連線時，您將收到另一則通知。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 繫統終端機離線

POS 繫統終端機離線

{{ terminal_name }} 已離線，且不再回應。

繫統資訊：
- 繫統：{{ terminal_name }}
- 位置：{{ location }}
- 最後見到時間：{{ last_seen }}
- 離線時間：{{ offline_since }}
- 持續時間：{{ offline_duration }}

常見原因：
• 網絡連線問題
• 繫統關機或重新啟動
• 軟體當機或凍結
• 網際網路服務中斷

建議措施：
1. 檢查繫統電源和網絡連線
2. 重新啟動繫統設備
3. 確認網際網路連線
4. 檢查防火牆和安全設定

{% if active_shift %}
⚠️ 有活動班次警告：
這個繫統目前有活動班次。重新連線之前，銷售資料可能不會同步。
{% endif %}

查看繫統狀態：{{ admin_terminals_url }}

繫統重新連線時，您將收到另一則通知。