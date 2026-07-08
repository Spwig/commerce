---
template_type: backup_scheduled_missed
category: Backups
---

# Email Template: backup_scheduled_missed

## Subject
⚠️ 予定されたバックアップが実行されませんでした - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 予定されたバックアップが実行されませんでした
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ admin_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ shop_name }} の予定されたバックアップが想定通りに実行されませんでした。あなたのデータが完全に保護されているとは限りません。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              バックアップスケジュールの詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>予定時間:</strong> {{ scheduled_time }}<br/>
              <strong>バックアップタイプ:</strong> {{ backup_type }}<br/>
              <strong>最後に成功したバックアップ:</strong> {{ last_successful_backup }}<br/>
              <strong>最後のバックアップからの経過時間:</strong> {{ time_since_last }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          可能な原因:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          • サーバーがオフラインまたはアクセス不能でした<br/>
          • 予定されたタスクサービスが実行されていません<br/>
          • 権限が不足しています<br/>
          • ストレージスペースがいっぱいです<br/>
          • データベース接続の問題
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          手動でバックアップを実行する
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          システムログを表示
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 予定されたバックアップが実行されませんでした

こんにちは {{ admin_name }}、

{{ shop_name }} の予定されたバックアップが想定通りに実行されませんでした。あなたのデータが完全に保護されているとは限りません。

バックアップスケジュールの詳細:
- 予定時間: {{ scheduled_time }}
- バックアップタイプ: {{ backup_type }}
- 最後に成功したバックアップ: {{ last_successful_backup }}
- 最後のバックアップからの経過時間: {{ time_since_last }}

可能な原因:
• サーバーがオフラインまたはアクセス不能でした
• 予定されたタスクサービスが実行されていません
• 権限が不足しています
• ストレージスペースがいっぱいです
• データベース接続の問題

手動でバックアップを実行する: {{ admin_backup_url }}
システムログを表示: {{ admin_logs_url }}
