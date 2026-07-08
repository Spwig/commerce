---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 緊急：備份失敗 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ 備份失敗
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您的 {{ shop_name }} 商店的一個關鍵備份操作已失敗。為確保數據保護，需要立即採取行動。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              備份詳情：
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>備份類型：</strong> {{ backup_type }}<br/>
              <strong>開始時間：</strong> {{ backup_started_at }}<br/>
              <strong>失敗時間：</strong> {{ backup_failed_at }}<br/>
              <strong>持續時間：</strong> {{ backup_duration }}
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

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建議操作：
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. 檢查您的伺服器可用磁碟空間<br/>
          2. 驗證資料庫連接性<br/>
          3. 檢查錯誤日誌以獲取詳細的堆疊追蹤<br/>
          4. 手動重試備份或等待下一次預約執行<br/>
          5. 如果問題持續存在，請聯繫支援
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看備份日誌
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          立即重試備份
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>上次成功備份：</strong> {{ last_successful_backup }}<br/>
          <strong>下次預定備份：</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 緊急：備份失敗

Hi {{ admin_name }},

您的 {{ shop_name }} 商店的一個關鍵備份操作已失敗。為確保數據保護，需要立即採取行動。

備份詳情：
- 備份類型：{{ backup_type }}
- 開始時間：{{ backup_started_at }}
- 失敗時間：{{ backup_failed_at }}
- 持續時間：{{ backup_duration }}

錯誤詳情：
{{ error_message }}

建議操作：
1. 檢查您的伺服器可用磁碟空間
2. 驗證資料庫連接性
3. 檢查錯誤日誌以獲取詳細的堆疊追蹤
4. 手動重試備份或等待下一次預約執行
5. 如果問題持續存在，請聯繫支援

查看備份日誌：{{ admin_backup_url }}
立即重試備份：{{ retry_backup_url }}

上次成功備份：{{ last_successful_backup }}
下次預定備份：{{ next_scheduled_backup }}

---
這是針對 {{ shop_name }} 管理員的重要系統警報。