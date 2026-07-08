---
template_type: dev_account_approved
category: Developer Portal
---

# Email Template: dev_account_approved

## Subject
Benvenuto nel programma per sviluppatori Spwig, {{ developer_name }}!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Success Accent -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Benvenuto in Spwig!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          La tua candidatura come sviluppatore è stata approvata
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Ciao {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          Congratulazioni! La tua candidatura come sviluppatore è stata approvata. Ora hai accesso completo al Portale per sviluppatori Spwig.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Free License Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 0">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          La tua licenza gratuita per sviluppatori è in attesa
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Come sviluppatore approvato, ricevi un'installazione gratuita di Spwig Shop + POS con aggiornamenti perpetui. Richiedi la tua licenza, installa Spwig sul tuo server e inizia a creare componenti subito.
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="15px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ license_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Richiedi Licenza Gratuita
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Get Started Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          Inizia:
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> Richiedi la tua licenza gratuita per sviluppatori
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> Installa Spwig sul tuo server
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>3.</strong> Crea il tuo primo componente utilizzando i nostri SDK
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>4.</strong> Invialo dal tuo dashboard
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Vai al Dashboard
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Portale per sviluppatori Spwig</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Hai domande? Contatta il supporto per sviluppatori
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ciao {{ developer_name }},

Congratulazioni! La tua candidatura come sviluppatore è stata approvata. Ora hai accesso completo al Portale per sviluppatori Spwig.

LA TUA LICENZA GRATUITA PER SVILUPPATORI È IN ATTESA
Come sviluppatore approvato, ricevi un'installazione gratuita di Spwig Shop + POS con aggiornamenti perpetui. Richiedi la tua licenza, installa Spwig sul tuo server e inizia a creare componenti subito.

Richiedi la tua licenza gratuita: {{ license_url }}

Inizia:
1. Richiedi la tua licenza gratuita per sviluppatori: {{ license_url }}
2. Installa Spwig sul tuo server
3. Crea il tuo primo componente utilizzando i nostri SDK
4. Invialo dal tuo dashboard

Vai al Dashboard: {{ dashboard_url }}

---
Portale per sviluppatori Spwig