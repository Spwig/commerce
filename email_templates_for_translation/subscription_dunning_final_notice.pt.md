---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ AVISO FINAL: Sua assinatura será cancelada em {{ days_until_cancellation }} dias

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ AVISO FINAL
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cancelamento de Assinatura Iminente
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Este é seu aviso final. Nós não conseguimos processar o pagamento para sua assinatura {{ plan_name }}. Se não recebermos o pagamento dentro de {{ days_until_cancellation }} dias, sua assinatura será cancelada.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Pagamento Falhou - Ação Necessária
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Subscription:</strong> {{ plan_name }}<br/>
              <strong>Amount Due:</strong> {{ amount_due }}<br/>
              <strong>Failed Attempts:</strong> {{ retry_count }}<br/>
              <strong>Last Attempt:</strong> {{ last_retry_date }}<br/>
              <strong>Cancellation Date:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Erro de Pagamento:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          O Que Acontecerá:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          Se o pagamento não for recebido até {{ cancellation_date }}:<br/>
          • Sua assinatura será cancelada<br/>
          • Você perderá o acesso a todos os benefícios da assinatura<br/>
          • Seus dados podem ser excluídos (consulte a política de retenção)<br/>
          • Você precisará se inscrever novamente para recuperar o acesso
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Atualize Seu Método de Pagamento Agora
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Atualizar Método de Pagamento
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Problemas Comuns & Soluções:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>Cartão expirado:</strong> Atualize com um cartão de crédito atual<br/>
          • <strong>Saldo insuficiente:</strong> Garanta um saldo suficiente<br/>
          • <strong>Cartão recusado:</strong> Entre em contato com seu banco ou use outro cartão<br/>
          • <strong>Inconsistência de endereço:</strong> Verifique se o endereço de cobrança corresponde ao cartão
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              Precisa de Ajuda?
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              Se você estiver enfrentando problemas de pagamento ou precisar de ajuda, por favor, entre em contato imediatamente com nossa equipe de suporte.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contate o Suporte
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Se você desejar cancelar sua assinatura, poderá fazê-lo nas configurações da sua conta.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ AVISO FINAL

Cancelamento de Assinatura Iminente

Olá {{ customer_name }},

Este é seu aviso final. Nós não conseguimos processar o pagamento para sua assinatura {{ plan_name }}. Se não recebermos o pagamento dentro de {{ days_until_cancellation }} dias, sua assinatura será cancelada.

⚠️ PAGAMENTO FALHOU - AÇÃO NECESSÁRIA:
- Assinatura: {{ plan_name }}
- Valor Devido: {{ amount_due }}
- Tentativas Falhadas: {{ retry_count }}
- Última Tentativa: {{ last_retry_date }}
- Data de Cancelamento: {{ cancellation_date }}

ERRO DE PAGAMENTO:
{{ payment_error_message }}

O QUE ACONTECERÁ:
Se o pagamento não for recebido até {{ cancellation_date }}:
• Sua assinatura será cancelada
• Você perderá o acesso a todos os benefícios da assinatura
• Seus dados podem ser excluídos (consulte a política de retenção)
• Você precisará se inscrever novamente para recuperar o acesso

ATUALIZE SEU MÉTODO DE PAGAMENTO AGORA

Problemas Comuns & Soluções:
• Cartão expirado: Atualize com um cartão de crédito atual
• Saldo insuficiente: Garanta um saldo suficiente
• Cartão recusado: Entre em contato com seu banco ou use outro cartão
• Inconsistência de endereço: Verifique se o endereço de cobrança corresponde ao cartão

PRECISA DE AJUDA?
Se você estiver enfrentando problemas de pagamento ou precisar de ajuda, por favor, entre em contato imediatamente com nossa equipe de suporte.

Atualize o método de pagamento: {{ update_payment_url }}
Contate o suporte: {{ support_url }}

Se você desejar cancelar sua assinatura, poderá fazê-lo nas configurações da sua conta.