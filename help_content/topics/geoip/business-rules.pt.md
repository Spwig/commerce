---
title: Regras de Negócio com Base na Localização
---

Regras de negócio com base na localização permitem que você execute ações automaticamente quando um visitante chega de um país, região ou tipo de dispositivo específico. Você pode usar regras para definir uma moeda para clientes de uma região específica, redirecionar visitantes para uma página localizada, mostrar um banner promocional ou restringir o acesso a certos conteúdos.

As regras são avaliadas em ordem de prioridade toda vez que uma sessão de visitante é estabelecida. Quando uma regra corresponde, suas ações configuradas são executadas imediatamente.

## Como as regras de negócio funcionam

Cada regra é composta por duas partes:

- **Condições** — os critérios que devem ser atendidos para que a regra seja acionada (ex.: "visitante é da Alemanha")
- **Ações** — o que acontece quando todas as condições forem atendidas (ex.: "definir moeda para EUR")

Condições e ações são armazenadas como objetos JSON no formulário da regra. O Spwig avalia todas as regras ativas em ordem de prioridade (números mais baixos primeiro) e aplica quaisquer regras que correspondam.

## Navegando até as regras de negócio

Navegue até **Clientes > Regras de Negócio** para ver todas as suas regras configuradas. A lista mostra o nome de cada regra, status, prioridade, quantas vezes ela foi acionada e quando foi acionada pela última vez.

Clique em qualquer regra para visualizá-la ou editá-la, ou clique em **+ Adicionar Regra de Negócio** para criar uma nova.

## Criando uma regra de negócio

### Etapa 1: informações básicas

Preencha os detalhes de identificação da regra:

- **Nome** — um nome claro e descritivo (ex.: `Definir EUR para Zona Euro`)
- **Descrição** — notas opcionais explicando o propósito da regra
- **Ativo** — marque este campo para ativar a regra; desmarque para pausá-la sem excluí-la
- **Prioridade** — números mais baixos são executados primeiro; use `10`, `20`, `30` para deixar espaço para regras futuras

### Etapa 2: definir condições

No campo **Condições**, insira um objeto JSON que descreva quando a regra deve ser acionada. Todas as condições no objeto devem ser verdadeiras para que a regra corresponda.

#### Chaves de condição disponíveis

| Condição | Formato | Exemplo |
|-----------|--------|---------|
| `country_in` | Array de códigos de país ISO | `["DE", "FR", "IT"]` |
| `country_not_in` | Array de códigos de país ISO | `["US", "CA"]` |
| `region_in` | Array de nomes de região | `["Bavaria", "Catalunha"]` |
| `region_not_in` | Array de nomes de região | `["Quebec"]` |
| `is_mobile` | Booleano | `true` |
| `is_vpn` | Booleano | `false` |

#### Exemplos de condições

Visitantes da Alemanha, França ou Itália:
```json
{
  "country_in": ["DE", "FR", "IT"]
}
```

Visitantes dos Estados Unidos que estão em dispositivos móveis:
```json
{
  "country_in": ["US"],
  "is_mobile": true
}
```

Visitantes fora da União Europeia:
```json
{
  "country_not_in": ["AT","BE","BG","CY","CZ","DE","DK","EE","ES","FI","FR","GR","HR","HU","IE","IT","LT","LU","LV","MT","NL","PL","PT","RO","SE","SI","SK"]
}
```

### Etapa 3: definir ações

No campo **Ações**, insira um objeto JSON que descreva o que deve acontecer quando a regra for acionada.

#### Chaves de ação disponíveis

| Ação | Formato | Descrição |
|--------|--------|-------------|
| `set_currency` | String com código de moeda | Defina uma moeda pré-selecionada para o visitante |
| `set_language` | String com código de idioma | Defina o idioma de exibição |
| `show_banner` | Booleano | Acione um banner promocional |
| `redirect_to` | String com caminho de URL | Redirecione o visitante para uma URL diferente |

#### Exemplos de ações

Definir moeda para Euro:
```json
{
  "set_currency": "EUR"
}
```

Redirecionar para uma página de destino localizada:
```json
{
  "redirect_to": "/de/"
}
```

Definir moeda e idioma juntos:
```json
{
  "set_currency": "GBP",
  "set_language": "en"
}
```

## Exemplos práticos

### Exemplo: regra de moeda da Zona Euro

**Cenário:** Mostrar automaticamente preços em Euro para visitantes de países da Zona Euro.

| Campo | Valor |
|-------|-------|
| Nome | `Zona Euro — Definir EUR` |
| Prioridade | `10` |
| Ativo | Marcado |
| Condições | `{"country_in": ["AT","BE","DE","ES","FI","FR","GR","IE","IT","LU","NL","PT"]}` |
| Ações | `{"set_currency": "EUR"}` |

### Exemplo: regra de preços do Reino Unido

**Cenário:** Mostrar preços em GBP para visitantes do Reino Unido.

| Campo | Valor |
|-------|-------|
| Nome | `UK — Definir GBP` |
| Prioridade | `20` |
| Ativo | Marcado |
| Condições | `"{\"country_in\": [\"GB\"]}"` |
| Ações | `"{\"set_currency\": \"GBP\"}"` |

### Exemplo: redirecionar para uma seção de loja localizada

**Cenário:** Redirecionar visitantes da Austrália para uma página australiana dedicada.

| Campo | Valor |
|-------|-------|
| Nome | `Austrália — Redirecionar` |
| Prioridade | `30` |
| Ativo | Marcado |
| Condições | `"{\"country_in\": [\"AU\"]}"` |
| Ações | `"{\"redirect_to\": \/au\/}"` |

## Testando regras

Você pode verificar se uma regra corresponde ao perfil esperado do visitante sem esperar pelo tráfego real:

1. Na lista de Regras de Negócio, selecione a regra usando seu checkbox
2. Abra o menu **Ação** e escolha **Testar regras selecionadas**
3. Clique em **Ir**

O Spwig avaliará a regra contra um perfil de visitante baseado nos EUA e relatará se ela correspondeu e quais ações teriam sido acionadas.

## Monitoramento da atividade da regra

A coluna **Acionada** na lista de regras mostra quantas vezes cada regra foi acionada. Clique em uma regra para ver o carimbo de tempo **Última vez acionada** na seção Estatísticas.

Use a ação **Redefinir estatísticas** para zerar as contagens de acionamento se quiser iniciar as medições a partir de uma data específica após fazer alterações em uma regra.

## Dicas

- Defina prioridades com lacunas (10, 20, 30) em vez de números sequenciais (1, 2, 3) para que você possa inserir novas regras posteriormente sem renumerar tudo
- As regras são acionadas na ordem de prioridade e todas as regras correspondentes são aplicadas — se duas regras definirem a mesma moeda, a ação da regra com menor prioridade (número mais alto) será aplicada por último
- Use o interruptor **Ativo** para pausar temporariamente uma regra durante promoções sem excluir a configuração
- Sempre teste uma nova regra antes de ativá-la em um ambiente de produção para garantir que as condições estejam corretas
- A detecção de VPN (`"is_vpn": true`) está disponível se quiser aplicar um tratamento diferente a visitantes que mascaram seu local, mas lembre-se de que alguns clientes legítimos usam VPNs por privacidade