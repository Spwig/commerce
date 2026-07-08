---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 重大: バックアップ復元に失敗しました - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 重大: バックアップ復元に失敗しました
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          こんにちは {{ admin_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          重大なバックアップ復元操作に失敗しました。ストアが一貫性のない状態になっている可能性があり、直ちに対処が必要です。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              復元の詳細:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>バックアップファイル:</strong> {{ backup_filename }}<br/>
              <strong>開始時間:</strong> {{ restore_started_at }}<br/>
              <strong>失敗時間:</strong> {{ restore_failed_at }}<br/>
              <strong>所要時間:</strong> {{ restore_duration }}
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 即時対応が必要です:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>変更を加えないでください</strong>ストアに<br/>
              2. データベースの接続性と整合性を確認してください<br/>
              3. 詳細なスタックトレースのためにエラーログを確認してください<br/>
              4. すぐに技術サポートに連絡してください<br/>
              5. 最後に知られている正常な状態にロールバックすることを検討してください
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          復元ログを表示
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          緊急サポートに連絡
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 重大: バックアップ復元に失敗しました

こんにちは {{ admin_name }}、

重大なバックアップ復元操作に失敗しました。ストアが一貫性のない状態になっている可能性があり、直ちに対処が必要です。

復元の詳細:
- バックアップファイル: {{ backup_filename }}
- 開始時間: {{ restore_started_at }}
- 失敗時間: {{ restore_failed_at }}
- 所要時間: {{ restore_duration }}

エラーの詳細:
{{ error_message }}

🚨 即時対応が必要です:
1. 変更を加えないでください ストアに
2. データベースの接続性と整合性を確認してください
3. 詳細なスタックトレースのためにエラーログを確認してください
4. すぐに技術サポートに連絡してください
5. 最後に知られている正常な状態にロールバックすることを検討してください

復元ログを表示: {{ admin_backup_url }}
緊急サポートに連絡: {{ support_url }}