---
title: Aggiornamenti della piattaforma
---

La tua installazione di Spwig è costruita da una serie di componenti — temi, widget, integrazioni, elementi del costruttore di pagine e connessioni ai fornitori — ciascuno con la propria versione che può essere aggiornata in modo indipendente. Il Registro dei Componenti ti fornisce una visione centrale di tutto ciò che è installato, mostra quali componenti hanno aggiornamenti in attesa e ti permette di installare o annullare gli aggiornamenti in qualsiasi momento.

![Panoramica del Registro dei Componenti](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Comprendere il registro dei componenti

Naviga verso **Pannello di Sistema > Aggiornamenti dei Componenti** per visualizzare ogni componente installato nel tuo negozio. Ogni riga mostra:

- **Nome** — il nome visualizzato del componente
- **Tipo** — di che tipo di componente si tratta (tema, widget, integrazione, ecc.)
- **Versione corrente** — la versione attualmente in esecuzione nel tuo negozio
- **Stato dell'aggiornamento** — se è disponibile un aggiornamento
- **Canale** — quale canale di aggiornamento segue il componente
- **Aggiornamento automatico** — se gli aggiornamenti vengono installati automaticamente
- **Bloccato** — se il componente è bloccato alla sua versione corrente

Il pannello in alto nella pagina mostra i conteggi riassuntivi: numero totale di componenti installati, quanti hanno aggiornamenti disponibili e quanti sono aggiornati.

### Tipi di componenti

| Tipo | Cosa è |
|------|------------|
| Tema | Il design visivo del tuo negozio |
| Widget | Blocchi riutilizzabili del costruttore di pagine |
| Elemento del Costruttore di Pagine | Elementi personalizzati per il costruttore di pagine |
| Utilità del Costruttore di Pagine | Strumenti e utilità per l'editor |
| Modello di Intestazione/Piede di Pagina | Layout per l'intestazione e il piede di pagina |
| Fornitore di Spedizione | Integrazioni con i corrieri (FedEx, UPS, ecc.) |
| Fornitore di Email | Servizi per la consegna delle email |
| Fornitore di Pagamento | Integrazioni con gateway di pagamento |
| Fornitore di Tasso di Cambio | Fonti di dati per i tassi di cambio |
| Fornitore di Traduzione | Servizi di traduzione basati sull'AI |
| Pacchetto di Lingua | File di traduzione dell'interfaccia |

## Canali di aggiornamento

Ogni componente segue un canale di aggiornamento che determina quali rilasci riceve. Puoi assegnare ogni componente a un canale diverso in base al livello di rischio che sei disposto a tollerare.

| Canale | Descrizione | Migliore per |
|---------|-------------|----------|
| **Stabile** | Rilasci pronti per la produzione, testati in modo approfondito | Tutti i componenti nei negozi in produzione |
| **Beta** | Costruzioni pre-rilascio per testare nuove funzionalità prima che diventino stabili | Componenti non critici che desideri previsualizzare |
| **Sviluppo** | Le ultime funzionalità, potrebbero essere instabili | Solo ambienti di test |
| **Sicurezza** | Solo patch critiche di sicurezza, consegnate con la massima priorità | Componenti per cui la stabilità è fondamentale |

Per cambiare il canale di un componente, fai clic sul suo nome per aprire la vista dettagliata, quindi seleziona un nuovo valore nel campo **Canale di Aggiornamento** e salva.

## Verifica degli aggiornamenti

Spwig controlla automaticamente gli aggiornamenti all'intervallo configurato nelle impostazioni del server di aggiornamento (predefinito: ogni 24 ore). Per controllare immediatamente:

1. Naviga verso **Pannello di Sistema > Aggiornamenti dei Componenti**
2. Fai clic sul pulsante **Verifica Aggiornamenti** in alto sulla pagina
3. Il sistema contatta il server di aggiornamento di Spwig e aggiorna lo stato degli aggiornamenti per tutti i componenti
4. I componenti con aggiornamenti disponibili vengono evidenziati, e il conteggio **Aggiornamenti Disponibili** viene aggiornato

Puoi anche attivare un controllo degli aggiornamenti per singoli componenti utilizzando l'azione **Verifica Aggiornamenti** dal menu delle azioni della lista.

## Installazione degli aggiornamenti

### Aggiornamento di un singolo componente

1. Naviga verso **Pannello di Sistema > Aggiornamenti dei Componenti**
2. Trova il componente che desideri aggiornare — i componenti con aggiornamenti disponibili mostrano un indicatore di aggiornamento accanto al loro numero di versione
3. Fai clic sul pulsante **Installa Aggiornamento** sulla riga di quel componente
4. Conferma l'aggiornamento quando richiesto
5. L'aggiornamento viene scaricato, verificato e installato — un indicatore di avanzamento mostra ogni fase
6. Una volta completato, il **Numero di Versione Corrente** del componente viene aggiornato al nuovo numero di versione

### Aggiornamento di più componenti

1.

Seleziona le caselle di controllo accanto ai componenti che desideri aggiornare
2.

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

Seleziona **Install updates** dal menu a discesa **Action**
3.

Fai clic su **Go** per procedere
4.

Gli aggiornamenti vengono installati nell'ordine delle dipendenze — vengono aggiornati prima i componenti su cui altri dipendono

### Cosa accade durante un aggiornamento

Il processo di aggiornamento passa attraverso queste fasi:

1. **Checking** — conferma che l'aggiornamento è disponibile e che il tuo abbonamento è valido
2. **Downloading** — recupera il pacchetto dal server degli aggiornamenti di Spwig
3. **Verifying** — verifica l'integrità del pacchetto rispetto a un controllo di somma SHA-256
4. **Extracting** — estrae i nuovi file
5. **Deploying** — attiva la nuova versione
6. **Health check** — verifica che il componente funzioni correttamente dopo l'aggiornamento

Se una qualsiasi fase fallisce, il sistema tenta automaticamente di ripristinare la versione precedente.

## Aggiornamenti a livello di piattaforma

Oltre ai singoli componenti, Spwig può ricevere aggiornamenti a livello di piattaforma che aggiornano il motore principale del negozio. Questi aggiornamenti passano attraverso un processo più approfondito che include migrazioni del database e un breve periodo di manutenzione.

Vai a **System Dashboard > Platform Updates** per visualizzare e gestire gli aggiornamenti a livello di piattaforma separatamente dai singoli componenti.

### Rivedi cosa è nuovo prima di installare

Fai clic su **Check for Updates** per verificare se una nuova versione della piattaforma è disponibile. Quando una versione è disponibile, la scheda **Update Available** mostra il cambiamento di versione (es. `v1.7.0 → v1.7.1`), la **Package Size**, **Est. Time**, e il **Channel** dell'aggiornamento — e un'anteprima **What's New** in modo da poter vedere cosa è cambiato prima di decidere di installare:

- Una breve riga descrittiva che spiega il rilascio
- Un elenco puntato dei principali cambiamenti in quella versione (fino a cinque, con una nota se ce ne sono di più)

Se l'aggiornamento modifica lo schema del database, compare un avviso **Requires database migration** con un tempo stimato. Gli aggiornamenti di sicurezza mostrano un badge **Security update** che ti consiglia di installarli immediatamente. Leggi l'anteprima **What's New** prima di installare — è il modo più veloce per vedere se un rilascio richiede attenzione aggiuntiva, ad esempio passaggi specifici da eseguire dopo il completamento dell'aggiornamento.

La cronologia degli aggiornamenti della piattaforma è visibile più in basso nella pagina. Ogni voce mostra la transizione di versione (es. `v1.3.2 → v1.3.3`), lo stato e la durata del processo di aggiornamento.

Gli aggiornamenti di sicurezza vengono contraddistinti separatamente e, se **Auto Install Security Updates** è abilitato nella configurazione del server degli aggiornamenti, vengono installati automaticamente senza richiedere un'azione manuale.

## Visualizzazione della cronologia delle versioni

Per visualizzare tutte le versioni precedentemente installate di un componente:

1. Fai clic sul nome del componente per aprire la sua vista dettagliata
2. Scorri fino alla sezione **Component Versions** in fondo alla pagina
3. Ogni voce di versione mostra il numero di versione, quando è stata installata, il metodo di installazione e lo stato di salute

Il sistema mantiene disponibili le ultime tre versioni installate per il rollback. Le versioni al di là di questa soglia vengono eliminate automaticamente.

## Rollback di un componente

Se un aggiornamento causa problemi, puoi tornare indietro a una versione precedente:

1. Apri la vista dettagliata del componente
2. Scorri fino alla sezione **Rollback**
3. Seleziona la versione che desideri ripristinare
4. Fai clic su **Roll Back to this Version**

Solo le versioni contrassegnate con **Rollback Available** possono essere ripristinate. L'entry del log del rollback registra chi ha iniziato il rollback e quando.

## Blocco dei componenti

Il blocco di un componente impedisce l'installazione di qualsiasi aggiornamento, incluso quelli automatici. Questo è utile quando hai personalizzazioni o integrazioni che dipendono da una versione specifica.

1. Apri la vista dettagliata del componente
2. Seleziona la casella **Locked** nella sezione **Lock & Freeze**
3. Inserisci una ragione in **Lock Reason** in modo che il tuo team sappia perché è bloccato
4. Salva il record

I componenti bloccati vengono visualizzati con un indicatore a forma di chiave nella lista del registro. Per sbloccarli, deseleziona **Locked** e salva.

## Lettura dei log degli aggiornamenti

Il log degli aggiornamenti registra ogni operazione di installazione, aggiornamento, rollback e controllo di salute:

1.

Apri la vista dettagliata di un componente
2.

I **Update Logs** sono visibili inline in fondo alla pagina
3.



Ogni voce mostra: l'azione eseguita, gli orari di inizio e fine, le versioni vecchie e nuove, se l'aggiornamento è stato automatico o manuale, e eventuali messaggi di errore se l'operazione è fallita

Le voci del log con lo stato **Failed** includono il messaggio di errore completo per aiutare nel risolvere i problemi.

## Abilitare gli aggiornamenti automatici

È possibile permettere a Spwig di installare gli aggiornamenti automaticamente non appena disponibili:

1. Apri la vista dettagliata del componente
2. Seleziona **Auto Update** nella sezione **Version & Update Status**
3. Salva il record

Con l'aggiornamento automatico abilitato, il sistema installerà gli aggiornamenti durante il prossimo ciclo di controllo programmato. Gli aggiornamenti di sicurezza seguono l'impostazione globale **Auto Install Security Updates**, indipendentemente dalle impostazioni dei singoli componenti.

## Consigli

- Aggiorna sempre sul canale **Stable** per i temi e i fornitori di pagamento — questi sono i componenti più esposti ai clienti e la stabilità è la cosa più importante
- Blocca un componente prima di apportare modifiche personalizzate ad esso, e registra chiaramente il motivo in modo che i membri del team futuri sappiano di non aggiornarlo
- Controlla le **Release Notes** nell'entry della versione del componente prima di installare un incremento di versione importante — le modifiche rompenti sono segnalate lì
- Prima di installare un aggiornamento della piattaforma, leggi l'anteprima **What's New** sulla pagina **Platform Updates** — per una visione completa delle note di rilascio, incluso eventuali passaggi aggiuntivi che potresti dover eseguire, continua alla pagina **System Upgrade**
- Dopo un aggiornamento, visita l'area interessata del tuo negozio per confermare che tutto sembri e funzioni come previsto prima di dichiarare l'aggiornamento completato
- Se l'aggiornamento automatico è abilitato per un componente, monitora periodicamente i **Update Logs** per assicurarti che gli aggiornamenti automatici vengano completati con successo