---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ バックアップ復元が完了しました - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ バックアップ復元が完了しました
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ admin_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          あなたのバックアップ復元操作が成功裏に完了しました。あなたのストアのデータが復元されました。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              復元の詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>バックアップファイル:</strong> {{ backup_filename }}<br/>
              <strong>バックアップ日:</strong> {{ backup_date }}<br/>
              <strong>開始時間:</strong> {{ restore_started_at }}<br/>
              <strong>完了時間:</strong> {{ restore_completed_at }}<br/>
              <strong>所要時間:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 重要な次のステップ:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. ストアが正常に動作しているか確認する<br/>
              2. 重要なデータ（商品、注文、顧客）を確認する<br/>
              3. 必要に応じてキャッシュをクリアする<br/>
              4. キャッシュ、管理者アクセスなどの重要なワークフローをテストする
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          管理者ダッシュボードへ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ BACKUP RESTORE COMPLETED

こんにちは {{ admin_name }},

あなたのバックアップ復元操作が成功裏に完了しました。あなたのストアのデータが復元されました。

RESTORE DETAILS:
- Backup File: {{ backup_filename }}
- Backup Date: {{ backup_date }}
- Started: {{ restore_started_at }}
- Completed: {{ restore_completed_at }}
- Duration: {{ restore_duration }}

⚠️ IMPORTANT NEXT STEPS:
1. Verify your store is functioning correctly
2. Check key data (products, orders, customers)
3. Clear cache if needed
4. Test critical workflows (checkout, admin access)

Go to admin dashboard: {{ admin_dashboard_url }}