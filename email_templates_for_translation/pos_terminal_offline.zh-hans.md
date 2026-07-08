---
template_type: pos_terminal_offline
category: POS
---

# Email Template: pos_terminal_offline

## Subject
⚠️ POS终端离线：{{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ 终端已断开连接
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          POS终端离线
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} 已离线，不再响应。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              终端信息：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>终端：</strong> {{ terminal_name }}<br/>
              <strong>位置：</strong> {{ location }}<br/>
              <strong>最后在线时间：</strong> {{ last_seen }}<br/>
              <strong>离线时间：</strong> {{ offline_since }}<br/>
              <strong>持续时间：</strong> {{ offline_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          常见原因：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 网络连接问题<br/>
          • 终端已关闭或重启<br/>
          • 软件崩溃或冻结<br/>
          • 网络服务中断
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建议操作：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. 检查终端电源和网络连接<br/>
          2. 重启终端设备<br/>
          3. 验证网络连接<br/>
          4. 检查防火墙和安全设置
        </mj-text>

        {% if active_shift %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ 活动班次警告
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              此终端有活动班次。重新连接之前销售数据可能无法同步。
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_terminals_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看终端状态
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          终端重新连接后，您将收到另一条通知。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 终端已断开连接

POS终端离线

{{ terminal_name }} 已离线，不再响应。

终端信息：
- 终端：{{ terminal_name }}
- 位置：{{ location }}
- 最后在线时间：{{ last_seen }}
- 离线时间：{{ offline_since }}
- 持续时间：{{ offline_duration }}

常见原因：
• 网络连接问题
• 终端已关闭或重启
• 软件崩溃或冻结
• 网络服务中断

建议操作：
1. 检查终端电源和网络连接
2. 重启终端设备
3. 验证网络连接
4. 检查防火墙和安全设置

{% if active_shift %}
⚠️ 活动班次警告：
此终端有活动班次。重新连接之前销售数据可能无法同步。
{% endif %}

查看终端状态：{{ admin_terminals_url }}

终端重新连接后，您将收到另一条通知。