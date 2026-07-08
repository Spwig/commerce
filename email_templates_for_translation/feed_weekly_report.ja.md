---
template_type: feed_weekly_report
category: Product Feeds
---

# Email Template: feed_weekly_report

## Subject
📊 週次の商品フィードレポート - {{ week_range }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 週次のフィードパフォーマンス
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          フィードパフォーマンス概要
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ week_range }} における商品フィードのパフォーマンスは以下の通りです。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          総合統計:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>総フィード数:</strong> {{ total_feeds }}<br/>
              <strong>アクティブフィード数:</strong> {{ active_feeds }}<br/>
              <strong>総同期数:</strong> {{ total_syncs }}<br/>
              <strong>成功した同期数:</strong> {{ successful_syncs }} ({{ success_rate }}%)<br/>
              <strong>失敗した同期数:</strong> {{ failed_syncs }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          フィードごとのパフォーマンス:
        </mj-text>

        {% for feed in feed_stats %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ feed.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              プラットフォーム: {{ feed.platform }}<br/>
              同期数: {{ feed.sync_count }} ({{ feed.success_count }} 成功)<br/>
              商品数: {{ feed.product_count }}<br/>
              {% if feed.errors > 0 %}エラー: {{ feed.errors }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if top_errors %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          最も一般的な問題:
        </mj-text>
        {% for error in top_errors %}
        <mj-section background-color="#fef3c7" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e">
              <strong>{{ error.type }}:</strong> {{ error.count }} 件
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}
        {% endif %}

        <mj-spacer height="30px" />

        {% if recommendations %}
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold">
              💡 おすすめ
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ feeds_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          フィードダッシュボードを表示
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 週次のフィードパフォーマンス

フィードパフォーマンス概要

{{ week_range }} における商品フィードのパフォーマンスは以下の通りです。

総合統計:
- 総フィード数: {{ total_feeds }}
- アクティブフィード数: {{ active_feeds }}
- 総同期数: {{ total_syncs }}
- 成功した同期数: {{ successful_syncs }} ({{ success_rate }}%)
- 失敗した同期数: {{ failed_syncs }}

フィードごとのパフォーマンス:
{% for feed in feed_stats %}
{{ feed.name }}
プラットフォーム: {{ feed.platform }}
同期数: {{ feed.sync_count }} ({{ feed.success_count }} 成功)
商品数: {{ feed.product_count }}
{% if feed.errors > 0 %}エラー: {{ feed.errors }}{% endif %}

{% endfor %}

{% if top_errors %}
最も一般的な問題:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} 件
{% endfor %}
{% endif %}

{% if recommendations %}
💡 おすすめ:
{{ recommendations }}
{% endif %}

フィードダッシュボードを表示: {{ feeds_dashboard_url }}