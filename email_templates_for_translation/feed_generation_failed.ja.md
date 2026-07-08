---
template_type: feed_generation_failed
category: Product Feeds
---

# Email Template: feed_generation_failed

## Subject
❌ チャンネル生成に失敗しました: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ チャンネル生成に失敗しました
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          生成エラー
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          エラーにより、{{ feed_name }} 製品チャンネルの生成に失敗しました。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              エラーの詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Failed At:</strong> {{ failed_at }}<br/>
              <strong>Error Code:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          エラーメッセージ:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Error Log:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:30 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          一般的な原因:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 必要な製品データが不足しています (タイトル、価格、画像)
          <br/>
          • 無効な製品データ形式
          <br/>
          • データベース接続の問題
          <br/>
          • 空間またはメモリが不足しています
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          生成を再試行
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          チャンネル設定を表示
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          問題が解決しない場合は、エラーコード {{ error_code }} を添えてサポートにお問い合わせください。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ チャンネル生成に失敗しました

生成エラー

{{ feed_name }} 製品チャンネルの生成はエラーにより失敗しました。

エラーの詳細:
- チャンネル: {{ feed_name }}
- 失敗した時間: {{ failed_at }}
- エラーコード: {{ error_code }}

エラーメッセージ:
{{ error_message }}

{% if error_log %}
エラーログ:
{{ error_log|truncatewords:30 }}
{% endif %}

一般的な原因:
• 必要な製品データが不足しています (タイトル、価格、画像)
• 無効な製品データ形式
• データベース接続の問題
• 空間またはメモリが不足しています

生成を再試行: {{ retry_url }}
チャンネル設定を表示: {{ admin_feed_url }}

問題が解決しない場合は、エラーコード {{ error_code }} を添えてサポートにお問い合わせください。