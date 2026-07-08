---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 URGENTE: Aggiornamento di sicurezza disponibile per {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 AGGIORNAMENTO DI SICUREZZA RICHIESTO
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Patch di Sicurezza Critica
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          È stata scoperta una vulnerabilità di sicurezza in {{ component_name }}. Aggiorna immediatamente per proteggere il tuo negozio.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Informazioni sulla Sicurezza
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Componente:</strong> {{ component_name }}<br/>
              <strong>Versione Corrente:</strong> {{ current_version }}<br/>
              <strong>Versione Corretta:</strong> {{ patched_version }}<br/>
              <strong>Gravità:</strong> {{ severity_level }}<br/>
              <strong>ID CVE:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Dettagli della Vulnerabilità:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Impatto Potenziale:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Mitigazione Temporanea
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Azione Richiesta: Installa l'Aggiornamento Subito
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Installa Patch di Sicurezza
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Leggi l'Avviso di Sicurezza
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Se hai bisogno di assistenza, contatta immediatamente il supporto Spwig.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 AGGIORNAMENTO DI SICUREZZA RICHIESTO

Patch di Sicurezza Critica

È stata scoperta una vulnerabilità di sicurezza in {{ component_name }}. Aggiorna immediatamente per proteggere il tuo negozio.

⚠️ INFORMAZIONI SULLA SICUREZZA:
- Componente: {{ component_name }}
- Versione Corrente: {{ current_version }}
- Versione Corretta: {{ patched_version }}
- Gravità: {{ severity_level }}
- ID CVE: {{ cve_id }}

DETTAGLI DELLA VULNERABILITÀ:
{{ vulnerability_description }}

IMPATTO POTENZIALE:
{{ impact_description }}

{% if mitigation_steps %}
MITIGAZIONE TEMPORANEA:
{{ mitigation_steps }}
{% endif %}

AZIONE RICHIESTA: INSTALLA L'AGGIORNAMENTO IMMEDIATAMENTE

Installa patch di sicurezza: {{ update_url }}
Leggi l'avviso di sicurezza: {{ advisory_url }}

Se hai bisogno di assistenza, contatta immediatamente il supporto Spwig.