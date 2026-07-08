---
template_type: translation_job_completed
category: Translation Service
---

# Email Template: translation_job_completed

## Subject
✓ Translation completed: {{ content_type }} ({{ language_count }} languages)

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Translation Complete!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Your Translations Are Ready
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Great news! Your bulk translation job has been completed successfully.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Job Summary:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Languages:</strong> {{ target_languages }}<br/>
              <strong>Items Translated:</strong> {{ items_translated }}<br/>
              <strong>Total Words:</strong> {{ word_count }}<br/>
              <strong>Completed:</strong> {{ completed_at }}<br/>
              <strong>Duration:</strong> {{ job_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Translation Quality:
        </mj-text>

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#065f46">
              <strong>Average Quality Score:</strong> {{ quality_score }}%<br/>
              <strong>High Quality:</strong> {{ high_quality_count }} items<br/>
              <strong>Review Recommended:</strong> {{ review_needed_count }} items
            </mj-text>
          </mj-column>
        </mj-section>

        {% if review_needed_count > 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Review Recommended
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ review_needed_count }} translations scored below 85% and should be reviewed before publishing.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Next Steps:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Review the translations in your admin panel<br/>
          2. Edit any translations that need refinement<br/>
          3. Publish translations to make them live<br/>
          4. Your multilingual content will be available to customers
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ review_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Review Translations
        </mj-button>

        {% if can_publish_all %}
        <mj-spacer height="10px" />
        <mj-button href="{{ publish_all_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Publish All
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ TRANSLATION COMPLETE!

Your Translations Are Ready

Great news! Your bulk translation job has been completed successfully.

JOB SUMMARY:
- Job ID: {{ job_id }}
- Content Type: {{ content_type }}
- Languages: {{ target_languages }}
- Items Translated: {{ items_translated }}
- Total Words: {{ word_count }}
- Completed: {{ completed_at }}
- Duration: {{ job_duration }}

TRANSLATION QUALITY:
- Average Quality Score: {{ quality_score }}%
- High Quality: {{ high_quality_count }} items
- Review Recommended: {{ review_needed_count }} items

{% if review_needed_count > 0 %}
⚠️ REVIEW RECOMMENDED:
{{ review_needed_count }} translations scored below 85% and should be reviewed before publishing.
{% endif %}

NEXT STEPS:
1. Review the translations in your admin panel
2. Edit any translations that need refinement
3. Publish translations to make them live
4. Your multilingual content will be available to customers

Review translations: {{ review_url }}
{% if can_publish_all %}Publish all: {{ publish_all_url }}{% endif %}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| job_id | Unique job identifier | TJ-2026-001234 |
| content_type | What was translated | Product Descriptions |
| target_languages | Languages translated to | French, German, Spanish |
| language_count | Number of languages | 3 |
| items_translated | Number of items | 247 |
| word_count | Total words translated | 15,432 |
| completed_at | Completion time | February 15, 2026 at 5:30 PM |
| job_duration | Total time taken | 1 hour 45 minutes |
| quality_score | Average quality percentage | 92 |
| high_quality_count | High quality items | 235 |
| review_needed_count | Items needing review | 12 |
| review_url | Translation review page | https://shop.com/en/admin/translations/review/12345 |
| can_publish_all | Boolean flag | true |
| publish_all_url | Bulk publish URL | https://shop.com/en/admin/translations/publish/12345 |

## Notes

- Admin notification - job completion
- Sent when bulk translation completes successfully
- Includes quality metrics and recommendations
- Flags low-quality translations for review
- Provides review and publish workflows
- Positive, actionable tone
- Transactional email
