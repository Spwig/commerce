---
title: Prodotti prenotabili
---

I prodotti prenotabili permettono ai clienti di riservare una data e un orario specifici al momento dell'acquisto. Questo supporta appuntamenti, noleggi, corsi, eventi e prenotazioni di alloggi — tutti gestiti direttamente dal tuo pannello di amministrazione Spwig.

## Tipi di prenotazione

| Tipo | Migliore per |
|------|----------|
| **Appuntamento** | Servizi: consulenze, tagli di capelli, allenamento personalizzato |
| **Noleggio** | Noleggio di attrezzature, veicoli, stanze |
| **Corso / Laboratorio** | Sessioni di gruppo con una capacità definita |
| **Alloggio** | Soggiorni multi-giornalieri con orari di check-in/check-out |
| **Evento** | Eventi con biglietti, unici o ricorrenti |

## Configurazione di un prodotto prenotabile

### Passaggio 1: Crea il prodotto

1. Vai a **Prodotti > Tutti i prodotti** e fai clic su **+ Aggiungi prodotto**
2. Imposta **Tipo di prodotto** su **Prodotto di prenotazione**
3. Compila i campi standard del prodotto (nome, descrizione, prezzo)
4. Salva il prodotto

### Passaggio 2: Configura le impostazioni di prenotazione

Dopo aver salvato, una sezione **Configurazione della prenotazione** appare nel modulo di modifica del prodotto. Compila le impostazioni di prenotazione:

#### Tipo e durata della prenotazione

- **Tipo di prenotazione** — Seleziona il tipo che meglio si adatta al tuo servizio (Appuntamento, Noleggio, Corso, ecc.)
- **Tipo di durata** — Scegli **Durata fissa** per sessioni con durata definita, o **Cliente seleziona la durata** per permettere ai clienti di scegliere quanto tempo necessitano
- **Durata** e **Unità di durata** — Imposta la lunghezza (es. `60` minuti, `1` ora, `2` giorni)
- **Durata minima/massima** — Se i clienti possono selezionare la durata, imposta l'intervallo consentito

#### Tempo di buffer

Il tempo di buffer viene aggiunto automaticamente tra le prenotazioni per permettere la preparazione o la pulizia:
- **Buffer prima** — Minuti riservati prima che inizi la prenotazione
- **Buffer dopo** — Minuti riservati dopo che termina la prenotazione

Per esempio, un appuntamento per un massaggio di 60 minuti con un buffer di 15 minuti dopo dà 15 minuti per prepararsi per il prossimo cliente.

#### Finestra di prenotazione anticipata

- **Avviso minimo di prenotazione** — Quanto in anticipo un cliente deve prenotare (es. `24 ore` in modo che non siano consentite prenotazioni dello stesso giorno)
- **Finestra massima di prenotazione** — Quanto in anticipo i clienti possono prenotare (es. `365 giorni`)

#### Capacità

- **Massimo di prenotazioni per slot** — Per corsi ed eventi, imposta quanti clienti possono prenotare lo stesso slot di tempo. Imposta su `1` per appuntamenti privati.

#### Conferma

- **Richiedi conferma manuale** — Quando selezionato, le prenotazioni non vengono confermate automaticamente. Devi approvare manualmente ogni prenotazione dall'elenco delle prenotazioni. Utile quando desideri verificare i clienti prima di confermare.

#### Politica di cancellazione

- **Cancellazione consentita** — Se i clienti possono cancellare la loro prenotazione
- **Termine di cancellazione** — Quante ore/giorni prima della prenotazione i clienti possono cancellare (es. `24 ore`)

#### Visualizzazione del calendario

Come i clienti selezionano la data e l'orario sulla pagina del prodotto:

| Modalità di visualizzazione | Migliore per |
|-------------|----------|
| **Visualizzazione del calendario** | Utilizzo generale — calendario completo del mese |
| **Selettore di data** | Selezione semplice di una singola data |
| **Elenco delle date disponibili** | Prodotti con slot di disponibilità limitati |
| **Selettore di intervallo di date** | Alloggi e noleggi multi-giornalieri |

#### Acconti

Per richiedere un acconto al momento del checkout invece di un pagamento completo:
1. Seleziona **Abilita acconto**
2. Imposta **Tipo di acconto** su **Importo fisso** o **Percentuale del totale**
3. Inserisci l'**Importo dell'acconto** (es. `50` per $50, o `25` per il 25%)

#### Impostazioni specifiche per alloggi

Per le prenotazioni di alloggi, vengono visualizzati ulteriori campi:
- **Orario di check-in** e **Orario di check-out** — Orari standard per la proprietà
- **Occupazione standard** — Numero predefinito di ospiti incluso nel prezzo base

### Passaggio 3: Aggiungi risorse di prenotazione (opzionale)

Le risorse sono gli oggetti fisici o i membri dello staff che vengono assegnati a una prenotazione — ad esempio, "Stanze 1", "Campo A" o "Istruttore Sam".

1. Nel modulo di modifica del prodotto, vai alla sezione **Risorse di prenotazione**
2. Fai clic su **Aggiungi risorsa**
3. Dà alla risorsa un **Nome** e imposta la sua **Capacità** (quanti booking può gestire contemporaneamente)
4. Opzionalmente aggiungi immagini della risorsa

Le risorse ti permettono di tracciare la disponibilità per singoli asset o membri dello staff, non solo per slot orari.

### Passaggio 4: Impostare le regole di disponibilità

Le regole di disponibilità definiscono quando è possibile effettuare prenotazioni:

1. Nella sezione **Disponibilità** del prodotto, fai clic su **Aggiungi regola di disponibilità**
2. Seleziona la **Risorsa** a cui si applica questa regola
3. Imposta i **Giorni della settimana** in cui le prenotazioni sono disponibili
4. Imposta l'**Ora di inizio** e l'**Ora di fine** per la finestra disponibile
5. Opzionalmente, imposta un intervallo di date (**Valido da** / **Valido fino a**) per la disponibilità stagionale
6. Salva

## Visualizzazione e gestione delle prenotazioni

### Elenco delle prenotazioni

Vai a **Catalogo > Prenotazioni** per visualizzare tutte le prenotazioni. Puoi filtrare per:
- Stato (In attesa di conferma, Confermato, Annullato, Completato, Non presente)
- Prodotto
- Intervallo di date

### Stati delle prenotazioni

| Stato | Significato |
|--------|---------|
| **In attesa di conferma** | In attesa di approvazione manuale (se richiesta la conferma) |
| **Confermato** | La prenotazione è confermata e attiva |
| **Annullato** | La prenotazione è stata annullata dal cliente o da te |
| **Completato** | La data della prenotazione è passata e è stata eseguita |
| **Non presente** | Il cliente non si è presentato |

### Confermare una prenotazione in attesa

1. Apri la prenotazione da **Catalogo > Prenotazioni**
2. Cambia lo **Stato** in **Confermato**
3. Salva — il cliente riceve automaticamente un'e-mail di conferma

### Annullare una prenotazione

1. Apri la prenotazione
2. Cambia lo **Stato** in **Annullato**
3. Inserisci un **Motivo di annullamento** (visualizzato nell'e-mail del cliente)
4. Salva

## Gestione della lista di attesa

Quando uno slot orario è completamente prenotato, i clienti possono aggiungersi alla lista di attesa. Spwig notifica automaticamente i clienti in lista di attesa quando un'annullamento crea uno slot disponibile.

### Visualizzazione della lista di attesa

Vai a **Catalogo > Lista di attesa per prenotazioni** per visualizzare tutte le voci della lista di attesa. Ogni voce mostra:
- Nome e indirizzo e-mail del cliente
- Il prodotto e la data desiderata
- Stato: **In attesa**, **Notificato**, **Convertito in prenotazione** o **Scaduto**

### Stati della lista di attesa

| Stato | Significato |
|--------|---------|
| **In attesa** | Il cliente è in coda, lo slot non è ancora disponibile |
| **Notificato** | Il cliente è stato informato via e-mail su uno slot disponibile |
| **Convertito in prenotazione** | Il cliente ha preso lo slot e ha completato una prenotazione |
| **Scaduto** | La data desiderata è passata senza che uno slot diventasse disponibile |

### Notificare manualmente un cliente in lista di attesa

Se desideri contattare un cliente specifico in lista di attesa prima della notifica automatica:
1. Apri la voce della lista di attesa
2. Copia il loro indirizzo e-mail e contattali direttamente
3. Una volta che completano una prenotazione, lo stato della voce della lista di attesa viene aggiornato a **Convertito in prenotazione**

## Consigli

- Abilita la conferma manuale per prenotazioni ad alto valore (es. sessioni fotografiche, eventi privati) in modo da poter verificare la disponibilità e abbinare i requisiti prima di impegnarti.
- Imposta un tempo di buffer generoso all'inizio — puoi sempre ridurlo una volta che comprendi le reali esigenze di turnaround.
- Per le classi in gruppo, imposta **Massimo numero di prenotazioni per slot** alla capacità della classe e abilita la lista di attesa in modo che le sessioni popolari creino automaticamente una coda.
- Utilizza la modalità del selettore di intervallo di date per i prodotti di alloggio — i clienti si aspettano di selezionare insieme le date di arrivo e partenza.
- Imposta un avviso minimo di prenotazione per prevenire le prenotazioni ultime minuti se hai bisogno di tempo per la preparazione (es. 48 ore minime per ordini di catering personalizzato).
- Rivedi regolarmente la tua lista di attesa durante le stagioni occupate — il contatto manuale con i clienti in lista di attesa può riempire più rapidamente le annullamenti rispetto alla notifica automatica.