---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ 备份还原完成 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ 备份还原完成
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ admin_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你的备份还原操作已成功完成。你的商店数据已恢复。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              还原详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>备份文件：</strong> {{ backup_filename }}<br/>
              <strong>备份日期：</strong> {{ backup_date }}<br/>
              <strong>开始时间：</strong> {{ restore_started_at }}<br/>
              <strong>完成时间：</strong> {{ restore_completed_at }}<br/>
              <strong>持续时间：</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 重要下一步：
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. 确认您的商店运行正常<br/>
              2. 检查关键数据（产品、订单、客户）<br/>
              3. 如有必要，请清除缓存<br/>
              4. 测试关键工作流程（结账、管理员访问）
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          前往管理员仪表板
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 备份还原完成

你好 {{ admin_name }}，

你的备份还原操作已成功完成。你的商店数据已恢复。

还原详情：
- 备份文件：{{ backup_filename }}
- 备份日期：{{ backup_date }}
- 开始时间：{{ restore_started_at }}
- 完成时间：{{ restore_completed_at }}
- 持续时间：{{ restore_duration }}

⚠️ 重要下一步：
1. 确认您的商店运行正常
2. 检查关键数据（产品、订单、客户）
3. 如有必要，请清除缓存
4. 测试关键工作流程（结账、管理员访问）

前往管理员仪表板：{{ admin_dashboard_url }}