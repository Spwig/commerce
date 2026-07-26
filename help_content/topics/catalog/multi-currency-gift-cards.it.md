---
title: Carte regalo a multi-valuta
---

Se vendi a clienti in diversi paesi, puoi emettere carte regalo in valute specifiche. Ad esempio, un cliente della Nuova Zelanda può acquistare una carta regalo da 50 NZD e il beneficiario la può utilizzare in NZD — il valore nominale rimane lo stesso indipendentemente dalle fluttuazioni del tasso di cambio.

Questa funzione richiede che la multi-valuta sia abilitata con almeno un fornitore di tassi di cambio configurato.

> **Le vendite di carte regalo sono temporaneamente sospese** mentre completiamo il flusso di consegna automatica — consulta l'argomento **Carte regalo** per i dettagli. Puoi comunque configurare una **Valuta Carta Regalo** su un prodotto in modo che sia pronto per la vendita non appena le vendite riprenderanno, e puoi emettere una carta regalo specifica per una valuta manualmente oggi nello stesso modo in cui emetteresti qualsiasi altra carta regalo (imposta il **Valore Iniziale** nella valuta in cui desideri che la carta sia denominata).

## Funzionamento

Quando imposti una **Valuta Carta Regalo** su un prodotto carta regalo, il sistema converte il prezzo del prodotto nella valuta target al momento dell'acquisto utilizzando il tasso di cambio corrente. La carta regalo risultante è denominata in quella valuta e può essere utilizzata solo da clienti che effettuano acquisti nella stessa valuta.

| Passo | Cosa accade |
|------|-------------|
| **Configurazione del prodotto** | Imposti il prezzo della carta regalo in valuta base e scegli una valuta target (es. NZD) |
| **Acquisto** | Un cliente acquista la carta regalo. Il prezzo base viene convertito in NZD al tasso di cambio corrente |
| **Carta regalo creata** | La carta regalo viene emessa con il valore in NZD (es. NZ$78,50) |
| **Utilizzo** | Il beneficiario applica il codice al checkout mentre effettua acquisti in NZD. Il saldo in NZD viene detratto |

## Requisiti

Prima di configurare le carte regalo a multi-valuta, assicurati di avere:

1. **Multi-valuta abilitata** — Vai a **Impostazioni > Impostazioni del negozio** e abilita il supporto per la multi-valuta
2. **Valute supportate configurate** — Aggiungi le valute che desideri offrire (es. NZD, SGD, EUR)
3. **Fornitore di tassi di cambio connesso** — Vai a **Impostazioni > Tassi di cambio** e configura un fornitore in modo che siano disponibili i tassi in tempo reale

## Configurazione di un prodotto carta regalo a multi-valuta

### Passo 1: Crea o modifica un prodotto carta regalo

1. Vai a **Prodotti > Tutti i prodotti**
2. Clicca su **+ Aggiungi prodotto** o apri un prodotto carta regalo esistente
3. Imposta **Tipo di prodotto** su **Carta regalo**

### Passo 2: Imposta la valuta della carta regalo

1. Clicca sulla scheda **Carta regalo**
2. Configura le impostazioni del valore come di consueto (importi fissi, importi personalizzati o entrambi)
3. Alla fine della scheda Carta regalo, trova il menu a discesa **Valuta Carta Regalo**
4. Seleziona la valuta target (es. **NZD - Dollaro Nuova Zelanda**)
5. Salva il prodotto

Il menu a discesa mostra tutte le valute abilitate nelle impostazioni del tuo negozio. Selezionare **Valuta base del negozio (predefinita)** significa che le carte regalo saranno emesse nella tua valuta base — questo è il comportamento standard.

### Passo 3: Imposta il prezzo

Imposta il prezzo del prodotto nella tua valuta base come faresti di solito. Quando un cliente acquista questa carta regalo, il prezzo viene automaticamente convertito nella valuta target utilizzando il tasso di cambio corrente.

**Esempio:** La tua valuta base è USD. Crei un prodotto carta regalo con un prezzo di 50 USD e imposti la **Valuta Carta Regalo** su NZD. Se il tasso di cambio è 1 USD = 1,57 NZD, la carta regalo risultante avrà un valore di NZ$78,50.

## Corrispondenza delle valute e utilizzo

Le carte regalo a multi-valuta utilizzano **utilizzo nella stessa valuta** — la valuta attiva di acquisto del cliente deve corrispondere alla valuta della carta regalo.

### Esperienza del cliente

- Un cliente che acquista in **NZD** può applicare una carta regalo in NZD al checkout
- Un cliente che acquista in **USD** non può applicare una carta regalo in NZD — vedrà un messaggio che spiega la discrepanza delle valute
- I clienti possono cambiare la valuta di acquisto utilizzando il selettore di valuta sul tuo sito web prima di applicare la carta regalo

### Funzionamento del saldo

Il saldo della carta regalo è sempre tracciato nella sua valuta nativa:

- Una gift card da NZ$78.50 inizia con un saldo di NZ$78.50
- Se un cliente effettua un acquisto di NZ$30, il saldo rimanente è NZ$48.50
- Il saldo non varia con i tassi di cambio — il valore nominale è fisso

Quando la gift card viene applicata al checkout, il sistema converte lo sconto nella tua valuta base internamente per i calcoli dell'ordine, ma il saldo della gift card viene sempre addebitato nella sua valuta nativa.

## Gestione di gift card a multi-valuta

Naviga verso **Prodotti > Gift Cards** per visualizzare tutte le gift card emesse. Le gift card a multi-valuta vengono visualizzate con la loro valuta nativa:

- **Saldo** viene visualizzato nella valuta della gift card (es. NZ$48.50)
- **Transazioni** registrano le somme nella valuta della gift card
- **Valore iniziale** mostra l'importo convertito al momento dell'acquisto

### Verifica dei dettagli del tasso di cambio

Ogni transazione della gift card registra il tasso di cambio utilizzato al momento della transazione. Questo fornisce un completo registro contabile per scopi di audit.

## Esempi

### Esempio 1: Gift card regionale per la Nuova Zelanda

**Scenario:** Operi dagli Stati Uniti ma hai clienti in Nuova Zelanda. Vuoi vendere gift card denominate in NZD.

| Impostazione | Valore |
|---------|-------|
| Nome prodotto | Gift Card Nuova Zelanda |
| Tipo prodotto | Gift Card |
| Prezzo | $50.00 (USD — la tua valuta base) |
| Tipo di denominazione | Denominazioni fisse |
| Denominazioni fisse | 25, 50, 100, 200 |
| Valuta della gift card | NZD - Nuova Zelanda Dollaro |
| Scadenza | 365 giorni |

Quando un cliente seleziona la denominazione di $50:
- Il sistema converte $50 USD in NZD al tasso corrente
- Viene creata una gift card con l'equivalente in NZD (es. NZ$78.50)
- Il destinatario può riscuderla mentre acquista in NZD

### Esempio 2: Gift card a multi-valuta

**Scenario:** Vendiamo a clienti in Singapore, Australia e Regno Unito. Crea tre prodotti di gift card:

1. **SG Gift Card** — Valuta della gift card: SGD
2. **AU Gift Card** — Valuta della gift card: AUD
3. **UK Gift Card** — Valuta della gift card: GBP

Ogni prodotto converte il tuo prezzo base nella valuta target al momento dell'acquisto. I clienti in ciascuna regione possono riscuotere la gift card nella loro valuta locale.

### Esempio 3: Offerta mista di gift card

**Scenario:** Vuoi offrire sia gift card in valuta base che gift card regionali.

- **Store Gift Card** — Valuta della gift card: *Valuta base del negozio (predefinita)* — riscuotibile nella tua valuta base
- **NZ Gift Card** — Valuta della gift card: NZD — riscuotibile solo in NZD

Entrambi i prodotti possono coesistere nel tuo catalogo. I clienti vedranno in quale valuta è denominate le gift card quando controllano il saldo.

## Consigli

- Inizia con una singola valuta regionale e testa l'intero flusso (acquisto, consegna, riscossione) prima di aggiungere altre valute.
- Il tasso di cambio al momento dell'acquisto determina il valore della gift card. Se i tassi cambiano significativamente, il valore della gift card rimane fisso — questo protegge sia te che i tuoi clienti.
- Fai in modo che la valuta sia chiara nel nome del prodotto (es. "NZ Gift Card" o "Gift Card (NZD)") in modo che i clienti sappiano cosa stanno acquistando.
- Le gift card senza una valuta impostata continuano a funzionare esattamente come prima nella tua valuta base — i prodotti esistenti non sono influenzati.
- Monitora il tuo fornitore di tassi di cambio per assicurarti che i tassi siano aggiornati. Tassi obsoleti potrebbero portare a gift card sovravalue o sottovalue.
- Considera attentamente le tue denominazioni. Una denominazione di $25 USD si converte in circa NZ$39 — denominazioni arrotondate nella valuta target potrebbero apparire meglio. Puoi creare prodotti separati con denominazioni che siano numeri arrotondati nella valuta target.