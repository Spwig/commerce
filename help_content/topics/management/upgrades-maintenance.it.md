---
title: Aggiornamenti e manutenzione
---

Spwig riceve aggiornamenti regolari con nuove funzionalità, miglioramenti delle prestazioni e correzioni di sicurezza. Questa guida copre come aggiornare l'installazione, utilizzare lo strumento diagnostico e gestire le attività di manutenzione.

## Aggiornamento di Spwig

### Prima di procedere all'aggiornamento

1. **Crea un backup** — vai a **Gestione > Metriche del sistema > Crea backup completo** o esegui lo script di backup dalla riga di comando. Questo è il tuo scudo di sicurezza nel caso in cui qualcosa vada storto.
2. **Verifica la versione corrente** — visibile in **Gestione > Metriche del sistema** o nel piè di pagina del pannello di amministrazione.
3. **Leggi le note sulla versione** — disponibili nel pannello di amministrazione sotto **Gestione > Aggiornamenti dei componenti** quando viene rilevata una nuova versione.

### Esecuzione di un aggiornamento

Accedi via SSH al tuo server e naviga nella directory di installazione di Spwig (tipicamente `/opt/spwig`):

```bash
./upgrade.sh
```

Lo script di aggiornamento:

1. **Controlli preliminari** — verifica lo spazio su disco, lo stato di salute di Docker e lo stato dei servizi
2. **Esecuzione di migrazioni del database in modalità di prova** — testa che i cambiamenti al database si applicheranno correttamente senza effettuare alcun cambiamento effettivo
3. **Entrata in modalità manutenzione** — il tuo negozio mostra una pagina di manutenzione ai visitatori durante l'aggiornamento
4. **Crea un backup** — backup automatico di sicurezza prima di apportare modifiche
5. **Svuota i lavoratori in background** — attende che le attività in corso (invio email, traduzioni) terminino in modo pulito
6. **Scarica nuove immagini** — scarica l'applicazione aggiornata dal registro Spwig
7. **Applica le migrazioni del database** — aggiorna lo schema del database per la nuova versione
8. **Riavvia i servizi** — avvia l'applicazione con la nuova versione
9. **Controllo della salute** — verifica che tutti i servizi siano in esecuzione correttamente
10. **Uscita dalla modalità manutenzione** — il tuo negozio è nuovamente online

Se il controllo della salute fallisce dopo l'aggiornamento, lo script **esegue automaticamente un rollback** alla versione precedente e ripristina il backup.

### Opzioni di aggiornamento

```bash
./upgrade.sh              # Aggiornamento standard con modalità manutenzione
./upgrade.sh --dry-run    # Controlla cosa cambierebbe senza applicare modifiche
```

## Lo strumento diagnostico

Spwig include uno strumento diagnostico integrato che controlla l'intera installazione per problemi:

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
| **Archiviazione oggetti** | Connessione a MinIO, accessibilità dei bucket |
| **Rete** | Risoluzione DNS, accessibilità delle porte, validità del certificato SSL |
| **Applicazione** | Endpoint di salute dei servizi, stato dei lavoratori in background |

Ogni controllo mostra un risultato pass/fail con dettagli se qualcosa non va.

### Modalità di riparazione automatica

Per problemi comuni, il doctor può tentare riparazioni automatiche:

```bash
./doctor.sh --fix
```

La riparazione automatica può risolvere:

- Contenitori fermi (riavvia)
- Connessioni al database obsolete (ricicla il pool di connessioni)
- Certificati SSL scaduti (attiva il rinnovo)
- Disco pieno a causa di immagini Docker obsolete (pulisci le immagini non utilizzate)

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

Durante l'attivazione della modalità manutenzione, puoi accedere al negozio normalmente aggiungendo un parametro segreto all'URL. Il segreto di bypass è mostrato nel tuo file di configurazione `.env` sotto `MAINTENANCE_SECRET`.

## Gestione dei servizi

### Visualizzazione dello stato dei servizi

# Verifica lo stato di tutti i servizi Spwig:

```bash
docker compose ps
```

Questo mostra ogni servizio, lo stato (in esecuzione, arrestato, riavvio), e lo stato di salute.

### Visualizzazione dei log

Verifica i log di un servizio specifico:

```bash
docker logs spwig_shop          # Log dell'applicazione
docker logs spwig_celery         # Log del worker in background
docker logs spwig_nginx          # Log di accesso del server web
docker logs spwig_db             # Log del database
```

Aggiungi `--tail 100` per visualizzare le ultime 100 righe, o `--follow` per visualizzare i log in tempo reale.

### Riavvia un servizio

Se è necessario riavviare un servizio specifico:

```bash
docker compose restart shop      # Riavvia l'applicazione
docker compose restart celery    # Riavvia i worker in background
docker compose restart nginx     # Riavvia il server web
```

Per riavviare tutti i servizi:

```bash
docker compose restart
```

## Aggiornamenti dei componenti

Spwig presenta un mercato dei componenti dove puoi installare temi, fornitori di pagamento, integrazioni di spedizione e altre estensioni. I componenti vengono aggiornati in modo indipendente dalla piattaforma principale.

Vai a **Management > Component Updates** per controllare gli aggiornamenti dei componenti disponibili. Gli aggiornamenti vengono scaricati e applicati automaticamente quando li approvi.

## Consigli

- **Aggiorna regolarmente** — rimanendo sulla versione più recente assicuri di avere le correzioni di sicurezza e l'accesso a nuove funzionalità
- **Fai sempre un backup** — anche se lo script di aggiornamento crea un backup automatico, avere il tuo proprio backup offre una maggiore sicurezza
- **Esegui doctor dopo i problemi** — se il tuo negozio si comporta in modo inaspettato, `./doctor.sh` è il modo più veloce per identificare i problemi
- **Pianifica gli aggiornamenti durante i periodi di basso traffico** — la modalità manutenzione interrompe brevemente l'accesso dei clienti, quindi aggiorna durante le ore di bassa attività
- **Mantieni lo spazio su disco disponibile** — gli aggiornamenti necessitano di spazio temporaneo per nuove immagini e backup. Mantieni almeno 5 GB liberi.