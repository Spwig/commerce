---
title: Gerenciamento de Token de Sincronização
---

Tokens de sincronização são credenciais seguras que permitem que duas instalações do Spwig se comuniquem entre si. Antes de você conseguir sincronizar configurações ou migrar dados entre lojas, você precisa gerar um token na loja **receptora** e fornecê-lo à loja **enviadora**.

## Como os Tokens de Sincronização Funcionam

Um token de sincronização é uma chave de API visível apenas uma vez que autentica solicitações entre duas instalações do Spwig. Quando você configura uma conexão, a loja remota usa esse token para provar que tem permissão para ler ou escrever em sua loja.

- Os tokens são gerados na loja que será **conectada** (o destino)
- Cada token pode ser visualizado apenas uma vez, imediatamente após a geração
- Os tokens podem ser revogados a qualquer momento para cortar imediatamente o acesso
- Uma loja pode ter vários tokens ativos para diferentes conexões

## Gerando um Token

1. Navegue até **Data Migration > Spwig-to-Spwig Sync** no menu lateral do administrador
2. Clique em **Manage Tokens** no painel de sincronização
3. Insira um nome descritivo para o token (ex.: "Staging Server" ou "Production Sync")
4. Clique em **Generate Token**
5. **Copie o token imediatamente** -- ele não será mostrado novamente

> **Importante:** Armazene o token de forma segura. Se você perder, será necessário gerar um novo.

## Usando um Token

Depois que você tiver um token da loja de destino:

1. Vá para o painel **Spwig-to-Spwig Sync** na loja que iniciará a conexão
2. Inicie uma nova **Settings Sync** ou **Full Migration**
3. Na etapa de conexão, insira a URL da loja de destino e cole o token
4. Clique em **Test Connection** para verificar se funciona
5. A conexão será salva para uso futuro

## Revogando um Token

Se um token for comprometido ou não for mais necessário:

1. Vá para **Manage Tokens** no painel de sincronização
2. Localize o token que deseja revogar
3. Clique no botão **Revoke**
4. Confirme a revogação

A revogação de um token entra em vigor imediatamente. Qualquer conexão ativa usando esse token parará de funcionar e precisará ser reconfigurada com um novo token.

## Boas Práticas

- **Nomeie os tokens de forma descritiva** para que você saiba a qual conexão cada token pertence
- **Revogue tokens não utilizados** para minimizar a exposição de segurança
- **Gerencie tokens separados** para cada loja conectada, em vez de compartilhar um único token entre várias lojas
- **Regenere tokens periodicamente** como parte de sua rotina de segurança, especialmente após mudanças no pessoal