---
title: Gestione degli ordini
---

This guide covers everything you need to manage customer orders — from reviewing new orders to processing shipments and handling refunds.

## Elenco degli ordini

Naviga a **Ordini > Tutti gli ordini** nel menu laterale per visualizzare tutti gli ordini. L'elenco mostra il numero, lo stato, il cliente, il totale e la data di ogni ordine.

![Elenco degli ordini](/static/core/admin/img/help/manage-orders/order-list.webp)

Utilizza i filtri in alto per restringere gli ordini per stato, intervallo di date o cerca per numero dell'ordine o nome del cliente.

## Dettagli dell'ordine

Clicca su un ordine per aprire la sua pagina dei dettagli. Qui troverai tutte le informazioni sull'ordine organizzate in sezioni chiare.

![Dettagli dell'ordine](/static/core/admin/img/help/manage-orders/order-detail.webp)

### Informazioni sull'ordine

La sezione in alto mostra:

- **Numero dell'ordine** — L'identificatore unico per questo ordine
- **Stato** — Stato corrente dell'ordine (In attesa, In elaborazione, Spedito, Consegnato, Completato, Annullato)
- **Cliente** — Nome e indirizzo email del cliente che ha effettuato l'ordine
- **Creato** — Quando l'ordine è stato effettuato

### Elementi dell'ordine

La sezione degli elementi elenca tutto ciò che il cliente ha ordinato:

- Nome del prodotto e SKU
- Quantità ordinata
- Prezzo unitario e totale riga
- Sconti applicati

### Dettagli del pagamento

Mostra il metodo di pagamento utilizzato, l'ID transazione e lo stato del pagamento. Per gli ordini in attesa di pagamento, puoi monitorare lo stato della passerella di pagamento qui.

### Indirizzo di spedizione

L'indirizzo di consegna del cliente. Se l'indirizzo di fatturazione è diverso, entrambi vengono visualizzati.

## Ciclo di vita degli ordini

Gli ordini passano tipicamente attraverso questi stati:

1. **In attesa** — Nuovo ordine ricevuto, in attesa di conferma del pagamento
2. **In elaborazione** — Pagamento confermato, preparazione per la spedizione
3. **Spedito** — Ordine spedito con informazioni di tracciamento
4. **Consegnato** — Cliente ha ricevuto l'ordine
5. **Completato** — Ordine finalizzato

## Elaborazione di un ordine

### 1. Rivedi l'ordine

Controlla che:

- Gli elementi e le quantità siano corretti
- L'indirizzo di spedizione sia completo
- Il pagamento sia stato ricevuto
- Siano state gestite eventuali note del cliente

### 2. Crea una spedizione

Per spedire l'ordine:

1. Clicca su **Crea spedizione** sulla pagina dei dettagli dell'ordine
2. Seleziona gli elementi da includere (per spedizioni parziali, seleziona solo alcuni elementi)
3. Scegli il corriere e il servizio di spedizione
4. Inserisci il numero di tracciamento
5. Clicca su **Salva spedizione**

Lo stato dell'ordine viene aggiornato automaticamente a **Spedito** e il cliente riceve un'e-mail di notifica con le informazioni di tracciamento.

### 3. Marca come consegnato

Una volta che il cliente conferma la consegna o il tracciamento mostra che è stata consegnata, aggiorna lo stato a **Consegnato** e successivamente a **Completato**.

## Azioni sugli ordini

### Aggiunta di note

Aggiungi note interne o messaggi visibili al cliente:

1. Scorri fino alla sezione **Note** sulla pagina dei dettagli dell'ordine
2. Digita il tuo messaggio
3. Scegli se è una nota interna (visibile solo allo staff) o una notifica al cliente
4. Clicca su **Aggiungi nota**

Le note visibili al cliente attivano una notifica via e-mail.

### Elaborazione del rimborso

Per emettere un rimborso:

1. Clicca su **Rimborso** sulla pagina dei dettagli dell'ordine
2. Seleziona gli elementi da rimborsare (o inserisci un importo personalizzato)
3. Scegli il motivo del rimborso
4. Conferma il rimborso

I rimborsi vengono elaborati tramite la passerella di pagamento originale. Il cliente riceve una conferma via e-mail.

### Annullamento di un ordine

Per annullare:

1. Clicca su **Annulla ordine**
2. Seleziona il motivo dell'annullamento
3. Scegli se rimettere in magazzino gli articoli
4. Conferma

Il cliente viene notificato automaticamente e viene iniziato un rimborso se il pagamento è già stato ricevuto.

## Azioni di gruppo

Dall'elenco degli ordini puoi selezionare più ordini e applicare azioni di gruppo:

- **Aggiorna stato** — Sposta diversi ordini nello stesso stato
- **Esporta** — Scarica gli ordini selezionati come CSV
- **Stampa** — Genera etichette di imballaggio o fatture

## Notifiche sugli ordini

I clienti ricevono automaticamente e-mail a momenti chiave:

- **Conferma ordine** — Subito dopo l'effettuazione dell'ordine
- **Pagamento ricevuto** — Quando il pagamento è confermato
- **Notifica di spedizione** — Quando viene creata una spedizione (include il link di tracciamento)
- **Conferma di consegna** — Quando viene segnato come consegnato

Configura i modelli di e-mail in **Impostazioni > Configurazione email**.

## Consigli

- Elabora gli ordini quotidianamente per mantenere i tempi di spedizione veloci.
- Utilizza i filtri per lo stato per concentrarti sugli ordini che necessitano di attenzione (In attesa e In elaborazione).
- Aggiungi note interne per tracciare eventuali requisiti di gestione speciale.
- Per periodi ad alto volume, utilizza le azioni di gruppo per aggiornare più ordini contemporaneamente.
- Configura regole per la spedizione per automatizzare la selezione del corriere in base al peso dell'ordine e alla destinazione.