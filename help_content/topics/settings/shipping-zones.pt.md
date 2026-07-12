---
title: Zonas de Envio
---

Zonas de envio definem regiões geográficas para taxas de envio direcionadas — agrupe países, estados ou códigos postais em zonas, depois vincule métodos de envio a zonas específicas para controle preciso de taxas. As zonas usam correspondência baseada em prioridade quando os endereços qualificam-se para múltiplas zonas (a prioridade mais alta vence). Este sistema permite estratégias de precificação sofisticadas: cobrar mais por áreas remotas, oferecer envio gratuito dentro do país ou fornecer taxas descontadas para regiões específicas.

Use zonas quando você precisar de diferentes custos de envio para diferentes áreas geográficas, desde a divisão simples entre doméstico vs internacional até precificação em níveis complexa multi-região.

## Entendendo Zonas de Envio

**O que são zonas**: Regiões geográficas nomeadas definidas por países, estados/províncias e padrões de códigos postais.

**Como as zonas funcionam**:
1. O cliente insere o endereço de envio no checkout
2. O sistema avalia todas as zonas ativas
3. As zonas que correspondem ao endereço do cliente são candidatas
4. Se múltiplas zonas correspondem, a zona com maior prioridade vence
5. Os métodos de envio vinculados à zona vencedora são exibidos
6. Métodos não vinculados a nenhuma zona (ou vinculados a uma zona correspondente) são mostrados

**Componentes da zona**:
- **Nome**: Identificador da zona (ex: "Doméstico", "UE", "Áreas Remotas")
- **Países**: Lista de códigos de países incluídos (vazio = todos os países)
- **Estados/Províncias**: Restrições de estado por país (opcional)
- **Padrões de Código Postal**: Padrões de expressão regular para correspondência de códigos postais (opcional)
- **Prioridade**: Número mais alto = maior prioridade quando múltiplas zonas correspondem

---

## Lógica de Correspondência de Zona

As zonas usam **narrowing progressivo** para corresponder aos endereços:

### Nível 1: Correspondência por País

**Lista de países vazia** → A zona corresponde a TODOS os países

**Lista de países fornecida** → O país do endereço deve estar na lista

Exemplo:
```
Zona: "Doméstico"
Países: ["US"]
→ Correspondência: Qualquer endereço dos EUA
→ Não corresponde: Canadá, Reino Unido, etc.
```

### Nível 2: Correspondência por Estado/Província

**Nenhum estado definido** → A zona corresponde a TODOS os estados nos países permitidos

**Estados definidos para países específicos** → O estado do endereço deve corresponder

Exemplo:
```
Zona: "West Coast"
Países: ["US"]
Estados: {"US": ["CA", "OR", "WA"]}
→ Correspondência: Endereços de Califórnia, Oregon e Washington
→ Não corresponde: Nova York, Texas, etc.
```

### Nível 3: Correspondência por Código Postal

**Nenhum padrão definido** → A zona corresponde a TODOS os códigos postais nos países/estados permitidos

**Padrões definidos** → O código postal do endereço deve corresponder a pelo menos um padrão

Exemplo:
```
Zona: "Los Angeles Metro"
Países: ["US"]
Estados: {"US": ["CA"]}
Padrões de Código Postal: ["^90[0-9]{3}$", "^91[0-9]{3}$"]
→ Correspondência: 90001, 91210, 90245
→ Não corresponde: 94102 (San Francisco)
```

**Exemplos de Padrões de Expressão Regular**:
- `^90[0-9]{3}$` - Área de Los Angeles (90000-90999)
- `^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$` - Formato de código postal canadense (K1A 0B1)
- `^SW[0-9]{1,2}` - Códigos postais do Reino Unido começando com SW

---

## Seleção de Zona com Base em Prioridade

Quando múltiplas zonas correspondem a um endereço, a **prioridade** determina qual zona se aplica:

**Como a prioridade funciona**:
- Número mais alto = maior prioridade
- Se o endereço corresponder a zonas com prioridade 100 e 50, a prioridade 100 vence
- Apenas os métodos de envio da zona vencedora estão disponíveis

**Casos de uso**:

**Cenário 1: Específico sobrepõe Geral**
```
Zona A: "Remote Alaska"
  Países: ["US"]
  Estados: {"US": ["AK"]}
  Prioridade: 100

Zona B: "Doméstico USA"
  Países: ["US"]
  Prioridade: 50

Endereço: Anchorage, AK
→ Correspondência: Ambas as zonas
→ Prioridade 100 vence
→ A zona "Remote Alaska" se aplica (custo de envio mais alto)
```

**Cenário 2: Código Postal sobrepõe Estado**
```
Zona A: "Manhattan Premium"
  Países: ["US"]
  Estados: {"US": ["NY"]}
  Padrões de Código Postal: ["^100[0-2][0-9]$"]
  Prioridade: 100

Zona B: "New York State"
  Países: ["US"]
  Estados: {"US": ["NY"]}
  Prioridade: 50

Endereço: New York, NY 10001
→ Correspondência: Ambas as zonas
→ Prioridade 100 vence
→ "Manhattan Premium" se aplica (serviço de entrega premium)
```

---

## Criando Zonas de Envio

**Fluxo de Trabalho Passo a Passo**:

1. **Navegue até Zonas**
   - Vá para Configurações > Envio > Zonas de Envio
   - Clique em "Adicionar Zona de Envio"

2. **Configuração Básica**
   - **Nome**: Identificador descritivo (ex.: "União Europeia", "Costa Oeste", "Áreas Remotas")
   - **Prioridade**: Defina a importância relativa (100 para específico, 50 para geral, 1 para fallback)
   - **Ativo**: Ative/desative com o botão de alternância

3. **Definir Cobertura Geográfica**

   **Opção A: Todos os Países** (deixe a lista de países vazia)
   - A zona corresponde a todos os endereços globalmente
   - Use para zonas padrão/fallback

   **Opção B: Países Específicos**
   - Clique em "Adicionar País"
   - Selecione países do menu suspenso (US, CA, UK, etc.)
   - Repita para todos os países incluídos

   **Opção C: Estados/Províncias Específicos**
   - Após adicionar países, clique em "Adicionar Estados" para cada país
   - Selecione estados do menu suspenso
   - Exemplo: US → CA, OR, WA para Costa Oeste

   **Opção D: Padrões de Códigos Postais** (avançado)
   - Insira padrões de expressão regular (um por linha)
   - Teste os padrões com códigos postais de exemplo
   - Clique em "Validar Padrões" para verificar a sintaxe

4. **Vincular a Métodos de Envio**
   - Os métodos podem ser vinculados ao editar o método (não na configuração da zona)
   - Ou vincule zonas a métodos existentes: Edite o Método → Zonas de Envio → Selecione as zonas

5. **Definir Prioridade de Exibição**
   - Zonas com prioridade mais alta substituem zonas com prioridade mais baixa quando várias correspondem
   - Recomendado: Zonas específicas (100), zonas regionais (50), zona padrão (1)

6. **Ativar Zona**
   - Ative "Ativo" = Sim
   - Salve

---

## Configurações de Zona Comuns

### Configuração 1: Nacional vs. Internacional

**Objetivo**: Taxas diferentes para nacional vs. todos os outros países.

```
Zona 1: "Nacional"
  Países: [Código do Seu País]
  Prioridade: 50

Zona 2: "Internacional"
  Países: [Deixe vazio ou selecione todos os outros países]
  Prioridade: 1
```

**Métodos de Envio**:
- "Envio Nacional" → Vinculado à zona Nacional
- "Envio Internacional" → Vinculado à zona Internacional

---

### Configuração 2: Internacional por Regiões

**Objetivo**: Taxas diferentes para UE, América do Norte, Ásia, Resto do Mundo.

```
Zona 1: "União Europeia"
  Países: [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Prioridade: 100

Zona 2: "América do Norte"
  Países: [US, CA, MX]
  Prioridade: 100

Zona 3: "Ásia-Pacífico"
  Países: [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Prioridade: 100

Zona 4: "Resto do Mundo"
  Países: [Deixe vazio]
  Prioridade: 1
```

**Métodos de Envio**:
- "Envio da UE" → Zona da UE
- "Envio da América do Norte" → Zona da América do Norte
- "Envio do Pacífico Asiático" → Zona do Pacífico Asiático
- "Envio Padrão Internacional" → Zona Resto do Mundo

---

### Configuração 3: Sobretaxa para Áreas Remotas

**Objetivo**: Adicione uma sobretaxa para códigos postais remotos dentro da zona nacional.

```
Zona 1: "Doméstico Remoto"
  Países: [US]
  Padrões de Código Postal: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alasca, Havaí
  Prioridade: 100

Zona 2: "Doméstico Padrão"
  Países: [US]
  Prioridade: 50
```

**Métodos de Envio**:
- "Envio Remoto" → Zona Doméstico Remoto (custo mais alto)
- "Envio Padrão" → Zona Doméstico Padrão

---

### Configuração 4: Zonas por Estado

**Objetivo**: Taxas diferentes para cada região dos EUA.

```
Zona 1: "Costa Oeste"
  Países: [US]
  Estados: {"US": ["CA", "OR", "WA"]}
  Prioridade: 100

Zona 2: "Costa Leste"
  Países: [US]
  Estados: {"US": ["NY", "NJ", "CT", "MA", "PA"]}
  Prioridade: 100

Zona 3: "Meio-Oeste"
  Países: [US]
  Estados: {"US": ["IL", "IN", "OH", "MI", "WI"]}
  Prioridade: 100

Zona 4: "Sul"
  Países: [US]
  Estados: {"US": ["TX", "FL", "GA", "NC", "SC"]}
  Prioridade: 100

Zona 5: "Outros Estados dos EUA"
  Países: [US]
  Prioridade: 50
```

---

## Exemplos de Padrões de Código Postal

Códigos postais usam **regex** (expressões regulares) para correspondência de padrões:

### Estados Unidos (Códigos ZIP)

**Formato**: 5 dígitos (ex.: 90210)

```
Califórnia (90000-96199):  ^9[0-6][0-9]{3}$
Nova Iorque (10000-14999):    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599):  ^(7[5-9]|885)[0-9]{2}$
Alasca (99500-99999):      ^99[5-9][0-9]{2}$
```

### Canadá (Códigos Postais)

**Formato**: A1A 1A1 (letra-número-letra espaço número-letra-número)


Todos os códigos postais canadenses:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$",
  "Ontario (K, L, M, N, P):    ^[KLMNP][0-9][A-Z] [0-9][A-Z][0-9]$",
  "Quebec (G, H, J):           ^[GHJ][0-9][A-Z] [0-9][A-Z][0-9]$",
  "### Reino Unido (Códigos postais)",
  "**Formato**: AA1A 1AA ou A1A 1AA",
  "London (E, EC, N, NW, SE, SW, W, WC):  ^(E|EC|N|NW|SE|SW|W|WC)[0-9]{1,2}",
  "Manchester (M):                        ^M[0-9]{1,2}",
  "Birmingham (B):                        ^B[0-9]{1,2}",
  "### Austrália (Códigos postais)",
  "**Formato**: 4 dígitos (ex., 2000)",
  "New South Wales (1000-2999):  ^[12][0-9]{3}$",
  "Victoria (3000-3999, 8000-8999):  ^[38][0-9]{3}$",
  "Queensland (4000-4999, 9000-9999):  ^[49][0-9]{3}$",
  "### Teste de Padrões",
  "**Antes de salvar os padrões**, teste com códigos postais conhecidos:",
  "1. Insira o padrão: `^90[0-9]{3}$`",
  "2. Entrada de teste: "90210" → Deve corresponder",
  "3. Entrada de teste: "10001" → Deve NÃO corresponder",
  "4. Entrada de teste: "9021" → Deve NÃO corresponder (apenas 4 dígitos)",
  "Use testadores de expressões regulares online (regex101.com) para validar padrões complexos.",
  "---",
  "## Resumo da Cobertura da Zona",
  "As zonas exibem **resumo da cobertura** na visão de lista do administrador, mostrando o que está incluído:",
  "**Exemplos**:",
  "- "Todos os países" → Nenhuma restrição de país",
  "- "US, CA, MX" → 3 países",
  "- "US (CA, OR, WA)" → EUA com 3 estados",
  "- "US (90xxx-91xxx)" → EUA com padrões de códigos postais",
  "**Use o Resumo Para**:",
  "- Verificar rapidamente a cobertura da zona sem abrir",
  "- Identificar sobreposições ou lacunas na cobertura",
  "- Fazer uma auditoria da configuração da zona de olho",
  "---",
  "## Linkando Zonas a Métodos de Envio",
  "Zonas e métodos têm **relação muitos-para-muitos**:",
  "**Do Lado do Método** (Recomendado):",
  "1. Edite o Método de Envio",
  "2. Role até a seção "Zonas de Envio"",
  "3. Selecione as zonas aplicáveis (seleção múltipla)",
  "4. Salve o método",
  "**Do Lado da Zona**:",
  "- As zonas não se vinculam diretamente aos métodos",
  "- O vinculo é sempre feito a partir da configuração do método",
  "**Comportamento Método-Zona**:",
  "**Nenhuma zona vinculada** → Método disponível para TODOS os endereços",
  "**Zonas vinculadas** → Método só está disponível se o endereço do cliente corresponder a pelo menos uma zona vinculada",
  "**Exemplo**:",
  "```,
  "Método: "Standard Nacional"",
  "Zonas vinculadas: ["Doméstico EUA"]",
  "→ Apenas mostrado para endereços dos EUA",
  "Método: "Expresso Internacional"",
  "Zonas vinculadas: ["EU", "Pacífico Asiático", "Resto do Mundo"]",
  "→ Mostrado para todos os endereços não dos EUA",
  "```",
  "---",
  "## Testando Correspondência de Zona",
  "Antes de ir ao ar, teste a configuração da zona:",
  "1. **Crie Pedidos de Teste**",
  "- Use endereços em diferentes zonas",
  "- Verifique a correspondência correta da zona",
  "2. **Verifique a Resolução de Prioridade**",
  "- Use um endereço que corresponda a múltiplas zonas",
  "- Verifique se a zona de maior prioridade vence",
  "- Confirme que os métodos de envio esperados aparecem",
  "3. **Teste Casos Limítrofes**",
  "- Códigos postais de fronteira (ex., 90999 vs 91000)",
  "- Limites de estados",
  "- Endereços internacionais com códigos postais semelhantes",
  "4. **Use a Ferramenta de Pré-visualização de Zona** (se disponível)",
  "- Insira um endereço de teste",
  "- Veja quais zonas correspondem",
  "- Veja a resolução de prioridade",
  "---",
  "## Solução de Problemas",
  "**Problema 1: Nenhum método de envio disponível no checkout**",
  "**Causas**:",
  "- O endereço do cliente não corresponde a nenhuma zona",
  "- Todos os métodos estão vinculados a zonas que não correspondem",
  "- Não existem métodos sem restrições de zona",
  "**Solução**:",
  "- Crie uma zona de fallback (todos os países, prioridade 1)",
  "- OU remova as restrições de zona de pelo menos um método",
  "- Verifique os padrões de país/estado/código postal da zona",
  "---",
  "**Problema 2: Correspondência de zona incorreta**",
  "**Causas**:",
  "- Uma zona de menor prioridade foi selecionada, apesar de uma zona de maior prioridade corresponder",
  "- Erro de sintaxe no padrão de código postal (o padrão falha silenciosamente)",
  "- Mismatch de código de estado (CA vs California)",
  "**Solução**:",
  "- Verifique os valores de prioridade (número mais alto = prioridade mais alta)",
  "- Teste os padrões de código postal com validador de expressões regulares",
  "- Use códigos de estado com duas letras (CA, não California)",
  "---",
  "**Problema 3: Método inesperado mostrado**",
  "**Causas**:",
  "- O método não tem zonas vinculadas (disponível em todos os lugares)",
  "- Múltiplas zonas correspondem, a zona inesperada tem prioridade mais alta",
  "- A cobertura da zona se sobrepõe acidentalmente",
  "**Solução**:",
  "- Revise as zonas vinculadas ao método",
  "- Verifique a prioridade das zonas correspondentes",
  "- Faça uma auditoria do resumo da cobertura da zona para sobreposições",
  "---",
  "## Dicas",
  "Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

- **Comece com 2 zonas** - Nacionais e Internacionais, expanda conforme necessário
- **Use a prioridade com sabedoria** - Zonas específicas 100, regionais 50, fallback 1
- **Teste padrões postais com cuidado** - Erros de regex falham silenciosamente, causando que as zonas não correspondam
- **Documente a lógica da zona** - Adicione notas à descrição da zona explicando a intenção de cobertura
- **Evite zonas excessivas** - Muitas zonas complicam a configuração; use promoções de envio para cenários complexos
- **Use códigos de estado, não nomes** - "CA" e não "California", "NY" e não "New York"
- **Crie uma zona de fallback** - Todos os países, prioridade 1, garante que pelo menos uma opção de envio esteja sempre disponível
- **Monitore o desempenho das zonas** - Se muitos clientes viram "nenhum envio disponível", faça uma auditoria da cobertura das zonas
- **Atualize as zonas para novas regiões** - Adicione países à zona da UE quando novos membros se juntarem
- **Use nomes descritivos** - "UE (Excluindo o Reino Unido)" é melhor que "Zona 3"
- **Teste com endereços reais** - Use endereços reais dos clientes durante os testes, não endereços inventados