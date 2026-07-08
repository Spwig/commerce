---
title: Aggiornamenti della piattaforma
---

La tua installazione di Spwig è costruita da una serie di componenti — temi, widget, integrazioni, elementi per il costruttore di pagine e connessioni ai fornitori — ciascuno con la propria versione che può essere aggiornata in modo indipendente. Il Registro dei Componenti ti dà una visione centrale di tutto ciò che è installato, mostra quali componenti hanno aggiornamenti in attesa e ti permette di installare o annullare gli aggiornamenti in qualsiasi momento.

![Panoramica del Registro dei Componenti](/static/core/admin/img/help/platform-updates/component-registry-overview.webp)

## Comprendere il registro dei componenti

Naviga verso **Estensioni > Registro dei Componenti** per vedere ogni componente installato nel tuo negozio. Ogni riga mostra:

- **Nome** — il nome visualizzato del componente
- **Tipo** — che tipo di componente è (tema, widget, integrazione, ecc.)
- **Versione corrente** — la versione attualmente in esecuzione nel tuo negozio
- **Stato dell'aggiornamento** — se è disponibile un aggiornamento
- **Canale** — quale canale di aggiornamento segue il componente
- **Aggiornamento automatico** — se gli aggiornamenti vengono installati automaticamente
- **Bloccato** — se il componente è congelato alla sua versione corrente

Il pannello in alto nella pagina mostra i conteggi riassuntivi: numero totale di componenti installati, quanti hanno aggiornamenti disponibili e quanti sono aggiornati.

### Tipi di componenti

| Tipo | Cosa è |
|------|------------|
| Tema | Il design visivo del tuo negozio |
| Widget | Blocchi riutilizzabili per il costruttore di pagine |
| Elemento del costruttore di pagine | Elementi personalizzati per il costruttore di pagine |
| Utilità del costruttore di pagine | Strumenti e utilità per l'editor |
| Modello di intestazione/piede di pagina | Layout per l'intestazione e il piede di pagina |
| Fornitore di spedizione | Integrazioni con i corrieri (FedEx, UPS, ecc.) |
| Fornitore di email | Servizi per la consegna delle email |
| Fornitore di pagamento | Integrazioni con i gateway di pagamento |
| Fornitore di tassi di cambio | Fonti di dati per i tassi di cambio |
| Fornitore di traduzione | Servizi di traduzione basati sull'intelligenza artificiale |
| Pacchetto di lingua | File di traduzione dell'interfaccia |

## Canali di aggiornamento

Ogni componente segue un canale di aggiornamento che controlla quali rilasci riceve. Puoi assegnare ogni componente a un canale diverso in base al livello di rischio che sei disposto a tollerare.

| Canale | Descrizione | Migliore per |
|---------|-------------|----------|
| **Stabile** | Rilasci pronti per la produzione, testati in modo approfondito | Tutti i componenti nei negozi in produzione |
| **Beta** | Costruzioni pre-rilascio per testare nuove funzionalità prima che diventino stabili | Componenti non critici che desideri previsualizzare |
| **Sviluppo** | Le ultime funzionalità, potrebbero non essere stabili | Solo ambienti di test |
| **Sicurezza** | Solo patch critiche di sicurezza, consegnate con la massima priorità | Componenti per cui la stabilità è fondamentale |

Per cambiare il canale di un componente, fai clic sul suo nome per aprire la vista dettagliata, quindi seleziona un nuovo valore nel campo **Canale di aggiornamento** e salva.

## Verifica degli aggiornamenti

Spwig controlla automaticamente gli aggiornamenti all'intervallo configurato nelle impostazioni del server di aggiornamento (predefinito: ogni 24 ore). Per controllare immediatamente:

1. Naviga verso **Estensioni > Registro dei Componenti**
2. Fai clic sul pulsante **Verifica Aggiornamenti** in alto nella pagina
3. Il sistema contatta il server di aggiornamento di Spwig e aggiorna lo stato degli aggiornamenti per tutti i componenti
4. I componenti con aggiornamenti disponibili vengono evidenziati, e il conteggio **Aggiornamenti Disponibili** viene aggiornato

Puoi anche attivare un controllo degli aggiornamenti per singoli componenti utilizzando l'azione **Verifica Aggiornamenti** dal menu delle azioni della lista.

## Installazione degli aggiornamenti

### Aggiornamento di un singolo componente

1. Naviga verso **Estensioni > Registro dei Componenti**
2. Trova il componente che desideri aggiornare — i componenti con aggiornamenti disponibili mostrano un indicatore di aggiornamento accanto al loro numero di versione
3. Fai clic sul pulsante **Installa Aggiornamento** sulla riga di quel componente
4. Conferma l'aggiornamento quando richiesto
5. L'aggiornamento scarica, verifica e installa — un indicatore di avanzamento mostra ogni fase
6. Una volta completato, il numero della **Versione Corrente** del componente viene aggiornato al nuovo numero di versione

### Aggiornamento di più componenti

1.

Seleziona le caselle di controllo accanto ai componenti che desideri aggiornare
2.

Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

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

Oltre ai singoli componenti, Spwig può ricevere aggiornamenti a livello di piattaforma che aggiornano il motore principale del negozio. Questi aggiornamenti vanno attraverso un processo più approfondito che include migrazioni del database e un breve periodo di manutenzione.

La cronologia degli aggiornamenti a livello di piattaforma è visibile nella sezione **Platform Updates** del registro. Ogni voce mostra la transizione di versione (es. `v1.3.2 → v1.3.3`), lo stato e la durata del processo di aggiornamento.

Gli aggiornamenti di sicurezza vengono contrassegnati separatamente e, se **Auto Install Security Updates** è abilitato nella configurazione del server degli aggiornamenti, vengono installati automaticamente senza richiedere un'azione manuale.

## Visualizzazione della cronologia delle versioni

Per visualizzare tutte le versioni precedentemente installate di un componente:

1. Fai clic sul nome del componente per aprire la sua vista dettagliata
2. Scorri fino alla sezione **Component Versions** in fondo alla pagina
3. Ogni voce di versione mostra il numero di versione, quando è stata installata, il metodo di installazione e lo stato di salute

Il sistema mantiene disponibili le ultime tre versioni installate per il rollback. Le versioni al di là di questa soglia vengono eliminate automaticamente.

## Rollback di un componente

Se un aggiornamento causa problemi, puoi tornare a una versione precedente:

1. Apri la vista dettagliata del componente
2. Scorri fino alla sezione **Rollback**
3. Seleziona la versione che desideri ripristinare
4. Fai clic su **Roll Back to this Version**

Solo le versioni contrassegnate come **Rollback Available** possono essere ripristinate. L'entry del log del rollback registra chi ha iniziato il rollback e quando.

## Blocco dei componenti

Il blocco di un componente impedisce l'installazione di qualsiasi aggiornamento, incluso quelli automatici. Questo è utile quando hai personalizzazioni o integrazioni che dipendono da una versione specifica.

1. Apri la vista dettagliata del componente
2. Seleziona la casella **Locked** nella sezione **Lock & Freeze**
3. Inserisci una ragione in **Lock Reason** in modo che il tuo team capisca perché è bloccato
4. Salva il record

I componenti bloccati vengono visualizzati con un indicatore di blocco nell'elenco del registro. Per sbloccarli, deseleziona **Locked** e salva.

## Lettura dei log degli aggiornamenti

Il log degli aggiornamenti registra ogni operazione di installazione, aggiornamento, rollback e controllo di salute:

1. Apri la vista dettagliata di un componente
2. I **Update Logs** sono visibili inline in fondo alla pagina
3. Ogni entry mostra: l'azione eseguita, gli orari di inizio e fine, le versioni vecchie e nuove, se l'operazione è stata automatica o manuale, e eventuali messaggi di errore se l'operazione è fallita

Le entry del log con lo stato **Failed** includono il messaggio di errore completo per aiutare nel risoluzione dei problemi.

## Abilitazione degli aggiornamenti automatici

Puoi permettere a Spwig di installare gli aggiornamenti automaticamente non appena diventano disponibili:

1. Apri la vista dettagliata del componente
2. Seleziona **Auto Update** nella sezione **Version & Update Status**
3. Salva il record

Con l'aggiornamento automatico abilitato, il sistema installa gli aggiornamenti durante il prossimo ciclo di controllo programmato. Gli aggiornamenti di sicurezza seguono l'impostazione globale **Auto Install Security Updates**, indipendentemente dalle impostazioni dei singoli componenti.

## Suggerimenti

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- Aggiorna sempre sul canale **Stable** per i temi e i fornitori di pagamento — questi sono i componenti più visibili ai clienti e la stabilità è la cosa più importante
- Blocca un componente prima di apportare modifiche personalizzate, e registra chiaramente il motivo in modo che i membri futuri del team sappiano di non aggiornarlo
- Controlla le **Note sulla Release** nell'entry della versione del componente prima di installare un aggiornamento significativo — le modifiche rompenti sono segnalate lì
- Dopo un aggiornamento, visita l'area interessata del tuo negozio per confermare che tutto appaia e funzioni come previsto prima di dichiarare l'aggiornamento completo
- Se l'aggiornamento automatico è abilitato per un componente, monitora periodicamente le **Log degli Aggiornamenti** per assicurarti che gli aggiornamenti automatici siano completati con successo