---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 重大なアラート: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 重大なシステムアラート
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          即時対応が必要です
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          あなたのSpwigインストールに重大なシステムヘルスの問題が検出されました。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 重大な問題
            </mj-text>
            <mj-text color="#991b1b">
              <strong>メトリクス:</strong> {{ metric_name }}<br/>
              <strong>現在値:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>重大閾値:</strong> {{ critical_threshold }}<br/>
              <strong>検出日時:</strong> {{ detected_at }}<br/>
              <strong>深刻度:</strong> 重大
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          影響:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          即時対応が必要な措置:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          トレンド:
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
              ⚠️ サービス劣化警告
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              この問題は、サービスの中断やパフォーマンスの劣化を引き起こす可能性があります。顧客への影響を防ぐために、すぐに処理してください。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          システムダッシュボードを表示
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          システムログを表示
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 重大なシステムアラート

即時対応が必要です

あなたのSpwigインストールに重大なシステムヘルスの問題が検出されました。

🚨 重大な問題:
- メトリクス: {{ metric_name }}
- 現在値: {{ current_value }}
- 重大閾値: {{ critical_threshold }}
- 検出日時: {{ detected_at }}
- 紛乱度: 重大

影響:
{{ impact_description }}

即時対応が必要な措置:
{{ recommended_actions }}

{% if trend_data %}
トレンド:
{{ trend_data }}
{% endif %}

⚠️ サービス劣化警告:
この問題は、サービスの中断やパフォーマンスの劣化を引き起こす可能性があります。顧客への影響を防ぐために、すぐに処理してください。

システムダッシュボードを表示: {{ dashboard_url }}
システムログを表示: {{ logs_url }}