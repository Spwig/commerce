---
title: Panoramica del sistema POS
---

Il sistema POS di Spwig trasforma il tuo negozio in una soluzione completa per il retail con terminali moderni di punto di vendita. È incluso in ogni edizione — Community, Pro e Enterprise — con un numero illimitato di terminali in un numero illimitato di ubicazioni senza costi aggiuntivi. Ogni terminale è un'app Web Progressiva (PWA) che funziona offline, sincronizza automaticamente e si integra perfettamente con il tuo inventario, i dati dei clienti e il processo di pagamento. Gestisci tutto dal dashboard di amministrazione: configurazione del terminale, conciliazione delle shift, personalizzazione delle ricevute e integrazione del hardware.

Utilizza il sistema POS quando hai ubicazioni fisiche, negozi pop-up, fiere commerciali o qualsiasi ambiente in cui i clienti effettuano acquisti di persona invece che online.

![Dashboard POS](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## Cosa è Spwig POS?

Spwig POS è un sistema di punto di vendita completamente integrato progettato per i commercianti che vendono sia online che in ubicazioni fisiche. A differenza dei sistemi POS di terze parti che richiedono integrazioni complesse, Spwig POS è costruito direttamente nella tua piattaforma, garantendo una perfetta sincronizzazione dei dati in tutti i canali di vendita.

**Caratteristiche principali**:
- **Terminali illimitati** - Distribuisci quanti terminali necessari senza costi aggiuntivi
- **Architettura a priorità offline** - Continua a processare le vendite anche quando la connessione internet è persa
- **App Web Progressiva** - Nessun installazione da app store; accesso tramite browser su qualsiasi dispositivo (tablet, computer, terminali dedicati)
- **Sincronizzazione dello stock reale** - Riservazioni di stock (TTL di 15 minuti) prevengono l'eccessivo vendita su canali
- **Supporto per pagamento fratto** - Accetta diversi metodi di pagamento per transazione (contanti + carta + carta regalo)
- **Integrazione del hardware** - Stampa termica ESC/POS, scanner di codici a barre, cassetti per contanti, display per clienti
- **Gestione delle shift** - Conferma del contante con conteggi di apertura/chiusura e tracciamento delle discrepanze
- **Pronto per multi-ubicazione** - Gruppi di negozi con ereditarietà delle impostazioni per la gestione di franchising e regionali

## Edizioni

Il POS è incluso in ogni edizione di Spwig — Community, Pro e Enterprise — a partire da Spwig 1.5.8. Non esiste una licenza POS separata, nessun passo di attivazione e nessun costo per terminale.

**Cosa è incluso in ogni edizione**:
- Registrazioni di terminali illimitate
- Assegnazioni di personale illimitate
- Tutte le funzionalità POS (shift, gestione del contante, personalizzazione delle ricevute, display per clienti)
- Integrazioni con fornitori di pagamento (Stripe Terminal e altri fornitori supportati)
- Supporto per l'integrazione del hardware

I commercianti che gestiscono negozi ospitati da Spwig o che pagano per una licenza Pro/Enterprise ottengono limiti più elevati sui servizi ospitati opzionali di Spwig (GeoIP, geocodificatore, notifiche push) e supporto prioritario, ma l'insieme di funzionalità POS è identico in tutte le edizioni.

## Architettura del sistema

**Frontend** - App Web Progressiva React 18:
- A priorità offline con caching del Service Worker (funziona senza internet)
- Sistema di build Vite per un caricamento rapido
- CSS Modules + token di design (coerenti con il tema del tuo negozio)
- IndexedDB per la persistenza dei dati locali
- 10 lingue supportate (inglese, cinese semplificato/tradizionale, francese, tedesco, spagnolo, portoghese, giapponese, russo, arabo)

**Backend** - Integrazione del backend:
- 13 modelli POS (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, ecc.)
- 43+ endpoint REST API per le operazioni del terminale
- Sistema di riserva dello stock con gestione TTL
- Task Celery per la sincronizzazione in background
- Archiviazione crittografata delle credenziali per i fornitori di pagamento

**Sicurezza**:
- Coppia di terminali tramite codici di 8 caratteri (generati dal server, scadono dopo l'uso)
- Controllo dell'assegnazione del personale che utenti possono accedere a quali terminali
- Capacità di blocco/sblocco remoto per emergenze di amministrazione
- Credenziali crittografate per i fornitori di pagamento
- Autenticazione basata su sessione con supporto per lo sblocco biometrico (dipendente dal browser)

## Flusso di lavoro per iniziare

Segui questi 4 passaggi per distribuire il tuo primo terminale POS.

Per un elenco completo dei passaggi dettagliati, inclusi l'impostazione del personale, i fornitori di pagamento e l'esecuzione della prima vendita, consulta [Getting Started with POS](getting-started-with-pos).

**Passaggio 1: Crea magazzino**
- Vai a **Catalogo > Magazzini**
- Crea un magazzino che rappresenti la tua posizione retail
- Configura l'indirizzo e le informazioni di contatto
- Questo magazzino traccerà l'inventario fisico per le vendite POS

**Passaggio 2: Registra il terminale**
- Vai a **POS > Terminali**
- Fai clic su **+ Aggiungi terminale**
- Imposta il nome del terminale (es. "Cassa principale", "Checkout 1")
- Assegna il magazzino del passaggio 2
- Configura le impostazioni del hardware (stampa, scanner, cassetto per contanti)
- Salva per generare il codice di accoppiamento di 8 caratteri

**Passaggio 3: Assegna il personale**
- Nella configurazione del terminale, scorri fino a **Utenti assegnati**
- Seleziona i membri del personale autorizzati all'uso di questo terminale
- Solo gli utenti assegnati possono accedere al terminale
- Gli utenti devono avere le autorizzazioni POS appropriate nel loro ruolo di personale

**Passaggio 4: Accoppia il dispositivo**
- Sul tuo dispositivo terminale (tablet/personal computer), vai all'URL `/pos/`
- Inserisci il codice di accoppiamento di 8 caratteri dal passaggio 3
- Il terminale scarica la configurazione e sincronizza i dati iniziali
- Accedi con le credenziali del personale assegnato
- Il terminale è pronto per le vendite

Dopo l'accoppiamento, i terminali si sincronizzano automaticamente ogni 5 minuti (configurabile). La modalità offline consente di continuare a operare quando non è disponibile la connessione internet — le vendite si sincronizzano automaticamente quando la connessione torna.

## Funzionalità principali del POS

**Elaborazione delle vendite**:
- Ricerca prodotti per nome, SKU o codice a barre
- Pagamento fratto (più metodi di pagamento per ordine)
- Carrelli parcheggiati (salva transazioni incomplete)
- Rimborsi e annullamenti con tracciamento delle ragioni
- Applicazione di sconti (buoni, carte regalo, promozioni)
- Ricerca clienti e riscossione di punti fedeltà

**Gestione del contante**:
- Apertura di turno con conteggio iniziale del contante
- Chiusura di turno con riconciliazione prevista vs effettiva
- Movimenti di contante (aggiunte di flusso, prelievi di contante di piccola somma con motivazioni)
- Calcolo automatico del contante previsto in base alle vendite in contante
- Tracciamento e reporting delle discrepanze

**Integrazione hardware**:
- Stampa termica ESC/POS (rete o seriale)
- Scanner a codice a barre USB
- Triggers del cassetto per contanti tramite impulso della stampante
- Display per clienti (carosello promozionale durante l'inerzia)
- Lettori di carte Stripe Terminal (S700, WisePOS E, P400)

**Funzionalità offline**:
- Il Service Worker memorizza tutti gli asset del terminale in cache
- IndexedDB memorizza gli ordini recenti (configurabile: 7-30 giorni, 200-1000 ordini)
- Riserve di stock con TTL di 15 minuti impediscono il sovendita
- Coda le vendite per la sincronizzazione quando torna la connessione
- Rilevamento automatico del riconnettersi

## Pagine di amministrazione POS

Accedi a queste pagine di amministrazione per gestire tutti gli aspetti del tuo deployment POS:

**Dashboard POS** (`/admin/pos/`)
- Panoramica del sistema e statistiche rapide
- Attività recenti dei terminali
- Riepilogo dei turni attivi
- Tile di utilizzo dei servizi ospitati (GeoIP, geocodificatore, push — vedi [Spwig Hosted Services](hosted-services))

**Gestione dei terminali** (`/admin/pos_app/posterminal/`)
- Registra e configura i terminali
- Assegna personale e magazzini
- Monitora lo stato online/offline (tracciamento del battito cardiaco)
- Sblocca i terminali da remoto
- [Scopri di più: Gestione dei terminali POS](managing-pos-terminals)

**Gestione dei turni** (`/admin/pos_app/posshift/`)
- Visualizza tutti i turni (aperti, chiusi, storici)
- Esamina i report di riconciliazione del contante
- Traccia i movimenti del contante e le discrepanze
- Audit dell'attività del turno
- [Scopri di più: Turni POS e Gestione del Contante](pos-shifts-cash-management)

**Gruppi di negozi** (`/admin/pos_app/storegroup/`)
- Organizza i terminali per posizione/regione
- Configura le impostazioni a livello di gruppo (valuta, lingua, fuso orario)
- Implementa una gerarchia di ereditarietà delle impostazioni
- [Scopri di più: Gruppi di negozi POS](pos-store-groups)

**Modelli di ricevute** (`/admin/pos_app/receipttemplate/`)
- Personalizza le ricevute stampate (larghezza carta, logo, intestazione/piede di pagina)
- Configura i campi obbligatori (codice fiscale, registrazione aziendale)
- Aggiungi codici QR per promozioni
- Assegna i modelli a specifici negozi o gruppi
- [Ulteriori informazioni: Personalizzazione dei modelli di ricevute](receipt-template-customization)

**Slide promozionali** (`/admin/pos_app/promoslide/`)
- Crea contenuti per il carosello su schermi per clienti
- Assegna le slide a specifici negozi o gruppi
- Pianifica promozioni stagionali
- [Ulteriori informazioni: Slide promozionali per schermi clienti](customer-display-promo-slides)

**Fornitori di pagamento** (`/admin/pos_app/posterminalprovider/`)
- Configura l'integrazione con Stripe Terminal
- Gestisci le credenziali dei fornitori di pagamento
- Monitora lo stato della connessione
- [Ulteriori informazioni: Fornitori di terminali di pagamento](payment-terminal-providers)

**Lettori di carte** (`/admin/pos_app/posterminalreader/`)
- Registra i lettori di carte fisici
- Assegna i lettori ai terminali
- Personalizza le schermate iniziali (branding per lo schermo rivolto ai clienti)
- Monitora lo stato del lettore (online/offline/occupato)
- [Ulteriori informazioni: Gestione dei lettori di carte](card-reader-management)

## Deployment multi-sito

Per i commercianti con più ubicazioni, Spwig POS supporta l'ereditarietà delle impostazioni gerarchiche:

**Gerarchia delle impostazioni** (priorità più alta a priorità più bassa):
1. Impostazioni specifiche del terminale (sovrascrivono tutto)
2. Impostazioni specifiche del negozio (sovrascrivono gruppo e sito)
3. Impostazioni del gruppo (sovrascrivono le impostazioni predefinite del sito)
4. Impostazioni predefinite del sito (impostazioni di fallback per tutti)

Configura le impostazioni condivise a livello di gruppo (es. valuta regionale, lingua) e sovrascrivi quelle necessarie per specifici negozi o terminali. Vedi [Gruppi di negozi POS](pos-store-groups) per le linee guida dettagliate sulla configurazione.

## Consigli

- **Inizia con un singolo terminale** - Testa l'impostazione e il flusso di lavoro del POS con un singolo terminale prima di distribuirlo su tutta la flotta
- **Assegna il magazzino prima di accoppiare** - I terminali non possono processare vendite senza un'assegnazione del magazzino
- **Configura i modelli di ricevute fin dall'inizio** - I campi obbligatori (codici fiscali) variano per regione; configurali prima di andare in live
- **Testa la modalità offline** - Disconnetti l'internet e verifica che le vendite continuino; conferma la sincronizzazione quando riconnesso
- **Utilizza i gruppi di negozi per le ubicazioni multiple** - Semplifica la gestione delle configurazioni per deployment franchising o regionali
- **Monitora lo stato del battito cardiaco** - I terminali pingono il server ogni 5 minuti; i terminali offline appaiono nel dashboard amministrativo
- **Configura i limiti di sincronizzazione per le prestazioni** - I terminali con connessioni lente traggono vantaggio da impostazioni di sync_days/sync_limit più basse
- **Fai un backup della configurazione hardware** - Documenta gli indirizzi IP delle stampanti, le impostazioni degli scanner e la configurazione del cassetto per il recupero in caso di disastro