---
template_type: pos_terminal_offline
category: POS
---

# Email Template: pos_terminal_offline

## Subject
⚠️ POS Terminal Offline: {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ Terminal Disconnected
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          POS Terminal Offline
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ terminal_name }} has gone offline and is no longer responding.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Terminal Info:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Terminal:</strong> {{ terminal_name }}<br/>
              <strong>Location:</strong> {{ location }}<br/>
              <strong>Last Seen:</strong> {{ last_seen }}<br/>
              <strong>Offline Since:</strong> {{ offline_since }}<br/>
              <strong>Duration:</strong> {{ offline_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Common Causes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Network connectivity issues<br/>
          • Terminal powered off or restarted<br/>
          • Software crash or freeze<br/>
          • Internet service outage
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Recommended Actions:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Check terminal power and network connection<br/>
          2. Restart the terminal device<br/>
          3. Verify internet connectivity<br/>
          4. Check firewall and security settings
        </mj-text>

        {% if active_shift %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Active Shift Warning
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              This terminal has an active shift. Sales data may not be synchronized until reconnected.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_terminals_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Terminal Status
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          You will receive another notification when the terminal reconnects.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ TERMINAL DISCONNECTED

POS Terminal Offline

{{ terminal_name }} has gone offline and is no longer responding.

TERMINAL INFO:
- Terminal: {{ terminal_name }}
- Location: {{ location }}
- Last Seen: {{ last_seen }}
- Offline Since: {{ offline_since }}
- Duration: {{ offline_duration }}

COMMON CAUSES:
• Network connectivity issues
• Terminal powered off or restarted
• Software crash or freeze
• Internet service outage

RECOMMENDED ACTIONS:
1. Check terminal power and network connection
2. Restart the terminal device
3. Verify internet connectivity
4. Check firewall and security settings

{% if active_shift %}
⚠️ ACTIVE SHIFT WARNING:
This terminal has an active shift. Sales data may not be synchronized until reconnected.
{% endif %}

View terminal status: {{ admin_terminals_url }}

You will receive another notification when the terminal reconnects.