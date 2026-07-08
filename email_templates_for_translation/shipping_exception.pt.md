---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
Exceção de Envio - Pedido #{{ order_number }} Requer Atenção

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Exceção de Envio
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Estamos escrevendo para informar sobre uma exceção no seu envio. Estamos trabalhando para resolver esse problema o mais rapidamente possível.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Detalhes da Exceção:
            </mj-text>
            <mj-text color="#92400e">
              <strong>Tipo de Exceção:</strong> {{ exception_type }}<br/>
              <strong>Descrição:</strong> {{ exception_description }}<br/>
              <strong>Ocorreu:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Informação do Pedido:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Número do Pedido:</strong> {{ order_number }}<br/>
              <strong>Número de Rastreamento:</strong> {{ tracking_number }}<br/>
              <strong>Transportadora:</strong> {{ carrier_name }}<br/>
              <strong>Localização Atual:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          O Que Acontece Em Seguida?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Ação Necessária:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rastrear Seu Pedido
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contate o Suporte
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ EXCEÇÃO DE ENVIO

Olá {{ customer_name }},

Estamos escrevendo para informar sobre uma exceção no seu envio. Estamos trabalhando para resolver esse problema o mais rapidamente possível.

DETALHES DA EXCEÇÃO:
- Tipo de Exceção: {{ exception_type }}
- Descrição: {{ exception_description }}
- Ocorreu: {{ exception_date }}

INFORMAÇÃO DO PEDIDO:
- Número do Pedido: {{ order_number }}
- Número de Rastreamento: {{ tracking_number }}
- Transportadora: {{ carrier_name }}
- Localização Atual: {{ current_location }}

O QUE ACONTECE EM SEGUIDA?
{{ resolution_steps }}

{% if action_required %}
⚠️ AÇÃO NECESSÁRIA:
{{ action_required_description }}
{% endif %}

Rastrear seu pedido: {{ tracking_url }}
Contate o suporte: {{ support_url }}