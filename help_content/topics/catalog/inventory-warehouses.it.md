---
title: Inventario e Magazzini
---

Il sistema dei magazzini consente di gestire l'inventario in diverse ubicazioni, impostare le priorità di soddisfazione degli ordini e monitorare i livelli di stock in tempo reale. Naviga verso **Impostazioni > Gestione Licenze** nel menu laterale, o accedi ai magazzini dalla scheda **Inventario del prodotto**.

![Elenco dei magazzini](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Magazzini

### Elenco dei magazzini

La pagina dei magazzini mostra tutte le ubicazioni dell'inventario come schede con:

- **Nome e codice** — Identificatore del magazzino (es. "Main Warehouse", codice "MAIN-WH")
- **Regione di vendita** — Assegnazione a una regione geografica
- **Sfogliatori di stato** — Attivo/Non attivo, ubicazione retail
- **Statistiche** — Prodotti in stock, priorità di soddisfazione, percentuale di buffer di stock
- **Ubicazione** — Città e paese
- **Ultimo aggiornamento** — Quando i livelli di stock sono stati ultimamente modificati

### Creare un magazzino

1. Fare clic su **+ Aggiungi magazzino**
2. Inserisci i dettagli del magazzino:
   - **Nome** — Etichetta descrittiva (es. "US East Warehouse")
   - **Codice** — Identificatore univoco breve (es. "US-EAST")
   - **Regione di vendita** — Assegna a una regione geografica per il routing della soddisfazione degli ordini
   - **Indirizzo** — Indirizzo completo del magazzino per i calcoli di spedizione
3. Configura le impostazioni:
   - **Attivo** — Abilita per includerlo nella soddisfazione degli ordini
   - **Ubicazione retail** — Contrassegna se questo magazzino funziona anche come negozio fisico
   - **Priorità di soddisfazione** — Numeri più alti = priorità più alta per la soddisfazione degli ordini
   - **Buffer di stock** — Percentuale di stock da riservare come buffer di sicurezza
4. Fare clic su **Salva**

### Priorità di soddisfazione

Quando un ordine arriva, il sistema seleziona il miglior magazzino in base a:

1. **Valore di priorità** — I magazzini con priorità più alta sono preferiti
2. **Disponibilità di stock** — Deve avere stock sufficiente
3. **Corrispondenza regionale** — I magazzini nella regione del cliente sono preferiti

Per esempio, se hai un magazzino USA (priorità 100) e un magazzino UE (priorità 60), gli ordini USA verranno soddisfatti prima dal magazzino USA.

### Buffer di stock

Il buffer di stock riserva una percentuale dell'inventario che non verrà venduta online. Questo è utile per:
- Negozio fisico che necessita di stock disponibile in sede
- Stock di sicurezza per prevenire la vendita di prodotti esauriti
- Inventario riservato per ordini al dettaglio

Un buffer del 10% su 100 unità significa che solo 90 unità sono disponibili per gli ordini online.

## Elementi di stock

Gli elementi di stock rappresentano l'inventario effettivo di un prodotto specifico in un magazzino specifico.

### Visualizzare i livelli di stock

1. Fare clic sull'icona **stock** su qualsiasi scheda del magazzino per visualizzare gli elementi di stock
2. Oppure naviga verso la scheda **Inventario** di un prodotto per visualizzare lo stock in tutti i magazzini

Ogni elemento di stock mostra:
- **Nome del prodotto** e variante (se applicabile)
- **Disponibile** — Totale dell'inventario fisico
- **Allocato** — Quantità riservata per ordini pendenti
- **Disponibile** — Disponibile meno allocato (quello che può essere venduto)

### Aggiungere stock

1. Dalla vista dello stock del magazzino, fare clic su **Aggiungi elemento di stock**
2. Seleziona il prodotto e la variante
3. Inserisci la quantità **disponibile**
4. Salva

### Movimenti di stock

Ogni modifica all'inventario viene registrata come **movimento di stock**:

| Tipo di movimento | Descrizione |
|------------------|-------------|
| **Ricevimento** | Nuovo stock ricevuto dal fornitore |
| **Vendita** | Stock detratto per un ordine soddisfatto |
| **Rimborso** | Stock restituito da un cliente |
| **Correzione** | Correzione manuale (discrepanza di conteggio) |
| **Trasferimento** | Trasferito tra magazzini |
| **Riserva** | Temporaneamente bloccato per un carrello attivo |

I movimenti di stock forniscono un registro completo delle modifiche all'inventario.

## Tracciamento dell'inventario sui prodotti

### Abilitare il tracciamento dell'inventario

Nella scheda **Inventario** di un prodotto:

1. Attiva **Tracciamento dell'inventario** per abilitare la gestione dello stock
2. Imposta la **Soglia di stock basso** — attiva alert quando lo stock scende al di sotto di questo livello
3. Configura **Consenti ordini in attesa** se si desidera accettare ordini quando lo stock è esaurito

### Stock multi-magazzino

Quando il tracciamento dell'inventario è abilitato, la scheda Inventario mostra i livelli di stock in tutte le ubicazioni in una tabella di riepilogo:

- Totale disponibile in tutte le ubicazioni
- Scomposizione per magazzino
- Quantità disponibili dopo riserve e allocazioni

## Alert di stock basso

Il sistema monitora automaticamente i livelli di stock e ti avvisa quando:
- Un prodotto scende al di sotto della sua **soglia di stock basso**
- Un prodotto raggiunge **zero stock disponibile**

Gli alert di stock basso appaiono in:
- Il **Pannello di controllo del negozio** nella sezione Richieste
- L'elenco dei prodotti con un indicatore visivo

## Consigli

- Iniziare con un singolo magazzino e aggiungere di più man mano che l'azienda cresce.
- Impostare le priorità di soddisfazione degli ordini in base alla velocità e al costo di spedizione per ogni regione.
- Utilizzare i buffer di stock per le ubicazioni retail per garantire la disponibilità di stock in sede.
- Controllare regolarmente i movimenti di stock per identificare eventuali perdite o discrepanze.
- Impostare le soglie di stock basso in base al tempo di riordino — se ci vogliono 2 settimane per rifornire, impostare la soglia per coprire 2 settimane di vendite.
- Abilitare il tracciamento dell'inventario prima di andare online per evitare la vendita di prodotti esauriti.
