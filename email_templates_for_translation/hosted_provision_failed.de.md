---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
Aktion erforderlich - Problem bei der Store-Setup für {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Store Setup Issue
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Wir haben ein Problem beim Einrichten Ihres Stores <strong>{{ store_name }}</strong> festgestellt. Unser Team wurde benachrichtigt und untersucht das Problem.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          Was passiert ist
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Was als Nächstes passiert?
        </mj-text>
        <mj-text font-size="14px">
          Unser Support-Team wurde automatisch über dieses Problem benachrichtigt. Sie müssen keine Aktion unternehmen – wir kontaktieren Sie, sobald das Problem behoben ist.
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          Wenn Sie in der Zwischenzeit Fragen haben, zögern Sie nicht, uns zu kontaktieren.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Store Setup Issue - {{ store_name }}

Hi {{ name|default:'there' }},

Wir haben ein Problem beim Einrichten Ihres Stores {{ store_name }} festgestellt. Unser Team wurde benachrichtigt und untersucht das Problem.

Was passiert ist:
{{ provision_error }}

Was als Nächstes passiert?
Unser Support-Team wurde automatisch über dieses Problem benachrichtigt. Sie müssen keine Aktion unternehmen – wir kontaktieren Sie, sobald das Problem behoben ist.

Wenn Sie in der Zwischenzeit Fragen haben, zögern Sie nicht, uns zu kontaktieren.

Need help? Contact {{ support_email }}