---
template_type: system_health_recovered
category: System Health
---

# Email Template: system_health_recovered

## Subject
✓ {{ metric_name }} が通常に戻りました

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ 問題解決済み
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          システムの健康状態が回復しました
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          良いニュース！{{ metric_name }} に関連するシステムの健康状態の問題は解決されました。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              回復の詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>メトリクス:</strong> {{ metric_name }}<br/>
              <strong>現在の値:</strong> <span style="color: #059669; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>正常閾値:</strong> {{ normal_threshold }}<br/>
              <strong>問題検出日時:</strong> {{ issue_detected_at }}<br/>
              <strong>回復日時:</strong> {{ recovered_at }}<br/>
              <strong>継続時間:</strong> {{ issue_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              ✓ システム状態: 通常
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ metric_name }} は通常のレベルに戻り、許容可能なパラメータ内で動作しています。
            </mj-text>
          </mj-column>
        </mj-section>

        {% if resolution_summary %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          解決概要:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ resolution_summary }}
        </mj-text>
        {% endif %}

        {% if actions_taken %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          実施された対応:
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
          予防策:
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
          システムダッシュボードを表示
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          インシデントレポートを表示
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 問題解決済み

システムの健康状態が回復しました

良いニュース！{{ metric_name }} に関連するシステムの健康状態の問題は解決されました。

回復の詳細:
- メトリクス: {{ metric_name }}
- 現在の値: {{ current_value }}
- 正常閾値: {{ normal_threshold }}
- 問題検出日時: {{ issue_detected_at }}
- 回復日時: {{ recovered_at }}
- 継続時間: {{ issue_duration }}

✓ システム状態: 通常
{{ metric_name }} は通常のレベルに戻り、許容可能なパラメータ内で動作しています。

{% if resolution_summary %}
解決概要:
{{ resolution_summary }}
{% endif %}

{% if actions_taken %}
実施された対応:
{{ actions_taken }}
{% endif %}

{% if preventive_measures %}
予防策:
{{ preventive_measures }}
{% endif %}

システムダッシュボードを表示: {{ dashboard_url }}
{% if incident_report_url %}インシデントレポートを表示: {{ incident_report_url }}{% endif %}