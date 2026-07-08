---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ 備份還原完成 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ 備份還原完成
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您的備份還原操作已成功完成。您的商店數據已恢復。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              備份還原詳情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>備份文件：</strong> {{ backup_filename }}<br/>
              <strong>備份日期：</strong> {{ backup_date }}<br/>
              <strong>開始時間：</strong> {{ restore_started_at }}<br/>
              <strong>完成時間：</strong> {{ restore_completed_at }}<br/>
              <strong>持續時間：</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 重要後續步驟：
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. 確認您的商店運作正常<br/>
              2. 檢查關鍵數據（商品、訂單、客戶）<br/>
              3. 如有必要，清除緩存<br/>
              4. 測試關鍵流程（結帳、管理員訪問）
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          前往管理員儀表板
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 備份還原完成

Hi {{ admin_name }},

您的備份還原操作已成功完成。您的商店數據已恢復。

備份還原詳情：
- 備份文件：{{ backup_filename }}
- 備份日期：{{ backup_date }}
- 開始時間：{{ restore_started_at }}
- 完成時間：{{ restore_completed_at }}
- 繼續時間：{{ restore_duration }}

⚠️ 重要後續步驟：
1. 確認您的商店運作正常
2. 檢查關鍵數據（商品、訂單、客戶）
3. 如有必要，清除緩存
4. 測試關鍵流程（結帳、管理員訪問）

前往管理員儀表板：{{ admin_dashboard_url }}