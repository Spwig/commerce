---
template_type: backup_size_warning
category: Backups
---

# Email Template: backup_size_warning

## Subject
⚠️ बैकअप आकार चेतावनी - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ बैकअप आकार चेतावनी
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ shop_name }} के आपके हालिया बैकअप अनुमोदित आकार थ्रेशहोल्ड को पार कर गया है। यह डेटा संग्रहण आवश्यकताओं के बढ़ते हुए होने का संकेत कर सकता है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              बैकअप जानकारी:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>वर्तमान आकार:</strong> {{ backup_size }}<br/>
              <strong>चेतावनी सीमा:</strong> {{ size_threshold }}<br/>
              <strong>पिछले सप्ताह के बाद की वृद्धि:</strong> {{ size_increase }}<br/>
              <strong>बैकअप तारीख:</strong> {{ backup_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सुझाए गए कार्य:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. बैकअप रखे रहने की नीति की जांच करें<br/>
          2. पुराने बैकअप के आर्काइव करने की विचार करें<br/>
          3. मीडिया पुस्तकालय में अनावश्यक बड़े फ़ाइलों की जांच करें<br/>
          4. संग्रहण क्षमता आवश्यकताओं की आकलन करें<br/>
          5. बैकअप वृद्धि रुझान की निगरानी करें
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          बैकअप प्रबंधन
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ बैकअप आकार चेतावनी

हेलो {{ admin_name }},

{{ shop_name }} के आपके हालिया बैकअप अनुमोदित आकार थ्रेशहोल्ड को पार कर गया है। यह डेटा संग्रहण आवश्यकताओं के बढ़ते हुए होने का संकेत कर सकता है।

बैकअप जानकारी:
- वर्तमान आकार: {{ backup_size }}
- चेतावनी सीमा: {{ size_threshold }}
- पिछले सप्ताह के बाद की वृद्धि: {{ size_increase }}
- बैकअप तारीख: {{ backup_date }}

सुझाए गए कार्य:
1. बैकअप रखे रहने की नीति की जांच करें
2. पुराने बैकअप के आर्काइव करने की विचार करें
3. मीडिया पुस्तकालय में अनावश्यक बड़े फ़ाइलों की जांच करें
4. संग्रहण क्षमता आवश्यकताओं की आकलन करें
5. बैकअप वृद्धि रुझान की निगरानी करें

बैकअप प्रबंधन: {{ admin_backup_url }}