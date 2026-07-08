---
template_type: return_received
category: Returns
---

# Email Template: return_received

## Subject
Recebemos seu devolução - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Devolução Recebida
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.primary|default:'#1d4ed8' }}">
          Pedido #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nós recebemos seus itens devolvidos para o pedido <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>O que acontece em seguida:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Nossa equipe inspecionará os itens devolvidos em 2-3 dias úteis<br/>
          2. Verificaremos se os itens estão em sua condição original<br/>
          3. Após a inspeção, processaremos seu reembolso<br/>
          4. Você receberá um e-mail de confirmação assim que o reembolso for processado
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          O reembolso será creditado no método de pagamento original e pode levar de 5 a 10 dias úteis para aparecer em sua conta.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Obrigado pela sua paciência!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Devolução Recebida - Pedido #{{ order_number }}

Olá {{ customer_name }},

Nós recebemos seus itens devolvidos para o pedido #{{ order_number }}.

O que acontece em seguida:
1. Nossa equipe inspecionará os itens devolvidos em 2-3 dias úteis
2. Verificaremos se os itens estão em sua condição original
3. Após a inspeção, processaremos seu reembolso
4. Você receberá um e-mail de confirmação assim que o reembolso for processado

O reembolso será creditado no método de pagamento original e pode levar de 5 a 10 dias úteis para aparecer em sua conta.

Obrigado pela sua paciência!