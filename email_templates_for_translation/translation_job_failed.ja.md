---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ 翻訳ジョブ失敗: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ 翻訳ジョブ失敗
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          翻訳エラー
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          あなたのバッチ翻訳ジョブはエラーに遭遇し、完了できませんでした。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ジョブ詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Target Languages:</strong> {{ target_languages }}<br/>
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

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              部分的な完了
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              エラーが発生する前までに、{{ items_completed }} / {{ total_items }} の項目が正常に翻訳されました。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          一般的な原因:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 翻訳サービスのAPI接続問題<br/>
          • 翻訳クレジットが不足しています<br/>
          • 無効または破損されたソースコンテンツ<br/>
          • 非対応の言語ペア
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          お勧めのアクション:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 翻訳サービスの設定を確認してください<br/>
          2. 翻訳クレジットが利用可能かどうかを確認してください<br/>
          3. エラーメッセージを確認して具体的な問題を特定してください<br/>
          4. 翻訳ジョブを再試行してください
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          翻訳を再試行
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          設定を確認
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          問題が継続する場合は、エラーコード {{ error_code }} とともにサポートに連絡してください。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ 翻訳ジョブ失敗

翻訳エラー

あなたのバッチ翻訳ジョブはエラーに遭遇し、完了できませんでした。

ジョブ詳細:
- ジョブID: {{ job_id }}
- コンテンツタイプ: {{ content_type }}
- 対象言語: {{ target_languages }}
- エラー発生時刻: {{ failed_at }}
- エラーコード: {{ error_code }}

エラーメッセージ:
{{ error_message }}

{% if partial_completion %}
部分的な完了:
{{ items_completed }} / {{ total_items }} の項目がエラー発生前に正常に翻訳されました。
{% endif %}

一般的な原因:
• 翻訳サービスのAPI接続問題
• 翻訳クレジットが不足しています
• 無効または破損されたソースコンテンツ
• 非対応の言語ペア

お勧めのアクション:
1. 翻訳サービスの設定を確認してください
2. 翻訳クレジットが利用可能かどうかを確認してください
3. エラーメッセージを確認して具体的な問題を特定してください
4. 翻訳ジョブを再試行してください

翻訳を再試行: {{ retry_url }}
設定を確認: {{ settings_url }}

問題が継続する場合は、エラーコード {{ error_code }} とともにサポートに連絡してください。