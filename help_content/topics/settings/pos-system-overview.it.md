---
title: Panoramica del sistema POS
---

Il sistema POS di Spwig trasforma il tuo negozio in una soluzione completa per il retail con terminali di punto di vendita moderni. Distribuisci un numero illimitato di terminali in un numero illimitato di ubicazioni con un costo di licenza fisso di €499/anno. Ogni terminale è un'app Web Progressiva (PWA) che funziona offline, sincronizza automaticamente e si integra perfettamente con il tuo inventario, i dati dei clienti e il processo di pagamento. Gestisci tutto dal dashboard di amministrazione: configurazione del terminale, conciliazione degli orari di lavoro, personalizzazione delle ricevute e integrazione del hardware.

Utilizza il sistema POS quando hai ubicazioni fisiche, negozi pop-up, fiere commerciali o qualsiasi ambiente in cui i clienti effettuano acquisti di persona invece che online.

![Dashboard POS](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## Cosa è Spwig POS?

Spwig POS è un sistema di punto di vendita completamente integrato progettato per i commercianti che vendono sia online che in ubicazioni fisiche. A differenza dei sistemi POS di terze parti che richiedono integrazioni complesse, Spwig POS è costruito direttamente nel tuo piattaforma, assicurando una perfetta sincronizzazione dei dati in tutti i canali di vendita.

**Caratteristiche principali**:
- **Terminali illimitati** - Distribuisci tanti terminali quanti necessari senza costi aggiuntivi
- **Architettura a priorità offline** - Continua a processare le vendite anche quando la connessione internet è persa
- **App Web Progressiva** - Nessun installazione da app store; accesso tramite browser su qualsiasi dispositivo (tablet, computer, terminali dedicati)
- **Sincronizzazione dello stock reale** - Riserve di stock (TTL di 15 minuti) impediscono la vendita eccessiva in tutti i canali
- **Supporto per pagamento fratto** - Accetta diversi metodi di pagamento per transazione (contanti + carta + carta regalo)
- **Integrazione del hardware** - Stampa termica ESC/POS, scanner di codici a barre, cassetto per contanti, display per clienti
- **Gestione degli orari di lavoro** - Conciliazione del contante con conteggi di apertura/chiusura e tracciamento delle discrepanze
- **Pronto per multi-ubicazione** - Gruppi di negozi con ereditarietà delle impostazioni per la gestione di franchising e regionali

## Licenza e Attivazione

**Prezzo a tariffa piatta**: €499 all'anno copre terminali illimitati in ubicazioni illimitate. Nessun costo per terminale, nessuna tariffa per transazione, nessun costo nascosto.

**Formato della licenza**: `POS-XXXX-XXXX-XXXX-XXXX` (fornito dopo l'acquisto)

**Attivazione**: Inserisci la tua chiave di licenza in **Impostazioni > Licenza POS**. Il sistema si verifica con il server di licenza di Spwig e attiva immediatamente tutte le funzionalità POS. Le licenze includono un periodo di grazia di 14 giorni dopo la scadenza per permettere ritardi nel pagamento.

**Cosa ricevi**:
- Registrazioni di terminali illimitate
- Assegnamenti di personale illimitati
- Tutte le funzionalità POS (orari di lavoro, gestione del contante, personalizzazione delle ricevute, display per clienti)
- Integrazioni con i fornitori di pagamento (Stripe Terminal e sistema estensibile dei fornitori)
- Supporto per l'integrazione del hardware
- Aggiornamenti e correzioni di bug durante il periodo di licenza

Nessuna funzionalità POS è accessibile senza una licenza valida—l'interfaccia di accoppiamento dei terminali, la gestione degli orari di lavoro e le pagine di amministrazione POS richiedono l'attivazione.

## Architettura del sistema

**Frontend** - App Web Progressiva React 18:
- A priorità offline con caching tramite Service Worker (funziona senza internet)
- Sistema di build Vite per caricamento rapido
- CSS Modules + token di design (coerenti con il tema del tuo negozio)
- IndexedDB per la persistenza dei dati locali
- 10 lingue supportate (inglese, cinese semplificato/tradizionale, francese, tedesco, spagnolo, portoghese, giapponese, russo, arabo)

**Backend** - Integrazione Backend:
- 13 modelli POS (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, ecc.)
- 43+ endpoint API REST per le operazioni sui terminali
- Sistema di riserva dello stock con gestione TTL
- Task Celery per la sincronizzazione in background
- Archiviazione crittografata delle credenziali per i fornitori di pagamento

**Sicurezza**:
- Accoppiamento dei terminali tramite codici di 8 caratteri (generati lato server, scadono dopo l'uso)
- Controllo dell'assegnamento del personale che utenti possono accedere a quali terminali
- Capacità di blocco/sblocco remoto per emergenze di amministrazione
- Credenziali crittografate per i fornitori di pagamento
- Autenticazione basata su sessione con supporto per lo sblocco biometrico (dipende dal browser)

## Flusso di lavoro per l'avvio

Segui questi 5 passaggi per distribuire il tuo primo terminale POS:

**Passaggio 1: Attivare la licenza POS**
- Naviga su **Impostazioni > Licenza POS**
- Inserisci la tua chiave di licenza (`POS-XXXX-XXXX-XXXX-XXXX`)
- Convalida la licenza (richiede una connessione internet)
- Conferma l'attivazione

**Passaggio 2: Creare un magazzino**
- Naviga su **Catalogo > Magazzini**
- Crea un magazzino che rappresenta la tua ubicazione retail
- Configura l'indirizzo e le informazioni di contatto
- Questo magazzino traccerà lo stock fisico per le vendite POS

**Passaggio 3: Registrare il terminale**
- Naviga su **POS > Terminali**
- Clicca su **+ Aggiungi terminale**
- Imposta il nome del terminale (es. "Cassa principale", "Checkout 1")
- Assegna il magazzino dal passaggio 2
- Configura le impostazioni del hardware (stampa, scanner, cassetto per contanti)
- Salva per generare il codice di accoppiamento di 8 caratteri

**Passaggio 4: Assegnare il personale**
- Nella configurazione del terminale, scorri fino a **Utenti assegnati**
- Seleziona i membri dello staff autorizzati all'uso di questo terminale
- Solo gli utenti assegnati possono accedere al terminale
- Gli utenti devono avere le autorizzazioni POS appropriate nel loro ruolo di staff

**Passaggio 5: Accoppiare il dispositivo**
- Sul tuo dispositivo terminale (tablet/computer), naviga all'URL `/pos/`
- Inserisci il codice di accoppiamento di 8 caratteri dal passaggio 3
- Il terminale scarica la configurazione e sincronizza i dati iniziali
- Accedi con le credenziali dello staff assegnato
- Il terminale è pronto per le vendite

Dopo l'accoppiamento, i terminali si sincronizzano automaticamente ogni 5 minuti (configurabile). La modalità offline permette l'operazione continua quando l'internet non è disponibile—le vendite si sincronizzano automaticamente quando la connettività torna.

## Funzionalità principali POS

**Elaborazione delle vendite**:
- Ricerca prodotti per nome, SKU o codice a barre
- Pagamento fratto (più metodi di pagamento per ordine)
- Carrelli parcheggiati (salva transazioni incomplete)
- Rimborsi e annullamenti con tracciamento delle ragioni
- Applicazione di sconti (buoni, carte regalo, promozioni)
- Ricerca clienti e riscossione di punti fedeltà

**Gestione del contante**:
- Apertura di orario con conteggio iniziale del contante
- Chiusura di orario con conciliazione prevista vs effettiva
- Movimenti del contante (aggiunte di flusso, prelievi di cassa piccola con motivazioni)
- Calcolo automatico del contante previsto in base alle vendite in contante
- Tracciamento e reporting delle discrepanze

**Integrazione del hardware**:
- Stampa termica ESC/POS (rete o seriale)
- Scanner di codici a barre USB
- Triggers del cassetto per contanti tramite impulso della stampante
- Display rivolti ai clienti (carosello promozionale durante l'inerzia)
- Lettori di carte Stripe Terminal (S700, WisePOS E, P400)

**Capacità offline**:
- Service Worker cache tutti gli asset del terminale
- IndexedDB memorizza gli ordini recenti (configurabile: 7-30 giorni, 200-1000 ordini)
- Riserve di stock con TTL di 15 minuti impediscono la vendita eccessiva
- Coda le vendite per la sincronizzazione quando la connettività torna
- Rilevamento automatico del riconnessione

## Pagine di amministrazione POS

Accedi a queste pagine di amministrazione per gestire tutti gli aspetti del tuo deployment POS:

**Dashboard POS** (`/admin/pos/`)
- Panoramica del sistema e statistiche rapide
- Attività recenti dei terminali
- Riepilogo degli orari di lavoro attivi
- Stato della licenza e data di scadenza

**Gestione dei terminali** (`/admin/pos_app/posterminal/`)
- Registra e configura i terminali
- Assegna personale e magazzini
- Monitora lo stato online/offline (tracciamento del battito cardiaco)
- Sblocca i terminali da remoto
- [Scopri di più: Gestione dei terminali POS](managing-pos-terminals)

**Gestione degli orari di lavoro** (`/admin/pos_app/posshift/`)
- Visualizza tutti gli orari di lavoro (aperti, chiusi, storici)
- Esamina i report di conciliazione del contante
- Traccia i movimenti del contante e le discrepanze
- Audit dell'attività degli orari di lavoro
- [Scopri di più: Orari di lavoro POS e gestione del contante](pos-shifts-cash-management)

**Gruppi di negozi** (`/admin/pos_app/storegroup/`)
- Organizza i terminali per ubicazione/regione
- Configura le impostazioni a livello di gruppo (valuta, lingua, fuso orario)
- Implementa una gerarchia di ereditarietà delle impostazioni
- [Scopri di più: Gruppi di negozi POS](pos-store-groups)

**Modelli di ricevute** (`/admin/pos_app/receipttemplate/`)
- Personalizza le ricevute stampate (larghezza della carta, logo, intestazione/piede di pagina)
- Configura i campi di conformità (ID fiscale, registrazione aziendale)
- Aggiungi codici QR per le promozioni
- Limita i modelli a specifici negozi o gruppi
- [Scopri di più: Personalizzazione dei modelli di ricevuta](receipt-template-customization)

**Scorrimenti promozionali** (`/admin/pos_app/promoslide/`)
- Crea contenuti per il carosello del display per clienti
- Targetizza gli scorrimenti a specifici negozi o gruppi
- Pianifica promozioni stagionali
- [Scopri di più: Scorrimenti promozionali per display clienti](customer-display-promo-slides)

**Fornitori di pagamento** (`/admin/pos_app/posterminalprovider/`)
- Configura l'integrazione con Stripe Terminal
- Gestisci le credenziali dei fornitori di pagamento
- Monitora lo stato della connessione
- [Scopri di più: Fornitori di terminali di pagamento](payment-terminal-providers)

**Lettori di carte** (`/admin/pos_app/posterminalreader/`)
- Registra i lettori di carte fisici
- Assegna i lettori ai terminali
- Personalizza le schermate di avvio (branding del display per clienti)
- Monitora lo stato del lettore (online/offline/occupato)
- [Scopri di più: Gestione dei lettori di carte](card-reader-management)

## Deployment multi-ubicazione

Per i commercianti con più ubicazioni retail, Spwig POS supporta l'ereditarietà gerarchica delle impostazioni:

**Gerarchia delle impostazioni** (priorità più alta a più bassa):
1. Impostazioni specifiche del terminale (sovrascrivono tutto)
2. Impostazioni specifiche del negozio (sovrascrivono gruppo e sito)
3. Impostazioni del gruppo (sovrascrivono le impostazioni predefinite del sito)
4. Impostazioni predefinite del sito (fallback per tutto)

Configura le impostazioni condivise a livello di gruppo (es. valuta regionale, lingua) e sovrascrivi quando necessario per specifici negozi o terminali. Vedi [Gruppi di negozi POS](pos-store-groups) per le linee guida dettagliate per la configurazione.

## Consigli

- **Inizia con un singolo terminale** - Testa la configurazione POS e il flusso di lavoro con un singolo terminale prima di distribuirlo in massa
- **Assegna il magazzino prima dell'accoppiamento** - I terminali non possono processare le vendite senza un'assegnazione del magazzino
- **Configura i modelli di ricevuta in anticipo** - I campi di conformità (ID fiscale) variano per regione; configurali prima di andare online
- **Testa la modalità offline** - Disconnetti l'internet e verifica che le vendite continuino; conferma la sincronizzazione quando riconnesso
- **Utilizza i gruppi di negozi per multi-ubicazione** - Semplifica la gestione delle configurazioni per deployment di franchising o regionali
- **Monitora lo stato del battito cardiaco** - I terminali pingono il server ogni 5 minuti; i terminali offline appaiono nel dashboard di amministrazione
- **Configura i limiti di sincronizzazione per le prestazioni** - I terminali con connessioni lente beneficiano di impostazioni più basse per sync_days/sync_limit
- **Fai un backup della configurazione del hardware** - Documenta gli IP delle stampanti, le impostazioni degli scanner, la configurazione del cassetto per contanti per il recupero in caso di disastro

Ricorda: Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.