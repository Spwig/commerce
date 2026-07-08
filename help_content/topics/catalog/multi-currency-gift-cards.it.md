---
title: Carte regalo a multi-valuta
---

Se vendi a clienti in diversi paesi, puoi emettere carte regalo in valute specifiche. Ad esempio, un cliente della Nuova Zelanda può acquistare una carta regalo da 50 NZD e il beneficiario la riscatta in NZD — il valore nominale rimane lo stesso indipendentemente dalle fluttuazioni del tasso di cambio.

Questa funzione richiede che la multi-valuta sia abilitata con almeno un fornitore di tassi di cambio configurato.

## Come funziona

Quando imposti una **Valuta Carta Regalo** su un prodotto carta regalo, il sistema converte il prezzo del prodotto nella valuta target al momento dell'acquisto utilizzando il tasso di cambio corrente. La carta regalo risultante è denominata in quella valuta e può essere riscattata solo da clienti che fanno acquisti nella stessa valuta.

| Passo | Cosa accade |
|------|-------------|
| **Impostazione del prodotto** | Imposti il prezzo del prodotto carta regalo nella vostra valuta base e scegliete una valuta target (es. NZD) |
| **Acquisto** | Un cliente acquista la carta regalo. Il prezzo base viene convertito in NZD al tasso di cambio corrente |
| **Carta regalo creata** | La carta regalo viene emessa con il valore in NZD (es. NZ$78,50) |
| **Riscatto** | Il beneficiario applica il codice al checkout mentre fa acquisti in NZD. Viene detratto il saldo in NZD |

## Requisiti preliminari

Prima di impostare le carte regalo a multi-valuta, assicurati di avere:

1. **Multi-valuta abilitata** — Vai a **Impostazioni > Impostazioni del negozio** e abilita il supporto per la multi-valuta
2. **Valute supportate configurate** — Aggiungi le valute che desideri offrire (es. NZD, SGD, EUR)
3. **Fornitore di tasso di cambio collegato** — Vai a **Impostazioni > Tassi di cambio** e configura un fornitore in modo che siano disponibili i tassi in tempo reale

## Impostazione di un prodotto carta regalo a multi-valuta

### Passo 1: Crea o modifica un prodotto carta regalo

1. Vai a **Prodotti > Tutti i prodotti**
2. Clicca su **+ Aggiungi prodotto** o apri un prodotto carta regalo esistente
3. Imposta **Tipo di prodotto** su **Carta regalo**

### Passo 2: Imposta la valuta della carta regalo

1. Clicca sulla scheda **Carta regalo**
2. Configura le impostazioni del valore come di consueto (importi fissi, importi personalizzati o entrambi)
3. In fondo alla scheda Carta regalo, trova il menu a discesa **Valuta Carta Regalo**
4. Seleziona la valuta target (es. **NZD - Dollaro Nuova Zelanda**)
5. Salva il prodotto

Il menu a discesa mostra tutte le valute abilitate nelle impostazioni del tuo negozio. Selezionare **Valuta base del negozio (predefinita)** significa che le carte regalo saranno emesse nella tua valuta base — questo è il comportamento standard.

### Passo 3: Imposta il prezzo

Imposta il prezzo del prodotto nella tua valuta base come di consueto. Quando un cliente acquista questa carta regalo, il prezzo viene automaticamente convertito nella valuta target utilizzando il tasso di cambio corrente.

**Esempio:** La tua valuta base è USD. Crei un prodotto carta regalo con prezzo 50 USD e Valuta Carta Regalo impostata su NZD. Se il tasso di cambio è 1 USD = 1,57 NZD, la carta regalo risultante avrà un valore di NZ$78,50.

## Corrispondenza della valuta e riscatto

Le carte regalo a multi-valuta utilizzano il **riscatto nella stessa valuta** — la valuta attiva per lo shopping del cliente deve corrispondere alla valuta della carta regalo.

### Esperienza del cliente

- Un cliente che acquista in **NZD** può applicare una carta regalo in NZD al checkout
- Un cliente che acquista in **USD** non può applicare una carta regalo in NZD — vedrà un messaggio che spiega la discrepanza di valuta
- I clienti possono cambiare la valuta per lo shopping utilizzando il selettore di valuta sul vostro sito web prima di applicare la carta regalo

### Come funziona il saldo

Il saldo della carta regalo viene sempre tracciato nella sua valuta nativa:

- Una carta regalo di NZ$78,50 inizia con un saldo di NZ$78,50
- Se un cliente effettua un acquisto di NZ$30, il saldo rimanente è NZ$48,50
- Il saldo non fluttua con i tassi di cambio — il valore nominale è fisso

Quando la carta regalo viene applicata al checkout, il sistema converte l'importo del vantaggio nella tua valuta base internamente per i calcoli dell'ordine, ma il saldo della carta regalo viene sempre detratto nella sua valuta nativa.

## Gestione delle carte regalo a multi-valuta

Vai a **Prodotti > Carte regalo** per visualizzare tutte le carte regalo emesse. Le carte regalo a multi-valuta vengono visualizzate con la loro valuta nativa:

- **Saldo** mostra la valuta della carta regalo (es. NZ$48,50)
- **Transazioni** registrano gli importi nella valuta della carta regalo
- **Valore iniziale** mostra l'importo convertito al momento dell'acquisto

### Verifica dei dettagli del tasso di cambio

Ogni transazione della carta regalo registra il tasso di cambio utilizzato al momento della transazione. Questo fornisce un registro completo per scopi contabili.

## Esempi

### Esempio 1: Carta regalo regionale per la Nuova Zelanda

**Scenario:** Operi dagli Stati Uniti ma hai clienti in Nuova Zelanda. Vuoi vendere carte regalo denominate in NZD.

| Impostazione | Valore |
|---------|-------|
| Nome prodotto | Carta regalo NZ |
| Tipo prodotto | Carta regalo |
| Prezzo | $50,00 (USD — la tua valuta base) |
| Tipo di denominazione | Denominazioni fisse |
| Denominazioni fisse | 25, 50, 100, 200 |
| Valuta Carta Regalo | NZD - Dollaro Nuova Zelanda |
| Scadenza | 365 giorni |

Quando un cliente seleziona la denominazione di $50:
- Il sistema converte $50 USD in NZD al tasso corrente
- Viene creata una carta regalo con l'equivalente in NZD (es. NZ$78,50)
- Il beneficiario può riscattarla mentre acquista in NZD

### Esempio 2: Carte regalo in diverse valute

**Scenario:** Vendiamo a clienti in Singapore, Australia e Regno Unito. Crea tre prodotti carta regalo:

1. **Carta regalo SG** — Valuta Carta Regalo: SGD
2. **Carta regalo AU** — Valuta Carta Regalo: AUD
3. **Carta regalo UK** — Valuta Carta Regalo: GBP

Ogni prodotto converte il prezzo base in valuta target al momento dell'acquisto. I clienti in ciascuna regione possono riscattare la carta regalo nella loro valuta locale.

### Esempio 3: Offerta mista di carte regalo

**Scenario:** Vuoi offrire sia carte regalo in valuta base che regionali.

- **Carta regalo del negozio** — Valuta Carta Regalo: *Valuta base del negozio (predefinita)* — riscattabile nella tua valuta base
- **Carta regalo NZ** — Valuta Carta Regalo: NZD — riscattabile solo in NZD

Entrambi i prodotti possono coesistere nel tuo catalogo. I clienti vedono in quale valuta è denominata una carta regalo quando controllano il saldo.

## Consigli

- Inizia con una singola valuta regionale e testa l'intero flusso (acquisto, consegna, riscatto) prima di aggiungere altre valute.
- Il tasso di cambio al momento dell'acquisto determina il valore della carta regalo. Se i tassi cambiano significativamente, il valore della carta regalo rimane fisso — questo protegge sia te che i tuoi clienti.
- Fai in modo che la valuta sia chiara nel nome del prodotto (es. "Carta regalo NZ" o "Carta regalo (NZD)") in modo che i clienti sappiano cosa stanno acquistando.
- Le carte regalo senza una valuta impostata continuano a funzionare esattamente come prima nella tua valuta base — i prodotti esistenti non sono influenzati.
- Monitora il fornitore di tasso di cambio per assicurarti che i tassi siano aggiornati. Tassi obsoleti potrebbero portare a carte regalo sovravalue o sottovalue.
- Considera attentamente le denominazioni. Una denominazione di $25 USD si converte in circa NZ$39 — denominazioni arrotondate nella valuta target potrebbero apparire meglio. Puoi creare prodotti separati con denominazioni che siano numeri arrotondati nella valuta target.