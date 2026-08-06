---
title: Aggiornamenti e manutenzione
---

Spwig riceve aggiornamenti regolari con nuove funzionalità, miglioramenti delle prestazioni e correzioni di sicurezza. Questa guida copre come aggiornare l'installazione, utilizzare lo strumento diagnostico e gestire le attività di manutenzione.

## Aggiornamento di Spwig

### Prima di procedere all'aggiornamento

1. **Crea un backup** — vai a **Gestione > Metriche del sistema > Crea backup completo** o esegui lo script di backup dalla riga di comando. Questo è il tuo sistema di sicurezza in caso di problemi.
2. **Verifica la versione corrente** — visibile in **Gestione > Metriche del sistema** o nel piè di pagina del dashboard amministratore.
3. **Rivedi le modifiche** — apri la pagina **Aggiornamento del sistema** per leggere le note complete del rilascio per la nuova versione prima di installarla, inclusi eventuali passaggi aggiuntivi che il rilascio richiede (vedi di seguito).

### Rivedere le novità sulla pagina Aggiornamento del sistema

Quando Spwig rileva una versione più recente, **Dashboard del sistema** mostra un'azione rapida **Aggiornamento disponibile**. Clicca su di essa — o vai prima a **Dashboard del sistema > Aggiornamenti del piattaforma** per visualizzare il log delle modifiche, quindi procedi — per aprire la pagina **Aggiornamento del sistema**.

La pagina mostra:

- **Versione corrente** e **Versione disponibile** — card che ti permettono di confermare esattamente le versioni tra cui stai passando
- Una sezione **Novità in {versione}** — un breve riassunto del rilascio, seguito dalle note complete del rilascio formattate con titoli e elenchi puntati, esattamente come scritte dagli sviluppatori
- **Controlli pre-aggiornamento** — spazio su disco, connessione al database, un backup recente, permessi di scrittura e connettività al server di aggiornamento di Spwig. Clicca su **Esegui controlli preliminari**; il pulsante **Avvia aggiornamento** rimane disattivato finché tutti i controlli non passano
- Un banner **Prima di procedere all'aggiornamento** che ti ricorda che un backup viene creato automaticamente, il tuo negozio entra in modalità manutenzione per un breve periodo durante l'aggiornamento e non dovresti chiudere la pagina o navigare altrove mentre procede

Leggi attentamente le **Note sull'aggiornamento** nella sezione Novità — alcuni rilasci richiedono passaggi che devi eseguire personalmente dopo l'aggiornamento. Ad esempio, un rilascio che aggiunge un nuovo formato immagine potrebbe chiederti di rigenerare le miniature dei prodotti da **Libreria media > Elaborazione immagini** in modo che le immagini già presenti nella tua libreria possano beneficiare dell'aggiornamento; le nuove immagini caricate lo ottengono automaticamente, ma il tuo catalogo esistente richiede un aggiornamento manuale.

Una volta superati i controlli preliminari, clicca su **Avvia aggiornamento** per iniziare dal browser. Una barra di avanzamento traccia ogni fase, e la pagina si ricarica automaticamente una volta completato l'aggiornamento. Questo è il percorso consigliato per la maggior parte dei commercianti — utilizza lo script basato su SSH riportato di seguito se hai bisogno di un controllo più diretto del processo.

### Eseguire un aggiornamento

Accedi via SSH al tuo server e naviga nella directory di installazione di Spwig (di solito `/opt/spwig`):

```bash
./upgrade.sh
```

Lo script di aggiornamento:

1. **Controlli preliminari** — verifica lo spazio su disco, lo stato di Docker e lo stato dei servizi
2. **Esecuzione di migrazioni del database in modalità di prova** — testa che le modifiche al database si applicheranno correttamente senza effettuare effettivamente alcun cambiamento
3. **Entrata in modalità manutenzione** — il tuo negozio mostra una pagina di manutenzione ai visitatori durante l'aggiornamento
4. **Creazione di un backup** — backup automatico di sicurezza prima di apportare modifiche
5. **Svuotamento dei lavoratori in background** — attende che le attività in corso (invio di e-mail, traduzioni) si completino in modo pulito
6. **Scaricamento delle nuove immagini** — scarica l'applicazione aggiornata dal registro di Spwig
7. **Applicazione delle migrazioni del database** — aggiorna lo schema del database per la nuova versione
8. **Riavvio dei servizi** — avvia l'applicazione con la nuova versione
9. **Controllo dello stato** — verifica che tutti i servizi siano in esecuzione correttamente
10. **Uscita dalla modalità manutenzione** — il tuo negozio è nuovamente online

Se il controllo dello stato fallisce dopo l'aggiornamento, lo script **si ripristina automaticamente** alla versione precedente e ripristina il backup.

### Opzioni di aggiornamento

```bash
./upgrade.sh              # Aggiornamento standard con modalità manutenzione
./upgrade.sh --dry-run    # Controlla cosa cambierebbe senza applicare alcun cambiamento
```

## Lo strumento diagnostico

Spwig include uno strumento diagnostico integrato che controlla l'intera installazione per eventuali problemi:

```bash
./doctor.sh
```

Il doctor controlla:

| Categoria | Cosa controlla |
|----------|---------------|
| **Sistema** | Spazio su disco, utilizzo della RAM, carico CPU |
| **Docker** | Salute del motore Docker, stati dei contenitori, versioni delle immagini |
| **Database** | Connessione a PostgreSQL, stato delle migrazioni, salute del pool di connessioni |
| **Cache** | Connessione a Redis, utilizzo della memoria |
| **Storage oggetti** | Connessione a MinIO, accessibilità dei bucket |
| **Rete** | Risoluzione DNS, accessibilità delle porte, validità del certificato SSL |
| **Applicazione** | Endpoint di salute dei servizi, stato dei lavoratori in background |

Ogni controllo mostra un risultato pass/fail con dettagli se qualcosa non va.

### Modalità di riparazione automatica

Per problemi comuni, il doctor può tentare riparazioni automatiche:

```bash
./doctor.sh --fix
```

La riparazione automatica può risolvere:

- Contenitori fermi (li riavvia)
- Connessioni database obsolete (ricicla il pool di connessioni)
- Certificati SSL scaduti (attiva il rinnovo)
- Disco pieno a causa di immagini Docker obsolete (pulizia delle immagini non utilizzate)

Il doctor spiega sempre cosa intende riparare prima di agire.

## Modalità manutenzione

La modalità manutenzione mostra ai visitatori una pagina "il negozio è temporaneamente non disponibile" mentre apporti modifiche. Il pannello di amministrazione rimane accessibile.

### Abilitare la modalità manutenzione

Dal pannello di amministrazione: **Impostazioni del negozio > Manutenzione > Abilita la modalità manutenzione**

Oppure dalla riga di comando:

```bash
docker exec spwig_shop python manage.py maintenance on
```

### Disabilitare la modalità manutenzione

Dal pannello di amministrazione: attiva/disattiva l'interruttore della modalità manutenzione.

Oppure dalla riga di comando:

```bash
./go-live.sh
```

### Bypassare l'accesso durante la manutenzione

Mentre la modalità manutenzione è attiva, puoi accedere al negozio normalmente aggiungendo un parametro segreto all'URL. Il segreto di bypass è mostrato nel tuo file di configurazione `.env` sotto `MAINTENANCE_SECRET`.

## Gestione dei servizi

### Visualizzare lo stato dei servizi

Controlla lo stato di tutti i servizi Spwig:

```bash
docker compose ps
```

Questo mostra ogni servizio, il suo stato (in esecuzione, fermato, riavvio), e lo stato della sua salute.

### Visualizzare i log

Controlla i log di un servizio specifico:

```bash
docker logs spwig_shop          # Log dell'applicazione
docker logs spwig_celery         # Log dei lavoratori in background
docker logs spwig_nginx          # Log di accesso del server web
docker logs spwig_db             # Log del database
```

Aggiungi `--tail 100` per visualizzare le ultime 100 righe, o `--follow` per osservare i log in tempo reale.

### Riavviare un servizio

Se un servizio specifico necessita di un riavvio:

```bash
docker compose restart shop      # Riavvia l'applicazione
docker compose restart celery    # Riavvia i lavoratori in background
docker compose restart nginx     # Riavvia il server web
```

Per riavviare tutti i servizi:

```bash
docker compose restart
```

## Aggiornamenti dei componenti

Spwig presenta un mercato dei componenti dove puoi installare temi, fornitori di pagamento, integrazioni di spedizione e altre estensioni. I componenti vengono aggiornati indipendentemente dalla piattaforma principale.

Naviga a **Gestione > Aggiornamenti dei componenti** per controllare gli aggiornamenti disponibili per i componenti. Gli aggiornamenti vengono scaricati e applicati automaticamente quando li approvi.

## Consigli

- **Aggiorna regolarmente** — rimanere sulla versione più recente assicura che tu abbia le correzioni di sicurezza e l'accesso a nuove funzionalità
- **Leggi la sezione What's New prima di cliccare Start Upgrade** — è il modo più veloce per individuare una migrazione del database richiesta, una correzione di sicurezza o un **messaggio di note sull'aggiornamento** per cui devi agire successivamente
- **Fai sempre un backup** — anche se lo script di aggiornamento crea un backup automatico, avere il tuo proprio fornisce una maggiore sicurezza
- **Esegui doctor dopo i problemi** — se il tuo negozio si comporta in modo inaspettato, `./doctor.sh` è il modo più veloce per identificare i problemi
- **Pianifica gli aggiornamenti durante i periodi di basso traffico** — la modalità manutenzione interrompe brevemente l'accesso dei clienti, quindi aggiorna durante le ore di bassa attività
- **Mantieni lo spazio su disco disponibile** — gli aggiornamenti necessitano di spazio temporaneo per nuove immagini e backup. Mantieni almeno 5 GB liberi.