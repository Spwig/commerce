---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
भुगतान प्रदाता समस्या - {{ provider_name }} SDK लोड नहीं हुआ

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          भुगतान प्रदाता समस्या
        </mj-text>
        <mj-text>
          चेकआउट के दौरान एक ग्राहक के लिए {{ provider_name }} भुगतान SDK लोड नहीं हुआ। यह प्रदाता के सेवा बाधित होने का संकेत हो सकता है।
        </mj-text>
        <mj-text>
          <strong>प्रदाता:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>त्रुटि प्रकार:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>समय:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>असफलता की संख्या (अंतिम एक घंटा):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          इस सूचना को प्रति प्रदाता प्रति घंटा एक के रूप में दर-सीमित किया गया है। यदि समस्या बनी रहती है, तो प्रदाता डैशबोर्ड की जांच करें या उनके समर्थन से संपर्क करें।
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          भुगतान सेटिंग्स देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
भुगतान प्रदाता समस्या

चेकआउट के दौरान एक ग्राहक के लिए {{ provider_name }} भुगतान SDK लोड नहीं हुआ। यह प्रदाता के सेवा बाधित होने का संकेत हो सकता है।

प्रदाता: {{ provider_name }}
त्रुटि प्रकार: {{ error_type }}
समय: {{ timestamp }}
असफलता की संख्या (अंतिम एक घंटा): {{ failure_count }}

इस सूचना को प्रति प्रदाता प्रति घंटा एक के रूप में दर-सीमित किया गया है। यदि समस्या बनी रहती है, तो प्रदाता डैशबोर्ड की जांच करें या उनके समर्थन से संपर्क करें।

भुगतान सेटिंग्स देखें: {{ admin_url }}