---
title: Gestione del lettore di carte
---

La gestione dei lettori di carte traccia i dispositivi fisici di hardware per pagamenti, li assegna ai terminali POS e monitora lo stato operativo. Ogni lettore di carte rappresenta un hardware effettivo (Stripe S700, WisePOS E o P400) registrato con il tuo fornitore di pagamento. I lettori hanno una relazione uno-a-uno con i terminali: ogni cassa ha il suo lettore dedicato. Monitora lo stato del lettore (online, offline, busy) in tempo reale, personalizza gli schermi di presentazione con la tua branding e risolvi i problemi di connettività prima che influenzino l'esperienza di checkout dei clienti.

Utilizza la gestione dei lettori di carte per assicurarti che l'hardware di pagamento sia configurato, assegnato e operativo in tutte le ubicazioni.

![Elenco dei lettori di carte](/static/core/admin/img/help/card-reader-management/reader-list.webp)

## Comprendere i lettori di carte

I lettori di carte sono dispositivi fisici che elaborano pagamenti con carte di credito e debito:

**Componenti hardware**:
- Slot per carte a chip EMV
- Antenna NFC (senza contatto/pagamento con tocco)
- Lettore di striscia magnetica (obsoleto, raramente utilizzato)
- Schermo (mostra l'importo, richiede PIN, firma)
- Connessione di rete (Wi-Fi o Ethernet, a seconda del modello)

**Integrazione software**:
- I lettori si connettono all'API Stripe Terminal (basata in cloud, non una connessione diretta al dispositivo POS)
- Il terminale POS richiede un pagamento tramite API
- Stripe indirizza la richiesta al lettore registrato
- Il lettore elabora la carta e restituisce il risultato al POS
- Non è necessaria una connessione USB/Bluetooth tra POS e lettore

**Un lettore per terminale**:
- Ogni terminale POS deve avere esattamente un lettore di carte assegnato
- La relazione uno-a-uno garantisce una responsabilità chiara e un'assistenza più semplice
- Più terminali non possono condividere un lettore (causano conflitti)

## Tipi di lettori di carte

Spwig POS supporta i lettori di carte Stripe Terminal:

**BBPOS WisePOS E** (`bbpos_wisepos_e`):
- Terminale Android tutto-in-uno con schermo a colori da 5"
- Opzione stampante integrata (ricevuta termica)
- Ideale per: Checkout al dettaglio completo, ristoranti (promemoria per mance sullo schermo a colori)
- Connessione: Solo Wi-Fi
- Schermo di presentazione: A colori 480×800 ritratto

**Stripe Reader S700** (`stripe_s700`):
- Lettore da banco con schermo LCD monocromatico
- Design compatto, resistente all'acqua
- Ideale per: Retail standard, contatori di checkout compatte
- Connessione: Wi-Fi o Ethernet
- Schermo di presentazione: Monocromatico 480×800 ritratto

**Verifone P400** (`verifone_p400`):
- Lettore da banco legacy (modello più vecchio)
- Ancora supportato ma non raccomandato per nuove implementazioni
- Ideale per: Implementazioni esistenti (non sostituire l'hardware funzionante)
- Connessione: Wi-Fi o Ethernet
- Schermo di presentazione: Monocromatico 480×800 ritratto

**Compatibilità futura**:
- Potrebbero essere aggiunti altri modelli di lettori man mano che Stripe Terminal espande le offerte hardware
- Il menu a discesa del tipo di lettore si popola automaticamente dalle capacità del fornitore

## Flusso di lavoro per la registrazione del lettore

**Passo 1: Acquisto e ricezione dell'hardware**
- Ordina il lettore da Stripe (stripe.com/terminal) o da un rivenditore autorizzato
- Sblocca e accendi il lettore
- Connettilo alla rete Wi-Fi (segui la procedura di configurazione a schermo del lettore)

**Passo 2: Registrazione nel pannello di controllo Stripe**
- Vai a **Pannello di controllo Stripe > Terminal > Lettori**
- Clicca su **Registra nuovo lettore**
- Segui il processo di accoppiamento a schermo (il lettore visualizza il codice di registrazione)
- Assegna il lettore a una posizione Stripe (deve corrispondere alla posizione nella configurazione del fornitore di pagamento)
- Nota l'**ID del lettore** (sembra `tmr_ABC123...`)

**Passo 3: Sincronizzazione con Spwig (automatica)**
- Spwig individua automaticamente i lettori registrati alla tua posizione Stripe
- Un lavoro in background sincronizza ogni 30 minuti
- I nuovi lettori appaiono nell'elenco **POS > Lettori di carte** entro 30 minuti

**Passo 4: Assegnamento al terminale (manuale)**
- Vai a **POS > Lettori di carte**
- Trova il lettore appena individuato nell'elenco
- Clicca per modificare
- Seleziona **Terminale** per assegnare il lettore
- Salva

**Passo 5: Test del pagamento**
- Al terminale POS, esegui una transazione di test
- Seleziona il metodo di pagamento con carta
- Il POS dovrebbe individuare il lettore assegnato
- Utilizza la carta di test Stripe (4242 4242 4242 4242) per completare il test
- Verifica che il pagamento venga completato con successo

Se il lettore non appare durante il test, controlla l'assegnamento del terminale e lo stato del lettore.

## Monitoraggio dello stato del lettore

I lettori segnalano lo stato all'API Stripe Terminal, che Spwig sincronizza ogni 5 minuti:

**Online** (verde) - Il lettore è acceso, connesso alla rete e pronto ad accettare pagamenti

**Offline** (rosso) - Il lettore è spento, disconnesso dalla rete o irraggiungibile

**Busy** (giallo) - Il lettore sta attualmente elaborando una transazione di pagamento

**Last Seen** - Timestamp dell'ultimo controllo-in del lettore con l'API Stripe
- Aggiornamenti ogni ~2 minuti quando il lettore è online
- Utile per diagnosticare problemi di connettività ("il lettore è andato offline 3 ore fa" = problema di alimentazione o rete durante l'orario di lavoro)

**Casi d'uso dello stato**:
- **Controllo pre-apertura**: Verifica che tutti i lettori della negozio siano online prima di sbloccare le porte
- **Risoluzione dei problemi**: "La cassa 3 non accetta le carte" → Controlla lo stato del lettore → Mostra offline → Controlla alimentazione/rete
- **Audit**: "Le transazioni sono state elaborate al terminale 5 ieri?" → Controlla l'ultimo timestamp di controllo-in

## Assegnamento del terminale

I lettori di carte utilizzano una **relazione uno-a-uno** con i terminali:

**Perché l'assegnamento è importante**:
- Durante il pagamento, il POS deve sapere a quale lettore comunicare
- Più terminali che condividono un lettore causano conflitti (due cassieri non possono usare lo stesso lettore contemporaneamente)
- I lettori non assegnati non saranno utilizzati (hardware orfano)

**Regole per l'assegnamento**:
- Ogni terminale può avere **esattamente un** lettore di carte assegnato
- Ogni lettore di carte può essere assegnato a **esattamente un** terminale
- Assegnare un lettore al terminale A lo disassegna automaticamente dal terminale precedente

**Modifica delle assegnazioni**:
- Modifica il record del lettore
- Cambia il campo **Terminale** in un nuovo terminale
- Salva
- Il terminale precedente perde l'assegnazione del lettore (mostrerà un errore "Nessun lettore assegnato" durante il pagamento)

**Lettori non assegnati**:
- I lettori appena individuati iniziano non assegnati
- I lettori non assegnati appaiono nell'elenco ma non sono utilizzabili
- Assegna a un terminale per attivarli

## Personalizzazione dello schermo di presentazione

Gli schermi di presentazione del lettore mostrano la branding sullo schermo rivolto al cliente quando è inattivo:

**Cosa è lo schermo di presentazione?**
- Immagine visualizzata sullo schermo del lettore quando non sta elaborando un pagamento
- Sostituisce il logo predefinito di Stripe con la tua branding
- Visibile ai clienti mentre attendono il checkout

**Schermo di presentazione automatico vs personalizzato**:

**Schermo di presentazione automatico** (predefinito):
- Spwig genera lo schermo di presentazione dal logo del tuo negozio (se il logo è configurato nelle impostazioni del negozio)
- Dimensioni automaticamente alle specifiche del lettore (480×800 ritratto)
- Monocromatico per S700/P400, a colori per WisePOS E
- Nessuna configurazione necessaria

**Schermo di presentazione personalizzato** (avanzato):
- Carica la tua immagine progettata personalmente per lo schermo di presentazione
- Controllo completo del design e della branding
- Deve soddisfare i requisiti dell'immagine (vedi di seguito)

**Requisiti per lo schermo di presentazione personalizzato**:
- **Risoluzione**: Esattamente 480×800 pixel (orientamento ritratto)
- **Formato**: PNG o JPG
- **S700/P400**: Solo monocromatico (nero e bianco, nessun grigio)
- **WisePOS E**: Supporta i colori completi
- **Dimensione del file**: <200KB

**Impostazione dello schermo di presentazione personalizzato**:
1. Modifica il record del lettore di carte
2. Carica l'immagine nel campo **Immagine di sovrascrittura dello schermo di presentazione** (o selezionala dalla Libreria Media)
3. Salva
4. Lo schermo di presentazione viene sincronizzato con il lettore entro 5 minuti

**Rimozione dello schermo di presentazione personalizzato**:
- Cancella il campo **Immagine di sovrascrittura dello schermo di presentazione**
- Salva
- Il lettore torna allo schermo di presentazione automatico (o al predefinito di Stripe se non è presente un logo del negozio)

**Test dello schermo di presentazione**:
- Dopo il caricamento, attendi 5 minuti per la sincronizzazione
- Visita il dispositivo del lettore
- Verifica che lo schermo di presentazione appaia sullo schermo inattivo
- Controlla la qualità dell'immagine, il centraggio e il contrasto

## Configurazione dello schermo di presentazione di Stripe

Dietro le quinte, Spwig gestisce la configurazione dello schermo di presentazione di Stripe Terminal:

**stripe_splash_file_id** - ID interno di Stripe per il file dell'immagine dello schermo di presentazione caricato
- Impostato automaticamente quando lo schermo di presentazione viene caricato
- Utilizzato per fare riferimento allo schermo di presentazione nell'API Stripe

**stripe_splash_config_id** - ID interno di Stripe per la configurazione dello schermo di presentazione
- Collega il file dello schermo al lettore
- Gestito automaticamente quando si assegna lo schermo di presentazione al lettore

Questi campi sono di sola lettura e vengono gestiti automaticamente: non è necessario interagire con essi direttamente.

## Risoluzione dei problemi comuni

**Problema 1: Il lettore mostra offline ma è acceso**
- **Causa**: Problema di connettività di rete, password Wi-Fi cambiata, lettore fuori portata
- **Soluzione**: Controlla le impostazioni di rete del lettore, riconnettilo alla rete Wi-Fi, verifica che l'API Stripe sia raggiungibile dalla rete

**Problema 2: Il POS dice "Nessun lettore assegnato" durante il pagamento**
- **Causa**: Il lettore non è assegnato al terminale o l'assegnamento non è completo
- **Soluzione**: Modifica il lettore, assegna al terminale, salva, riprova il pagamento

**Problema 3: Il lettore è bloccato in stato busy (bloccato nello schermo di pagamento)**
- **Causa**: Transazione scaduta o crashata, stato del lettore non reimpostato
- **Soluzione**: Riavvia il lettore (ciclo di alimentazione), contatta il supporto Stripe se persiste

**Problema 4: Lo schermo di presentazione personalizzato non appare**
- **Causa**: Immagine con risoluzione errata, non sincronizzata ancora, requisito monocromatico non soddisfatto (S700/P400)
- **Soluzione**: Verifica che l'immagine sia esattamente 480×800, attendi 5 minuti per la sincronizzazione, assicurati che sia monocromatico per i lettori non a colori

**Problema 5: Il lettore è registrato in Stripe ma non appare in Spwig**
- **Causa**: Il lettore è registrato in una posizione Stripe diversa da quella della configurazione del fornitore
- **Soluzione**: Nel pannello di controllo Stripe, verifica che la posizione del lettore corrisponda all'ID della posizione del fornitore

## Consigli

- **Un lettore per terminale** - Non condividere i lettori tra i terminali; previene conflitti e semplifica la responsabilità
- **Registra i lettori prima di deployarli** - Completa la registrazione in Stripe e l'assegnazione in Spwig prima di posizionare il lettore al checkout
- **Testa gli schermi di presentazione in negozio** - Il contrasto varia per modello di lettore e illuminazione; verifica che lo schermo appaia bene nell'ambiente reale
- **Monitora lo stato prima dell'apertura** - Controlla l'elenco dei lettori ogni mattina per assicurarti che tutti i lettori siano online prima che il negozio apra
- **Etichetta l'hardware fisicamente** - Utilizza un etichettatore per contrassegnare il lettore con il nome del terminale ("Lettore della cassa 1") per un'identificazione facile durante la risoluzione dei problemi
- **Mantieni i lettori con alimentazione ininterrotta** - Le interruzioni di corrente durante una transazione possono corrompere lo stato del lettore; raccomandato l'UPS
- **Documenta i numeri di serie dei lettori** - Mantieni un registro dei numeri di serie per garanzia e supporto (trovati sull'etichetta hardware del lettore)
- **Aggiorna il firmware dei lettori** - Stripe invia automaticamente gli aggiornamenti del firmware, ma verifica periodicamente che i lettori siano aggiornati alla versione più recente (controlla il pannello di controllo Stripe)