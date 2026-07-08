---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 緊急: バックアップ失敗 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ バックアップ失敗
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          こんにちは {{ admin_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          あなたの {{ shop_name }} ショップの重要なバックアップ操作が失敗しました。データの保護を確保するために、直ちに行動が必要です。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              バックアップの詳細:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>バックアップの種類:</strong> {{ backup_type }}<br/>
              <strong>開始時間:</strong> {{ backup_started_at }}<br/>
              <strong>失敗時間:</strong> {{ backup_failed_at }}<br/>
              <strong>所要時間:</strong> {{ backup_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          エラーの詳細:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          おすすめの対応策:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. サーバーの利用可能なディスク容量を確認する<br/>
          2. データベース接続を確認する<br/>
          3. 詳細なスタックトレースのためにエラーログを確認する<br/>
          4. 手動でバックアップを再試行するか、次の予定された実行を待つ<br/>
          5. 問題が継続する場合は、サポートに連絡する
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          バックアップログの確認
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          今すぐバックアップを再試行
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>最後に成功したバックアップ:</strong> {{ last_successful_backup }}<br/>
          <strong>次の予定バックアップ:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 緊急: BACKUP 失敗

こんにちは {{ admin_name }}、

あなたの {{ shop_name }} ショップの重要なバックアップ操作が失敗しました。データの保護を確保するために、直ちに行動が必要です。

BACKUP 詳細:
- バックアップの種類: {{ backup_type }}
- 開始時間: {{ backup_started_at }}
- 失敗時間: {{ backup_failed_at }}
- 所要時間: {{ backup_duration }}

ERROR 詳細:
{{ error_message }}

RECOMMENDED ACTIONS:
1. サーバーの利用可能なディスク容量を確認する
2. データベース接続を確認する
3. 詳細なスタックトレースのためにエラーログを確認する
4. 手動でバックアップを再試行するか、次の予定された実行を待つ
5. 問題が継続する場合は、サポートに連絡する

バックアップログの確認: {{ admin_backup_url }}
今すぐバックアップを再試行: {{ retry_backup_url }}

最後に成功したバックアップ: {{ last_successful_backup }}
次の予定バックアップ: {{ next_scheduled_backup }}

---
これは {{ shop_name }} の管理者向けの重要なシステムアラートです。