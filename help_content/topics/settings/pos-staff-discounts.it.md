---
title: Sconti per il personale POS e sicurezza del terminale
---

Le impostazioni degli sconti per il personale POS ti permettono di controllare quanto sconto ciascun membro dello staff può applicare al momento del pagamento. Gli eventi di blocco del terminale forniscono un registro di audit di ogni volta in cui un terminale è stato bloccato o sbloccato, aiutandoti a tracciare chi ha avuto accesso al terminale e se sono avvenuti tentativi di accesso falliti.

## Limiti degli sconti per il personale

Ogni membro dello staff che utilizza il POS può avere permessi di sconto individuali. Di default, lo staff può applicare uno sconto fino al 10% sugli articoli o sull'intero carrello. Puoi aumentare o ridurre questo limite per persona, o designare lo staff come manager che possono approvare sconti che superano i limiti standard.

### Configurazione del limite di sconto per un membro dello staff

1. Vai a **POS > Sconti per il personale**
2. Clicca su **+ Aggiungi sconto per il personale POS** o clicca su un membro dello staff esistente per modificare
3. Seleziona il **Membro dello staff** dall'elenco
4. Imposta i limiti degli sconti:

| Campo | Descrizione |
|-------|-------------|
| **Massimo sconto %** | Percentuale massima di sconto che questa persona può applicare (es. `10` per 10%) |
| **Massimo importo sconto** | Importo fisso massimo per transazione (lascia vuoto per non avere un limite fisso) |
| **Applicare sconti su singoli articoli** | Consente di applicare sconti su singoli elementi del carrello |
| **Applicare sconti sull'intero carrello** | Consente di applicare sconti sull'importo totale del carrello |
| **Richiedi motivo** | Quando selezionato, il membro dello staff deve inserire un motivo prima di applicare qualsiasi sconto |

5. Clicca su **Salva**

### Funzionamento dei limiti degli sconti al POS

Quando un cassiere tenta di applicare uno sconto:
- Se lo sconto è entro il limite, viene applicato immediatamente
- Se lo sconto supera il limite, il terminale richiede **l'approvazione di un manager**
- Un manager inserisce il proprio PIN per autorizzare l'override, e lo sconto viene applicato

Questo flusso di lavoro impedisce sconti di alto valore non autorizzati, consentendo flessibilità quando gli sconti sono realmente necessari.

## Ruoli dei manager

I membri dello staff con il flag **È manager** possono approvare sconti che superano i limiti di altri membri dello staff. I manager vengono identificati al terminale da un PIN che inseriscono quando viene richiesta un'approvazione.

### Configurazione di un manager

1. Apri il record degli sconti di un membro dello staff
2. Seleziona **È manager**
3. Inserisci un **PIN manager** (4-6 cifre) — questo viene crittografato in modo sicuro al salvataggio
4. Clicca su **Salva**

Il PIN manager è separato dal PIN del cassiere utilizzato per il blocco/sblocco del terminale. Un manager può avere sia un PIN manager (per l'approvazione degli sconti) che un PIN del cassiere (per l'accesso al terminale).

### Sicurezza del PIN manager

Quando inserisci un PIN nel modulo amministrativo e lo salvi, Spwig lo crittografa automaticamente — il PIN non crittografato non viene mai memorizzato. Il campo del PIN non crittografato si svuota dopo il salvataggio, che è un comportamento previsto.

## PIN del cassiere e accesso con carta

Ogni membro dello staff può anche avere un **PIN del cassiere** per bloccare e sbloccare il terminale:

- **PIN del cassiere** — PIN di 4-6 cifre utilizzato per sbloccare il terminale dopo che si è bloccato automaticamente o manualmente
- **Identificatore della carta** — Una carta registrata (carta da swipe o NFC) può essere utilizzata anche per sbloccare il terminale

Per configurare un PIN del cassiere, inseriscilo nel campo **PIN del cassiere** e salva. Come il PIN manager, viene crittografato automaticamente al salvataggio.

## Eventi di blocco del terminale

Ogni volta che un terminale viene bloccato o sbloccato, Spwig registra un evento di blocco del terminale. Questo crea un registro completo di audit della sicurezza.

### Visualizzazione degli eventi di blocco

Vai a **POS > Eventi di blocco del terminale** per visualizzare la cronologia completa. Puoi filtrare gli eventi per:
- Terminale
- Tipo di evento
- Intervallo di date

### Tipi di eventi


| Evento | Significato |
|-------|---------|
| **Blocco Manuale** | Un membro dello staff ha deliberatamente bloccato il terminale |
| **Blocco Automatico (Timeout di Inattività)** | Il terminale è stato bloccato automaticamente a causa di inattività |
| **Sblocco da Cassiere** | Il cassiere si è autenticato e ha sbloccato il terminale |
| **Sblocco da Manager** | Un manager ha utilizzato le proprie credenziali per sbloccare il terminale |
| **Sblocco con Carta** | Il terminale è stato sbloccato utilizzando una carta registrata |
| **Sblocco con Biometria** | Il terminale è stato sbloccato utilizzando impronta digitale o riconoscimento facciale |
| **Sblocco Fallito** | È stata fatta un'azione di sblocco con credenziali errate |
| **Blocco (3+ fallimenti)** | Il terminale è stato bloccato dopo tentativi ripetuti falliti |

### Cosa contengono i record degli eventi di blocco

Ogni evento registra:
- Il **Terminale** coinvolto
- Il **Tipo di Evento**
- Chi ha eseguito l'azione (**Eseguito da**) e chi era loggato quando è avvenuto il blocco (**Bloccato da**)
- Se è stato utilizzato un **Override del Manager**
- Il **Metodo di Sblocco** (PIN, carta o biometria)
- **Tentativi falliti** prima di questo evento (utile per rilevare pattern di forza bruta)
- Il **Totale del Carrello** e il numero di articoli al momento dell'evento
- L'indirizzo IP della richiesta

### Investigare un problema di sicurezza

Se sospetti un accesso non autorizzato a un terminale:

1. Vai a **POS > Eventi di Blocco del Terminale**
2. Filtra per il terminale in questione
3. Cerca eventi del tipo **Sblocco Fallito** o **Blocco** — indicano accessi ripetuti falliti
4. Controlla il campo **Eseguito da** negli sblocchi riusciti per vedere chi ha ottenuto l'accesso
5. Incrocia con i record delle shift (**POS > Shifts**) per verificare il cassiere che doveva essere di turno

## Consigli

- Imposta limiti per gli sconti in base al livello di esperienza dello staff — lo staff nuovo potrebbe iniziare al 5%, lo staff esperto al 10-15%, e i manager possono approvare qualsiasi percentuale superiore.
- Abilita **Richiedi Motivo** per qualsiasi membro dello staff con limiti di sconto più elevati. Avere un motivo registrato ti aiuta a analizzare i pattern degli sconti e a identificare eventuali abusi.
- Controlla gli eventi di blocco del terminale settimanalmente se il tuo negozio ha molti dipendenti o un alto turnover — i pattern di accesso irregolari sono più facili da rilevare prima che diventino un problema.
- Se un membro dello staff lascia, rimuovi immediatamente il loro PIN e l'identificatore della carta per prevenire l'accesso al terminale.
- Utilizza l'evento di blocco per identificare i terminali che potrebbero necessitare di un timeout di blocco automatico aggiustato — se i clienti attivano frequentemente blocchi accidentali, il timeout di inattività potrebbe essere impostato troppo breve.
- I PIN dei manager dovrebbero essere aggiornati periodicamente. Aggiornali nel record degli sconti dello staff — il nuovo PIN viene hashato al salvataggio.