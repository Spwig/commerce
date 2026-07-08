---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 重大：備份還原失敗 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 重大：備份還原失敗
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          一次關鍵的備份還原操作已失敗。您的商店可能處於不一致的狀態，需要立即處理。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              備份還原詳情：
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>備份檔案：</strong> {{ backup_filename }}<br/>
              <strong>開始時間：</strong> {{ restore_started_at }}<br/>
              <strong>失敗時間：</strong> {{ restore_failed_at }}<br/>
              <strong>持續時間：</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          錯誤詳情：
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
              🚨 立即採取行動：
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>切勿</strong> 對商店進行任何更改<br/>
              2. 檢查資料庫連線性和完整性<br/>
              3. 檢視錯誤日誌以取得詳細的堆疊追蹤<br/>
              4. 立即聯絡技術支援<br/>
              5. 考慮回滾到最後已知的良好狀態
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看還原日誌
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          聯絡緊急技術支援
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 重大：備份還原失敗

Hi {{ admin_name }},

一次關鍵的備份還原操作已失敗。您的商店可能處於不一致的狀態，需要立即處理。

備份還原詳情：
- 備份檔案：{{ backup_filename }}
- 開始時間：{{ restore_started_at }}
- 失敗時間：{{ restore_failed_at }}
- 持續時間：{{ restore_duration }}

錯誤詳情：
{{ error_message }}

🚨 立即採取行動：
1. 切勿對商店進行任何更改
2. 檢查資料庫連線性和完整性
3. 檢視錯誤日誌以取得詳細的堆疊追蹤
4. 立即聯絡技術支援
5. 考慮回滾到最後已知的良好狀態

查看還原日誌：{{ admin_backup_url }}
聯絡緊急技術支援：{{ support_url }}

