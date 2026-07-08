---
title: Regioni di vendita
---

Le regioni di vendita ti permettono di definire mercati geografici per il tuo negozio e di controllare quali prodotti sono disponibili in ciascuna regione. Questo è utile quando vendi in diversi paesi o territori e hai bisogno di cataloghi di prodotti diversi, valute regionali o disponibilità di stock per ubicazione.

## Cosa è una regione di vendita?

Una regione di vendita è un'area geografica con un nome, composta da uno o più paesi. Ogni regione ha una valuta predefinita, una priorità e può essere collegata a uno o più magazzini. Quando un cliente naviga nel tuo negozio, Spwig determina la sua regione in base alla sua posizione e applica le regole appropriate per la valuta e la visibilità dei prodotti.

Casi d'uso comuni:
- Mostrare solo prodotti disponibili localmente ai clienti di ciascun paese
- Assegnare valute predefinite specifiche per regione (es. NZD per i clienti della Nuova Zelanda)
- Controllare quali magazzini gestiscono gli ordini per ciascuna regione
- Nascondere prodotti non ancora disponibili in determinati mercati

## Creare una regione di vendita

1. Vai a **Catalogo > Regioni di vendita**
2. Clicca su **+ Aggiungi regione di vendita**
3. Compila i dettagli della regione:

| Campo | Descrizione | Esempio |
|-------|-------------|---------|
| **Nome della regione** | Nome visualizzato per questa regione | `Asia-Pacifico` |
| **Codice della regione** | Identificatore univoco breve | `APAC` |
| **Paesi** | Codici ISO dei paesi inclusi in questa regione | `["NZ", "AU", "SG", "FJ"]` |
| **Valuta predefinita** | Codice ISO della valuta per questa regione | `NZD` |
| **Priorità** | Le regioni con priorità più alta vengono abbinare per prime | `10` |
| **Attiva** | Se questa regione è attualmente in uso | Selezionata |

4. Clicca su **Salva**

### Codici dei paesi

Inserisci i paesi come elenco JSON di codici ISO a due lettere. Per esempio:
- Nuova Zelanda e Australia: `["NZ", "AU"]`
- Solo Singapore: `["SG"]`
- Tutta Europa: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Priorità

Se il paese del cliente corrisponde a più di una regione, viene utilizzata la regione con il numero di priorità più alto. Imposta una priorità più alta per le regioni più specifiche (es. assegna a `NZ` una priorità di 20 e a `APAC` una priorità di 10 in modo che i clienti della Nuova Zelanda vengano abbinati alla regione NZ prima).

## Controllare la visibilità dei prodotti per regione

Di default, ogni prodotto è visibile in tutte le regioni. Per limitare un prodotto a regioni specifiche, utilizza i record **Visibilità per regione dei prodotti**.

### Limitare un prodotto a regioni specifiche

1. Vai a **Catalogo > Visibilità per regione dei prodotti**
2. Clicca su **+ Aggiungi visibilità per regione dei prodotti**
3. Seleziona il **Prodotto**
4. Seleziona la **Regione**
5. Imposta **Visibile** su attivo o disattivo come necessario
6. Clicca su **Salva**

Una volta che esiste qualsiasi record di visibilità per un prodotto, Spwig applica le regole. I prodotti senza record di visibilità rimangono visibili ovunque.

### Pattern comuni

**Limitare a una sola regione**

Aggiungi un record di visibilità per ciascuna regione che desideri supportare, impostando **Visibile** su `Sì` per le regioni consentite. I clienti di altre regioni non vedranno il prodotto.

**Escludere da una regione**

Aggiungi un singolo record di visibilità per la regione che desideri escludere e imposta **Visibile** su `No`. Il prodotto rimarrà visibile in tutte le altre regioni.

### Modificare la visibilità dalle pagine del prodotto

Puoi anche gestire la visibilità per regione direttamente dal modulo di modifica del prodotto. Nella sezione **Visibilità per regione** del prodotto, troverai una tabella inline che mostra tutte le regioni e le impostazioni di visibilità per quel prodotto.

## Valuta regionale

Ogni regione ha una valuta predefinita. I clienti che navigano da quella regione vedranno i prezzi visualizzati nella valuta della regione. La valuta utilizzata viene determinata al momento del checkout.

Per configurare i prezzi in diverse valute, configura i tassi di cambio sotto **Impostazioni > Tassi di cambio**. I prezzi possono essere convertiti automaticamente o impostati manualmente per ciascuna valuta.

## Collegare i magazzini alle regioni

I magazzini vengono collegati alle regioni quando crei o modifichi un magazzino sotto **Catalogo > Magazzini**. Ogni magazzino appartiene a una regione, che controlla quale stock della regione viene utilizzato per soddisfare gli ordini.

Per ulteriori dettagli sui magazzini, consulta l'argomento **Inventory e Warehouses** della sezione Aiuto.

## Tips

- Mantieni i codici delle regioni brevi e descrittivi (`NZ`, `APAC`, `EU`, `US`) — vengono utilizzati internamente e nei log.
- Utilizza numeri di priorità più elevati per regioni più piccole e specifiche in modo che prevalgano sulle regioni più ampie e generiche.
- Se vendi solo in un paese, non è necessario configurare le regioni affatto — Spwig funziona correttamente con un unico catalogo globale.
- Testa la visibilità basata sulla regione anteprimando il tuo negozio mentre filtri per una regione specifica nell'amministrazione.
- I record di visibilità dei prodotti devono essere creati solo quando desideri limitare i prodotti. Lasciare un prodotto senza record di visibilità lo rende disponibile universalmente.
- Rivedi le tue regole di visibilità ogni volta che aggiungi una nuova regione per assicurarti che le limitazioni esistenti sui prodotti siano corrette.