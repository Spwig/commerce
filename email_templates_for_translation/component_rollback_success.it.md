---
template_type: component_rollback_success
category: Component Updates
---

# Email Template: component_rollback_success

## Subject
✓ {{ component_name }} rolled back to v{{ previous_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dbeafe">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          ↩️ Rollback Complete
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Component Restored
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} has been successfully rolled back to the previous version.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Rollback Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Component:</strong> {{ component_name }}<br/>
              <strong>Rolled Back From:</strong> v{{ failed_version }}<br/>
              <strong>Restored To:</strong> v{{ previous_version }}<br/>
              <strong>Completed:</strong> {{ completed_at }}<br/>
              <strong>Duration:</strong> {{ rollback_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rollback_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Reason for Rollback:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ rollback_reason }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ✓ Store Status
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              Your store is now running on the stable version {{ previous_version }}. All functionality should be restored.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if data_restored %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Data Restoration:</strong> {{ data_restoration_message }}
        </mj-text>
        {% endif %}

        {% if next_steps %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Next Steps:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ component_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Component Details
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Incident Report
        </mj-button>
        {% endif %}

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          If you continue to experience issues, please contact support.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
↩️ ROLLBACK COMPLETE

Component Restored

{{ component_name }} has been successfully rolled back to the previous version.

ROLLBACK DETAILS:
- Component: {{ component_name }}
- Rolled Back From: v{{ failed_version }}
- Restored To: v{{ previous_version }}
- Completed: {{ completed_at }}
- Duration: {{ rollback_duration }}

{% if rollback_reason %}
REASON FOR ROLLBACK:
{{ rollback_reason }}
{% endif %}

✓ STORE STATUS:
Your store is now running on the stable version {{ previous_version }}. All functionality should be restored.

{% if data_restored %}
DATA RESTORATION: {{ data_restoration_message }}
{% endif %}

{% if next_steps %}
NEXT STEPS:
{{ next_steps }}
{% endif %}

View component details: {{ component_url }}
{% if incident_report_url %}View incident report: {{ incident_report_url }}{% endif %}

If you continue to experience issues, please contact support.