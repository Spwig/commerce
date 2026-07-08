---
template_type: loyalty_tier_demotion_warning
category: Loyalty Program
---

# Email Template: loyalty_tier_demotion_warning

## Subject
⚠️ Seu status de {{ current_tier }} está prestes a expirar - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Status de Nível Expirando
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Não Perca os Benefícios do Seu {{ current_tier }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Seu status de nível {{ current_tier }} expirará em {{ expiry_date }} a menos que você mantenha seu nível de atividade.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Status Atual:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Status Atual:</strong> {{ current_tier }}<br/>
              <strong>Vence:</strong> {{ expiry_date }} ({{ days_remaining }} dias)<br/>
              <strong>Próximo Nível:</strong> {{ next_tier }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Como Manter o Seu Status de {{ current_tier }}:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          Você precisa {{ requirement_type }} antes de {{ expiry_date }}:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
              {{ requirement_description }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
              Atual: {{ current_progress }} | Necessário: {{ required_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Benefícios que Você Perderá:
        </mj-text>

        <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {% for benefit in tier_benefits %}
          • {{ benefit }}<br/>
          {% endfor %}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Compre Agora & Mantenha Seu Status
        </mj-button>

        <mj-spacer height="20px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver Detalhes Completos
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ STATUS DE NÍVEL EXPIRADO

Não Perca os Benefícios do Seu {{ current_tier }}!

Olá {{ customer_name }},

Seu status de nível {{ current_tier }} expirará em {{ expiry_date }} a menos que você mantenha seu nível de atividade.

STATUS ATUAL:
- Status Atual: {{ current_tier }}
- Vence: {{ expiry_date }} ({{ days_remaining }} dias)
- Próximo Nível: {{ next_tier }}

COMO MANTER SEU STATUS DE {{ current_tier }}:
Você precisa {{ requirement_type }} antes de {{ expiry_date }}:

{{ requirement_description }}
Atual: {{ current_progress }} | Necessário: {{ required_amount }}

BENEFÍCIOS QUE VOCÊ PERDERÁ:
{% for benefit in tier_benefits %}
• {{ benefit }}
{% endfor %}

Compre agora & mantenha seu status: {{ shop_url }}
Ver detalhes completos: {{ loyalty_dashboard_url }}