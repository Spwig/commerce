---
title: Domínio de envio de marketing
---

# Domínio de envio de marketing

Sua loja envia dois tipos muito diferentes de e-mail:

- **Transacional** — confirmações de pedido, atualizações de envio, redefinições de senha. Esses e-mails devem sempre chegar à caixa de entrada.
- **Marketing** — newsletters, promoções, recuperação de carrinho, alertas de reposição de estoque.

Por padrão, ambos são enviados sob a mesma identidade de envio, o que significa que **compartilham uma única reputação de remetente**. Se uma campanha de marketing gerar reclamações de spam ou atingir endereços obsoletos, essa reputação cai — e suas confirmações de pedido e redefinições de senha podem começar a cair na caixa de spam também.

Um **domínio de envio de marketing** resolve isso. Você configura uma segunda identidade de envio — em seu próprio subdomínio, como `news.yourstore.com` — e a marca para marketing. O Spwig então envia todas as campanhas a partir dessa identidade e mantém os e-mails transacionais no seu domínio principal. Uma campanha ruim não pode mais arrastar para baixo os e-mails que seus clientes *precisam* receber.

> Isso se aplica a lojas auto-hospedadas. Nos planos hospedados pelo Spwig, a reputação de envio é gerenciada para você.

## Como o Spwig decide qual identidade usar

Assim que uma conta de envio de marketing existir, o roteamento é automático — você não precisa marcar nada:

- **E-mail de marketing** (campanhas, jornadas, newsletters, recuperação de carrinho, reposição de estoque) →
  o domínio de envio de marketing.
- **E-mail transacional** (pedidos, envio, redefinições de senha, verificação) → seu domínio
  principal.

Se você nunca configurar um domínio de marketing, nada muda: tudo continua sendo enviado
a partir da sua conta padrão exatamente como antes.

## Configuração

Você pode começar por qualquer um dos pontos de entrada:

- O botão **"Configurar domínio de marketing"** no banner do painel do Campaign Studio, ou
- **Contas de E-mail → "Domínio de envio de marketing"**.

![O painel do Campaign Studio com o banner "Proteja seu e-mail transacional" e seu botão Configurar domínio de marketing](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-nudge.webp)

![O botão Domínio de envio de marketing na lista de Contas de E-mail, ao lado de Navegar por Provedores](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-button.webp)

Ambos abrem o assistente de configuração de e-mail pré-marcado para uma conta de marketing. Em seguida:

1. **Escolha um subdomínio.** Use algo como `news.yourstore.com` ou
   `mail.yourstore.com`. Este é o passo mais importante: a identidade de marketing deve ser um
   **(sub)domínio diferente** daquele usado pelo seu e-mail transacional — essa separação
   é exatamente o que protege sua reputação transacional. Enviar marketing a partir do seu
   domínio principal não oferece isolamento.
2. **Insira o endereço do remetente** naquele subdomínio, por exemplo, `news@news.yourstore.com`.
3. **Adicione os registros DNS.** O assistente gera registros SPF, DKIM e DMARC para o
   subdomínio — incluindo uma chave DKIM exclusiva para essa identidade de marketing. Adicione-os no
   seu provedor DNS (o assistente tem botões de copiar e abas por provedor), depois execute a
   verificação até que todos os registros sejam aprovados.
4. **Conclua.** A conta é criada e marcada como **Somente Marketing**. A partir de agora, suas
   campanhas serão enviadas a partir dela.

Você pode confirmar que funcionou na lista de **Contas de E-mail**: você verá uma segunda conta com
o propósito **Somente Marketing**, e o banner do Campaign Studio desaparece.

## Bom saber

- **Você não pode quebrar acidentalmente o e-mail transacional.** O Spwig não permite que você defina sua única
  conta como "Somente Marketing", nem desative/exclua sua última conta transacional — sempre
  haverá um destino para confirmações de pedido e redefinições de senha.
- **Aqueça gradualmente.** Um domínio de envio totalmente novo ainda não tem reputação.

Aumente seu
  volume ao longo de algumas semanas, em vez de disparar para toda a sua lista no primeiro dia.
- **Mantenha o DNS do subdomínio saudável.** SPF, DKIM e DMARC no subdomínio de marketing
  precisam permanecer válidos, assim como no seu domínio principal.

Veja o [Email Deliverability Runbook](deliverability) para obter uma visão completa.
- **O consentimento ainda se aplica.** E-mails de marketing são enviados apenas para assinantes que optaram por recebê-los,
  e cada campanha contém um link de cancelamento de assinatura — separar o domínio não muda
  nada disso.