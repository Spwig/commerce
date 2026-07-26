---
title: Login do Funcionário POS & Autenticação Biométrica
---

Todo pessoa que atende clientes em um caixa POS precisa de uma conta de funcionário com as permissões certas. Este tópico explica como criar essa conta, atribuir o funcionário a um terminal e configurar o login biométrico para que eles possam desbloquear o caixa com uma impressão digital, varredura facial ou chave de hardware em vez de digitar uma senha toda vez.

Para códigos PIN, limites de desconto e configurações de bloqueio de terminal, veja [Descontos de Funcionário POS & Segurança do Terminal](pos-staff-discounts).

## O que um funcionário precisa para usar um terminal POS

Para fazer login em um terminal POS, uma pessoa precisa:

1. Uma **conta de funcionário** — um usuário Spwig com a **bandeira de status de funcionário** ativada.
2. Um **papel que inclui acesso ao POS** — os papéis controlam o que um funcionário pode fazer dentro do administrador. Um papel com permissões de POS é necessário para acessar o caixa.
3. **Atribuição ao terminal** — o terminal deve listá-lo como um funcionário atribuído, ou ele deve ser atribuído no nível da localização da loja.

## Criando uma conta de funcionário elegível para POS

Navegue até **Funcionários & Contas > Funcionários** (ou vá para `/admin/accounts/staffmember/`).

1. Clique em **+ Adicionar Funcionário**.
2. Preencha o **nome**, **sobrenome** e **endereço de e-mail** do funcionário.
3. Defina uma senha temporária e peça ao funcionário para alterá-la na primeira entrada.
4. Certifique-se de que **Status de Funcionário** esteja marcado — é isso que permite que eles façam login no administrador e na aplicação POS.
5. Clique em **Salvar**.

> **Nota:** Não marque **Status de Superusuário** para caixas comuns ou supervisores. O status de superusuário pula todas as verificações de permissão e deve ser reservado para o proprietário da loja.

### Atribuindo um papel com acesso ao POS

Contas de funcionários por si só não têm permissões — os papéis concedem capacidades específicas. Após criar a conta, abra o registro do funcionário e vá para a seção **Papéis**. Atribua um papel que inclua acesso ao POS.

Para uma explicação completa de como funcionam os papéis e quais permissões incluir, veja [Papéis de Funcionário](staff-roles).

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: staff-user-list.webp
  description: Lista de funcionários mostrando um usuário elegível para POS com seu distintivo de papel
-->

![Lista de funcionários](/static/core/admin/img/help/pos-staff-login/staff-user-list.webp)

## Atribuindo funcionários a um terminal

As configurações seguem uma cascata: **Padrão do site → Grupo de lojas → Localização da loja → Terminal individual**. Para a maioria das lojas, o lugar certo para atribuir funcionários é no nível do terminal.

1. Navegue até **POS > Terminais** (ou vá para `/admin/pos_app/posterminal/`).
2. Abra o terminal que deseja configurar.
3. Vá para a guia **Atribuição de Funcionários**.
4. No campo **Funcionários Atribuídos**, procure e adicione o funcionário.
5. Clique em **Salvar**.

Funcionários que aparecem na lista **Funcionários Atribuídos** de um terminal podem selecionar seu nome na tela de login desse terminal. Funcionários não atribuídos a nenhum terminal ainda podem fazer login digitando seu e-mail diretamente.

> **Dica:** Se sua loja tiver muitos funcionários se movendo entre terminais, atribua-os no nível da localização da loja (armazém) em vez de terminal por terminal. Qualquer funcionário atribuído à localização tem automaticamente acesso a todos os terminais naquela localização.

## Fazer login no caixa POS

Quando um caixa abre a aplicação POS (`/pos/`) em um terminal, ele vê uma tela de seleção de funcionários. O fluxo de login funciona da seguinte forma:

1. O caixa toca ou clica no seu nome na lista (ou digita seu e-mail se não estiver listado).
2. Eles inserem sua senha.
3. Eles são autenticados e o caixa abre para seu turno.

Para desbloqueio com base em PIN (depois que o terminal se bloqueia durante um turno), veja [Descontos de Funcionário POS & Segurança do Terminal](pos-staff-discounts).

## Login biométrico

O login biométrico permite que um caixa toque em um sensor de impressão digital, olhe para uma câmera facial ou toque em uma chave de hardware em vez de digitar uma senha. Em um caixa ocupado, isso economiza vários segundos por turno e evita erros durante os horários de pico.

Spwig usa o padrão **WebAuthn** do navegador para login biométrico.

Um "credential de WebAuthn" é um par de chaves vinculado ao dispositivo: a chave privada é armazenada no hardware seguro do dispositivo e nunca sai dele.

O aplicativo POS comunica-se com esse hardware através do navegador.

### Dispositivos e navegadores que suportam login biométrico

WebAuthn é suportado por todos os navegadores modernos — Chrome, Edge, Firefox e Safari — em dispositivos com hardware compatível. Configurações comuns que funcionam bem:

| Dispositivo | Autenticador |
|--------|---------------|
| iPad (Touch ID) | Impressão digital via Safari ou Chrome |
| Tablet Android | Impressão digital ou rosto via Chrome |
| Tablet ou PC Windows | Windows Hello (impressão digital, rosto ou PIN) |
| Qualquer dispositivo + chave de segurança | Chave FIDO2 USB, NFC ou Bluetooth (ex. YubiKey) |
| iPhone (Face ID) | Rosto via Safari |

O aplicativo POS mostrará a opção de login biométrico apenas quando o navegador confirmar que uma credencial está registrada para o usuário atual nesse dispositivo.

### Como funciona o registro

O registro acontece no terminal POS, não no administrador. O membro da equipe deve primeiro concluir um login normal com senha, depois escolher configurar o login biométrico dentro do aplicativo POS. O navegador então solicitará que eles verifiquem sua identidade usando o sensor biométrico do dispositivo (ou uma chave de acesso salva em sua conta no iOS/macOS/Windows). Uma vez confirmado, a credencial é armazenada e o login biométrico estará disponível para futuras sessões nesse dispositivo.

Um único membro da equipe pode se registrar em múltiplos dispositivos — por exemplo, um tablet pessoal e um caixa compartilhado — e cada dispositivo armazena sua própria credencial.

> **Nota:** A exata frase do prompt de registro ("Registrar biométrico", "Configurar login com impressão digital", etc.) vem do aplicativo POS e pode variar por navegador e dispositivo.

### Fazer login com biométrico

Depois de registrado, o nome do caixa na tela de login mostrará um botão de login biométrico (ícone de impressão digital ou similar). O caixa:

1. Toque no nome no terminal de login.
2. Toque em **Fazer login com impressão digital** (ou equivalente).
3. Toque no sensor ou olhe para a câmera.
4. O terminal desbloqueia imediatamente.

Se a verificação biométrica falhar (dedo não reconhecido, rosto obscurecido), o caixa recorrerá à entrada de senha.

### Revogar uma credencial

Se um dispositivo for perdido, roubado ou um membro da equipe sair, você deve remover imediatamente suas credenciais biométricas.

1. Navegue até **Funcionários & Contas > Funcionários**.
2. Abra o registro do funcionário.
3. Role até a seção **Configurações do POS**.
4. Na linha **Desbloqueio Biométrico**, clique em **Remover Todos**.
5. Confirme a ação.

Isso remove todas as credenciais WebAuthn registradas para esse funcionário em todos os dispositivos. A próxima vez que eles tentarem usar o login biométrico em qualquer terminal, eles serão obrigados a fazer login com sua senha em vez disso.

> **Importante:** Remover credenciais aqui não impede o funcionário de fazer login com sua senha. Para revogar o acesso totalmente, desative também sua conta de funcionário ou remova-o da lista de funcionários atribuídos ao terminal.

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: webauthn-credential-list.webp
  description: Formulário de alteração do funcionário mostrando a seção Configurações do POS com a contagem de credenciais biométricas e o botão Remover Todos
-->

## Notas de segurança

- **As credenciais são vinculadas ao hardware.** A chave privada nunca sai do elemento seguro do dispositivo.

Se um tablet for roubado, um atacante não consegue extrair a chave biométrica — ainda assim, eles precisariam contornar a tela de bloqueio do dispositivo antes que o navegador liberasse a chave.
- **Perder um dispositivo não vaza uma senha.** O WebAuthn substitui a senha para esse dispositivo; a senha do funcionário é separada e não afetada.
- **Revogue imediatamente quando o funcionário sair.** Remova as credenciais biométricas e desative a conta do funcionário na mesma sessão ao desonboarding de um funcionário.
- **A biométrica em si nunca é transmitida.** A digital ou a varredura facial é processada totalmente pelo hardware do dispositivo.

Spwig recebe apenas uma resposta de desafio assinada, e não quaisquer dados biométricos.

## Solução de problemas

### O botão "Entrar com impressão digital" não está aparecendo

A opção biométrica só aparece quando:
- O funcionário tem uma credencial registrada nesse dispositivo específico.
- O navegador suporta WebAuthn (todos os navegadores modernos fazem isso — atualize se estiver usando uma versão mais antiga).

Se o botão estiver faltando, o funcionário ainda não registrou nesse dispositivo. Ele deve fazer login com sua senha e configurar o login biométrico através do aplicativo POS.

### Registro falhou

Motivos comuns:
- **Permissão do navegador negada.** O navegador pediu permissão para acessar o autenticador e o funcionário recusou. Ele precisa tentar novamente e tocar em **Permitir** quando solicitado.
- **Nenhum autenticador compatível encontrado.** O dispositivo não possui sensor de impressão digital, câmera facial ou chave de segurança anexada. Verifique o hardware do dispositivo.
- **Credencial duplicada.** O funcionário pode já ter se registrado nesse dispositivo. Credenciais existentes são excluídas durante o registro novamente para evitar duplicatas.

### A biométrica funcionou em um dispositivo, mas não em outro

Cada dispositivo armazena sua própria credencial. Registrar em um iPad não funciona automaticamente em um segundo iPad. O funcionário deve concluir o registro separadamente em cada dispositivo que usará.

### Chaves de passagem entre dispositivos

Alguns sistemas operacionais (iOS 16+, macOS Ventura+, Windows 11 com uma conta Microsoft) podem sincronizar chaves de passagem entre dispositivos por meio do iCloud Keychain ou Windows Hello. Se o funcionário se registrou usando uma chave de passagem sincronizada, ela pode funcionar automaticamente em vários dispositivos. O comportamento depende do sistema operacional e do navegador, e não do Spwig.

## Dicas

- Configure o login biométrico em registradores compartilhados antes que os funcionários cheguem para seu turno — o processo de registro de dois minutos é muito mais suave quando feito sem clientes esperando.
- Atribua um papel com permissões limitadas de POS aos caixas e um papel separado de gerente aos supervisores. Mantenha suas contas distintas da conta do proprietário da loja.
- Quando um funcionário mudar de dispositivo (novo tablet, novo telefone), faça com que ele se registre no novo dispositivo primeiro, depois revogue a credencial antiga no administrador se o dispositivo não estiver mais em uso.
- Para lojas com alta rotatividade de funcionários, revise a lista **Funcionários atribuídos** em cada terminal periodicamente e remova funcionários que não trabalham mais na localização.
- Se você usar chaves de segurança hardware (YubiKey ou similares), uma chave pode ser registrada em múltiplos terminais sem nenhuma alteração no administrador — simplesmente conecte a chave e conclua o registro em cada terminal.