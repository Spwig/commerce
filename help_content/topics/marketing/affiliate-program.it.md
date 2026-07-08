---
title: Programma di Affiliazione
---

Il programma di affiliazione ti permette di reclutare partner che promuovono i tuoi prodotti e guadagnano commissioni sulle vendite che generano. Gli affiliati condividono link di riferimento unici e Spwig traccia automaticamente i clic, attribuisce gli ordini e calcola le commissioni.

![Programmi di affiliazione](/static/core/admin/img/help/affiliate-program/program-list.webp)

## Come Funziona

1. Crei uno o più **programmi di affiliazione** con tassi di commissione e regole
2. Gli affiliati **si iscrivono** tramite un portale pubblico o vengono aggiunti manualmente
3. Ogni affiliato riceve un **link di riferimento unico** con un codice di tracciamento
4. Quando un cliente clicca sul link e effettua un acquisto, una **commissione** viene registrata
5. Verifichi e approvi le commissioni, quindi procedi al **pagamento**

## Creare un Programma

Naviga verso **Marketing > Programmi di Affiliazione** e clicca su **Aggiungi Programma**.

### Impostazioni del Programma

| Impostazione | Descrizione |
|---------|-------------|
| **Nome** | Nome del programma visibile agli affiliati (es. "Programma Partner") |
| **Tipo di Commissione** | **Percentuale** del totale dell'ordine o **Fissa** per vendita |
| **Tasso di Commissione** | La percentuale o l'importo fisso che gli affiliati guadagnano |
| **Durata della Cookie** | Quanti giorni dura il cookie di tracciamento del riferimento (predefinito: 30 giorni) |
| **Pagamento Minimo** | Guadagno minimo prima che un affiliato possa richiedere un pagamento |
| **Approva Automaticamente gli Affiliati** | Accetta automaticamente le nuove richieste di iscrizione degli affiliati o richiedi un'approvazione manuale |
| **Stato** | Attivo, sospeso o chiuso |

### Tipi di Commissione

- **Percentuale** — Gli affiliati guadagnano una percentuale del sottototale di ogni ordine riferito (es. 10% di un ordine da 100 dollari = 10 dollari di commissione)
- **Fissa** — Gli affiliati guadagnano un importo fisso per vendita, indipendentemente dal valore dell'ordine (es. 5 dollari per vendita)

## Gestione degli Affiliati

Naviga verso **Marketing > Affiliati** per visualizzare e gestire gli account degli affiliati.

### Dettagli dell'Affiliato

Ogni affiliato ha:
- **Codice Affiliato** — Un codice unico utilizzato nei link di riferimento (generato automaticamente o personalizzato)
- **Link di Riferimento** — L'URL completo di tracciamento che l'affiliato condivide (es. `yourstore.com/?ref=CODE`)
- **Stato** — In attesa, approvato o rifiutato
- **Metodo di Pagamento** — Come l'affiliato riceve i pagamenti (PayPal o trasferimento bancario)
- **Appartenenza al Programma** — A quali programmi appartiene l'affiliato

### Aggiungere Affiliati Manualmente

1. Clicca su **Aggiungi Affiliato**
2. Seleziona un account cliente esistente o crea uno nuovo
3. Assegna l'affiliato a uno o più programmi
4. Imposta il codice affiliato (o lascia vuoto per generare automaticamente)

### Portale degli Affiliati

Gli affiliati accedono a un portale pubblico dove possono:
- Visualizzare il proprio dashboard con guadagni e statistiche dei clic
- Copiare i propri link di riferimento
- Tracciare la storia delle commissioni
- Richiedere pagamenti

L'URL del portale è automaticamente disponibile a `/affiliate/` nel tuo negozio.

## Tracciamento e Commissioni

### Come Funziona il Tracciamento

1. Un cliente clicca su un link di riferimento di un affiliato
2. Viene impostato un cookie di tracciamento nel browser del cliente (che dura per la durata della cookie configurata)
3. Se il cliente effettua un ordine entro la durata del cookie, l'ordine viene attribuito all'affiliato
4. Viene creata una registrazione della commissione con lo stato **In Attesa**

### Stati delle Commissioni

| Stato | Descrizione |
|--------|-------------|
| **In Attesa** | Commissione registrata, in attesa di revisione |
| **Approvata** | Verificata e pronta per il pagamento |
| **Rifiutata** | Commissione negata (es. ordine fraudolento o articolo restituito) |
| **Pagata** | Commissione inclusa in un pagamento completato |

### Revisione delle Commissioni

Naviga verso **Marketing > Commissioni** per revisionare le commissioni in attesa:

1. Controlla i dettagli dell'ordine per verificare che la vendita sia legittima
2. Clicca su **Approva** per confermare, o **Rifiuta** con una ragione
3. Le commissioni approvate si accumulano verso il saldo del pagamento dell'affiliato

## Pagamenti

Quando il saldo delle commissioni approvato di un affiliato raggiunge il limite minimo di pagamento, puoi processare un pagamento.

### Elaborazione dei Pagamenti

1. Naviga verso **Marketing > Pagamenti**
2. Seleziona gli affiliati con saldi disponibili
3. Scegli il metodo di pagamento:
   - **PayPal** — Invia i fondi direttamente all'e-mail PayPal dell'affiliato
   - **Trasferimento Bancario** — Registra un trasferimento bancario manuale
4. Conferma e elabora il pagamento
5. Lo stato del pagamento viene aggiornato a **Completato** e le commissioni vengono contrassegnate come **Pagate**

### Fornitori di Pagamento

Spwig si integra con fornitori di pagamento per effettuare pagamenti automatici:
- **PayPal** — Pagamenti di massa automatici tramite l'API di PayPal
- **Airwallex** — Pagamenti internazionali con tassi di cambio competitivi
- **Manuale** — Registra i pagamenti elaborati al di fuori di Spwig

## Link di Riferimento

Ogni link di riferimento di un affiliato segue questo modello:

```
https://yourstore.com/?ref=AFFILIATE_CODE
```

Gli affiliati possono anche creare link a prodotti o categorie specifiche:

```
https://yourstore.com/products/shoe-name/?ref=AFFILIATE_CODE
```

Il parametro `ref` funziona su qualsiasi pagina — il cookie di tracciamento viene impostato indipendentemente dalla pagina di destinazione.

## Analisi del Programma

Il dashboard del programma di affiliazione mostra:
- **Totale Clic** — Quante volte i link di riferimento sono stati cliccati
- **Totale Ordini** — Ordini attribuiti agli affiliati
- **Totale Commissioni** — Somma di tutte le commissioni (in attesa, approvate e pagate)
- **Affiliati Attivi** — Numero di affiliati approvati che attualmente generano riferimenti

## Consigli

- Inizia con una **commissione basata su percentuale** (5–15%) — si adatta naturalmente al valore dell'ordine e è facile da comprendere per gli affiliati.
- Imposta una **durata della cookie di 30 giorni** come base — questo dà ai clienti tempo per tornare e completare l'acquisto, mantenendo comunque l'attribuzione della vendita all'affiliato.
- Abilita **approvazione automatica** per i programmi pubblici per ridurre l'attrito, o usa l'approvazione manuale per i programmi su invito dove desideri verificare ogni affiliato.
- Imposta un **pagamento minimo** ragionevole (es. 25–50 dollari) per evitare di elaborare molte transazioni piccole.
- Personalizza il **portale degli affiliati** per adattarlo al tuo brand — gli affiliati sono più propensi a promuovere il tuo negozio quando l'esperienza sembra professionale.
- Monitora regolarmente le commissioni per **pattern fraudolenti** come riferimenti a se stessi, tassi di resi insolitamente elevati o volumi di clic sospetti.