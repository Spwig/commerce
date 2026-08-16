---
title: Inventario & Magazzini
---

Il sistema dei magazzini ti permette di gestire l'inventario in più posizioni, impostare le priorità di evasione e tenere traccia dei livelli di scorta in tempo reale. Vai a **Prodotti > Magazzini** nel lato amministrativo per gestire le tue posizioni di magazzino.

![Elenchi di magazzino](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Magazzini

### Elenchi di magazzino

La pagina del magazzino mostra tutte le tue posizioni di inventario come schede con:

- **Nome e codice** — Identificatore del magazzino (es. "Magazzino principale", codice "MAIN-WH")
- **Area di vendita** — Assegnazione della regione geografica
- **Badge di stato** — Attivo/inattivo, posizione di vendita al dettaglio
- **Statistiche** — Prodotti in magazzino, priorità di evasione, percentuale di buffer di scorta
- **Posizione** — Città e paese
- **Ultimo aggiornamento** — Quando i livelli di scorta sono stati modificati l'ultima volta

### Creazione di un magazzino

1. Clicca **+ Aggiungi Magazzino**
2. Compila le **Informazioni base**:
   - **Nome** — Etichetta descrittiva (es. "Magazzino Est USA")
   - **Codice** — Identificatore unico breve (es. "US-EAST") — deve essere unico rispetto a tutti i magazzini
   - **Area di vendita** — Assegna a una regione geografica per il routing dell'evasione
   - **Attivo** — Abilita per includerlo nell'evasione
3. Compila la sezione **Indirizzo** con l'indirizzo completo del magazzino
4. Configura le **Impostazioni per l'evasione**:
   - **Priorità di evasione** — I numeri più alti = priorità maggiore per l'evasione degli ordini
   - **Percentuale del buffer di scorta** — Percentuale di scorta da riservare come buffer di sicurezza (0–100)
   - **Posizione di spedizione** — Opzionalmente collega a una posizione di ritiro se questo magazzino supporta il ritiro da parte del cliente
5. Configura la **Visualizzazione per il cliente** (opzionale):
   - **Nome visualizzato** — Etichetta visibile al cliente (es. "Spedisci dall'Australia"). Lascia vuoto per utilizzare il nome del magazzino.
   - **Mostra sulla homepage** — Visualizza l'origine di questo magazzino ai clienti sulle pagine dei prodotti
6. Configura **POS / Negozio al dettaglio** (opzionale):
   - **Posizione di vendita** — Seleziona se questo magazzino funge anche da negozio fisico con terminali POS
   - **Nome visualizzato in POS** — Nome breve visualizzato nell'interfaccia POS
   - **Gruppo di negozi** — Assegna a un gruppo di negozi POS per l'eredità delle impostazioni
7. Aggiungi le **Informazioni di contatto** se necessario (nome, email, telefono)
8. Clicca **Salva**

### Priorità di evasione

Quando arriva un ordine, il sistema seleziona il miglior magazzino in base a:

1. **Valore della priorità** — I magazzini con priorità più alta vengono preferiti
2. **Disponibilità dello stock** — Deve avere abbastanza scorte
3. **Corrispondenza della regione** — I magazzini nella regione del cliente vengono preferiti

Ad esempio, se hai un magazzino USA (priorità 100) e un magazzino UE (priorità 60), gli ordini USA saranno evasi dal magazzino USA per primi.

### Buffer di scorta

Il buffer di scorta riserva una percentuale dell'inventario che non verrà venduta online. Questo è utile per:

- Negozi al dettaglio fisici che hanno bisogno di scorte in esposizione
- Scorte di sicurezza per evitare di vendere troppo
- Inventario riservato per ordini all'ingrosso

Un buffer del 10% su 100 unità significa che solo 90 unità sono disponibili per gli ordini online.

## Oggetti di scorta

Gli oggetti di scorta rappresentano l'inventario effettivo di un prodotto specifico in un magazzino specifico.

### Visualizzazione dei livelli di scorta

1. Clicca sull'**icona della scorta** su qualsiasi scheda del magazzino per vedere i suoi oggetti di scorta
2. Oppure vai alla scheda **Inventario** di un prodotto per vedere lo stock in tutti i magazzini

Ogni oggetto di scorta mostra:

- **Nome del prodotto** e variante (se applicabile)
- **A disposizione** — Inventario fisico totale
- **Assegnato** — Quantità riservata per gli ordini in sospeso
- **Disponibile** — A disposizione meno assegnato (ciò che può essere venduto)

### Aggiunta di scorte

1. Vai a **Prodotti > Oggetti di scorta** e clicca **+ Aggiungi Oggetto di scorta**, oppure
2. Apri la finestra di modifica di un prodotto e usa la sezione **Oggetti di scorta** in fondo
3. Seleziona il **prodotto** e il **magazzino** (e opzionalmente una **variante** per i prodotti variabili)
4. Inserisci la quantità **a disposizione**
5. Imposta la ** soglia di scorta bassa** — questo valore per oggetto attiva un avviso di scorta bassa
6. Salva

### Movimenti di scorta

Ogni modifica all'inventario viene registrata come **movimento di scorta**:

| Tipo di movimento | Descrizione |
|--------------|-------------|
| **Carico** | Nuovo stock ricevuto dal fornitore |
| **Vendita** | Stock sottratto per un ordine completato |
| **Ritorno** | Stock reso da un cliente |
| **Aggiustamento** | correzione manuale (differenza nel conteggio) |
| **Trasferimento** | Spostato tra magazzini |
| **Riserva** | Tenuto temporaneamente per un carrello attivo |
| **Danni** | Scartato come danneggiato o perso |
| **Conteggio** | Corretto per corrispondere a un conteggio fisico |

I movimenti di magazzino forniscono una tracciabilità completa dei cambiamenti dell'inventario. Oltre all'azione **Aggiorna i livelli di magazzino**, Spwig offre inoltre azioni in bulk sulla lista degli articoli di magazzino per trasferire, scartare e contare nuovamente lo stock su molti articoli contemporaneamente — vedi [Azioni di stock in bulk](/help/stock-bulk-actions).

## Tracciamento dell'inventario sui prodotti

### Abilitare il tracciamento dell'inventario

Nella sezione **Inventario** di un prodotto:

1. Attiva **Traccia l'inventario** per abilitare la gestione dello stock per questo prodotto
2. Imposta la ** soglia di stock basso ** — attiva gli avvisi del pannello quando lo stock in qualsiasi magazzino scende al di sotto di questo livello
3. Configura **Consenti ordinazioni in ritardo** se si desidera accettare gli ordini quando non è disponibile lo stock
4. Imposta in modo opzionale un'**azione per esaurito** per sovrascrivere il comportamento del sito o della categoria per questo prodotto specifico

Dopo aver abilitato il tracciamento, gestisci le quantità effettive dello stock utilizzando la sezione **Articoli di magazzino** incorporata nella parte inferiore del modulo del prodotto, oppure tramite **Prodotti > Articoli di magazzino**.

### Stock su più magazzini

Quando il tracciamento dell'inventario è abilitato, la scheda Inventario mostra i livelli dello stock in un tavolo riassuntivo:

- Totale disponibile in tutte le località
- Panoramica per magazzino
- Quantità disponibili dopo le riserve e gli assegni

## Avvisi di stock basso

Il sistema monitora automaticamente i livelli dello stock e ti avvisa quando:
- Un prodotto scende sotto la **soglia di stock basso**
- Un prodotto raggiunge **zero stock disponibile**

Gli avvisi di stock basso appaiono su:
- Il **pulsante del negozio** nella sezione Azioni richieste
- La lista dei prodotti con un indicatore visivo

## Suggerimenti

- Inizia con un unico magazzino e aggiungine di più mentre la tua azienda cresce.
- Imposta le priorità di evasione in base alla velocità e al costo della spedizione per ogni area.
- Usa buffer di stock per i punti vendita al dettaglio per garantire la disponibilità dello stock in negozio.
- Controlla regolarmente i movimenti dello stock per identificare scompensi o discrepanze.
- Imposta le soglie di stock basso in base al tuo tempo di rifornimento — se ci vogliono 2 settimane per rifornire, imposta la soglia per coprire 2 settimane di vendite.
- Abilita il tracciamento dell'inventario prima del lancio per evitare di vendere troppo.