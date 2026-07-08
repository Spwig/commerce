---
template_type: translation_job_started
category: Translation Service
---

# Email Template: translation_job_started

## Subject
🌐 Translation job started: {{ content_type }} ({{ source_language }} → {{ target_languages }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          🌐 Translation Job Started
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bulk Translation In Progress
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Your bulk translation job has been started and is now processing.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Job Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Source Language:</strong> {{ source_language }}<br/>
              <strong>Target Languages:</strong> {{ target_languages }}<br/>
              <strong>Items to Translate:</strong> {{ item_count }}<br/>
              <strong>Started:</strong> {{ started_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Estimated Completion:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46" font-weight="bold" align="center">
              {{ estimated_completion }}
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              (Based on {{ word_count }} words)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What Happens Next:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. AI translation service processes your content<br/>
          2. Translations are saved as drafts for review<br/>
          3. You'll receive an email when the job is complete<br/>
          4. Review and publish translations from your admin panel
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ job_status_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Job Status
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          You can close this email. We'll notify you when the translation is complete.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🌐 TRANSLATION JOB STARTED

Bulk Translation In Progress

Your bulk translation job has been started and is now processing.

JOB DETAILS:
- Job ID: {{ job_id }}
- Content Type: {{ content_type }}
- Source Language: {{ source_language }}
- Target Languages: {{ target_languages }}
- Items to Translate: {{ item_count }}
- Started: {{ started_at }}

ESTIMATED COMPLETION:
{{ estimated_completion }}
(Based on {{ word_count }} words)

WHAT HAPPENS NEXT:
1. AI translation service processes your content
2. Translations are saved as drafts for review
3. You'll receive an email when the job is complete
4. Review and publish translations from your admin panel

View job status: {{ job_status_url }}

You can close this email. We'll notify you when the translation is complete.

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| job_id | Unique job identifier | TJ-2026-001234 |
| content_type | What's being translated | Product Descriptions |
| source_language | Source language | English |
| target_languages | Target languages list | French, German, Spanish |
| item_count | Number of items | 247 |
| word_count | Total words to translate | 15,432 |
| started_at | Job start time | February 15, 2026 at 3:45 PM |
| estimated_completion | Estimated finish time | Approximately 2 hours |
| job_status_url | Job monitoring page | https://shop.com/en/admin/translations/jobs/12345 |

## Notes

- Admin notification - job confirmation
- Sent when bulk translation job starts
- Provides job tracking information
- Sets expectations for completion time
- Links to live status page
- Transactional email
