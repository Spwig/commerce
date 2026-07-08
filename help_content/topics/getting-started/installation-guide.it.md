---
title: Guida all'installazione
---

Questa guida ti accompagna nell'installazione di Spwig sul tuo proprio server. L'intero processo è automatizzato — un singolo comando gestisce l'impostazione di Docker, la creazione del database, la configurazione dei servizi e i certificati SSL.

## Prima di iniziare

Hai bisogno di:

- Un server che esegua **Ubuntu 22.04 o 24.04** (Debian 12 è anche supportato)
- **Accesso root o sudo** al server
- Almeno **4 GB RAM** e **20 GB di spazio su disco** (si consiglia **8 GB RAM**)
- Un **token di licenza** dal tuo acquisto di Spwig (controlla la ricevuta email)
- Opzionalmente, un **nome di dominio** puntato all'indirizzo IP del tuo server

> **Consiglio:** Puoi installare senza un dominio e aggiungerne uno in seguito utilizzando lo strumento di configurazione del dominio. Nel frattempo, il tuo negozio sarà accessibile tramite l'indirizzo IP del server.

## Esecuzione dell'installer

Connetti il tuo server tramite SSH e esegui il comando di installazione ricevuto nell'email di conferma dell'acquisto. Ha questo aspetto:

```bash
curl -fsSL https://spwig.com/install.sh | sudo bash -s -- --token YOUR_LICENSE_TOKEN
```

Sostituisci `YOUR_LICENSE_TOKEN` con il token ricevuto via email.

L'installer procede automaticamente attraverso otto fasi:

1. **Controlli preliminari** — verifica che il server soddisfi i requisiti (sistema operativo, disco, RAM, porte)
2. **Convalida del token** — conferma la licenza e estrae la configurazione del tuo negozio
3. **Rilevamento della modalità** — determina la migliore modalità di installazione per il tuo server (vedi di seguito)
4. **Configurazione** — genera password sicure, credenziali del database e configurazione dei servizi
5. **Download delle immagini** — scarica le immagini dell'applicazione Spwig dal registro
6. **Avvio dei servizi** — avvia il database, il cache, l'applicazione e i lavoratori in background nell'ordine
7. **Configurazione SSL** — ottiene un certificato SSL se hai un dominio configurato
8. **Finalizzazione** — crea il tuo account amministratore e genera script di comodo

Il processo dura da 5 a 15 minuti, a seconda della velocità di connessione internet del tuo server.

## Modalità di installazione

L'installer rileva automaticamente l'ambiente del server e seleziona la modalità migliore. Puoi anche specificarne una manualmente con il flag `--mode`.

### Modalità standalone

**Migliore per:** Server dedicati e istanze VPS dove Spwig è l'unica applicazione web.

- Utilizza le porte 80 e 443 direttamente
- Gestisce automaticamente i certificati SSL tramite Let's Encrypt
- Questa è la modalità più comune e consigliata

### Modalità sidecar

**Migliore per:** Server che già eseguono un'altra applicazione web (WordPress, un sito aziendale, ecc.) sulle porte 80/443.

- Spwig funziona su una porta alternativa (rilevata automaticamente, tipicamente 8080 o 8443)
- L'installer genera un blocco di configurazione nginx da aggiungere al tuo server web esistente
- Il tuo server web esistente gestisce SSL e proxy traffic verso Spwig

### Modalità locale

**Migliore per:** Sviluppo e test sul tuo computer.

- Accessibile solo a `localhost` o `127.0.0.1`
- Utilizza un certificato SSL autofirmato (il browser mostrerà un avviso di sicurezza — è normale)
- Sono abilitate le funzionalità di debug
- Non è richiesta la convalida della licenza

## Cosa accade durante l'installazione

### Docker

Se Docker non è già installato, l'installer offre l'opzione di installarlo. Spwig funziona interamente all'interno di contenitori Docker — niente viene installato direttamente sul sistema operativo del server al di fuori di Docker.

### Servizi creati

L'installer crea questi servizi:

| Servizio | Scopo |
|---------|---------|
| **Database** (PostgreSQL 16) | Archivia tutti i dati del tuo negozio — prodotti, ordini, clienti, impostazioni |
| **Cache** (Redis) | Accelerare il caricamento delle pagine e gestire le code per i task in background |
| **Connection pooler** (PgBouncer) | Gestisce le connessioni al database in modo efficiente |
| **Object storage** (MinIO) | Archivia immagini, file e media caricati |
| **Application** (Spwig) | Il negozio stesso — pannello di amministrazione e sito di vendita |
| **Web server** (Nginx) | Fornisce il tuo negozio ai visitatori con compressione e caching |
| **Background worker** (Celery) | Gestisce email, traduzioni, analisi e altri task in background |
| **Task scheduler** (Celery Beat) | Esegue task pianificati come backup automatici e campagne email |
| **Translator** | Servizio di traduzione alimentato da AI per negozi multilingue |
| **Upgrader** | Gestisce gli aggiornamenti dei componenti dal marketplace Spwig |

### Account amministratore

Alla fine dell'installazione, ti viene chiesto di creare un account amministratore. Questo è l'account che utilizzerai per accedere al pannello di amministrazione del tuo negozio.

### Modalità manutenzione

Il tuo negozio inizia in **modalità manutenzione** — i visitatori vedranno una pagina "Coming Soon". Questo ti dà tempo per configurare il tuo negozio (aggiungere prodotti, impostare metodi di pagamento, personalizzare il tema) prima di andare online.

Quando sei pronto, esegui lo script di comodo creato dall'installer:

```bash
./go-live.sh
```

Oppure disattiva la modalità manutenzione da **Admin > Store Settings > Maintenance**.

## Dopo l'installazione

Una volta completata l'installazione, vedrai un riepilogo con:

- L'URL del tuo negozio
- L'URL del pannello di amministrazione (tipicamente `https://yourdomain.com/en/admin/`)
- La posizione dei file di configurazione
- Script di comodo disponibili

### Script di comodo

L'installer crea questi script nella directory di installazione:

- **`./go-live.sh`** — esce dalla modalità manutenzione del tuo negozio
- **`./configure-domain.sh`** — aggiunge o modifica il tuo dominio e ottiene un certificato SSL

### Passaggi successivi

1. Accedi al tuo pannello di amministrazione
2. Completa il **Setup Wizard** — ti guida attraverso il nome del negozio, la valuta, il fuso orario e le impostazioni di base
3. Aggiungi i tuoi prodotti
4. Configura un metodo di pagamento
5. Scegli e personalizza un tema
6. Esegui `./go-live.sh` quando sei pronto

## Installazione su marketplace cloud

Spwig è disponibile come applicazione a un clic su diversi provider cloud:

- **DigitalOcean** — distribuisci dal DigitalOcean Marketplace
- **Akamai (Linode)** — distribuisci dal Linode Marketplace
- **Vultr** — distribuisci dal Vultr Marketplace

Queste immagini del marketplace vengono fornite con l'installer pre-caricato. Dopo aver creato il server, accedi via SSH e segui le istruzioni a schermo per completare l'installazione con il tuo token di licenza.

## Ottenere aiuto

Se l'installazione fallisce o incontri un errore:

1. Esegui lo **strumento diagnostico**: `./doctor.sh` (creato durante l'installazione)
2. L'analizzatore controlla tutti i servizi, la connettività, l'SSL e i problemi comuni
3. Usa `./doctor.sh --fix` per tentare riparazioni automatiche
4. Contatta il supporto Spwig con l'output dello strumento diagnostico se il problema persiste