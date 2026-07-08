---
title: Preferenze di Comunicazione
---

Le preferenze di comunicazione consentono ai clienti di controllare quali email e messaggi SMS ricevono dal tuo negozio. Questo sistema garantisce la conformità al GDPR e ti aiuta a rispettare le preferenze di comunicazione dei clienti in tutti i canali.

Naviga verso **Customers > Communication Preferences** nel menu laterale di amministrazione per gestire le preferenze di comunicazione dei clienti.

## Comprendere le Preferenze di Comunicazione

Il sistema delle preferenze di comunicazione dà ai clienti un controllo dettagliato sui messaggi che ricevono. Questo include:

- **Email transazionali** — Conferma dell'ordine, aggiornamenti di spedizione, email di sicurezza dell'account (sempre attive)
- **Email di marketing** — Newsletter, promozioni, suggerimenti di prodotti (richiede l'iscrizione)
- **Notifiche specifiche dell'app** — Post del blog, punti fedeltà, premi di reclutamento, commissioni affiliati
- **Notifiche SMS** — Notifiche tramite messaggio di testo (richiede un'iscrizione esplicita per TCPA)

Tutte le comunicazioni di marketing richiedono il consenso del cliente e la verifica dell'indirizzo email per garantire la conformità al GDPR.

## Spiegazione dei Tipi di Preferenze

### Comunicazioni Transazionali (Sempre Abilitate)

Le comunicazioni transazionali sono essenziali per l'account e gli ordini del cliente. Queste **non possono essere disattivate** dai clienti:

| Tipo | Descrizione | Esempi |
|------|-------------|----------|
| **Conferma Ordine** | Conferma quando l'ordine è stato effettuato | L'ordine #12345 è stato ricevuto |
| **Aggiornamenti di Spedizione** | Notifiche quando lo stato dell'ordine cambia | Il tuo ordine è stato spedito |
| **Conferma di Pagamento** | Pagamento ricevuto, rimborso processato | Pagamento di $49.99 confermato |
| **Sicurezza dell'Account** | Reimpostazione della password, verifica email | Reimposta la password |

### Comunicazioni di Marketing (Richiesta di Iscrizione)

Le comunicazioni di marketing richiedono il consenso del cliente e la verifica dell'indirizzo email:

| Tipo | Descrizione | Default |
|------|-------------|---------|
| **Newsletter** | Newsletter e aggiornamenti generali | Opt-out |
| **Offerte Promozionali** | Vendite, sconti, offerte speciali | Opt-out |
| **Suggerimenti di Prodotti** | Suggerimenti personalizzati di prodotti | Opt-out |
| **Torna in Magazzino** | Notifiche quando i prodotti tornano in magazzino | Opt-out |

I clienti devono **verificare il loro indirizzo email** prima di ricevere qualsiasi email di marketing (richiesta di doppia iscrizione per il GDPR).

### Preferenze Specifiche dell'App

I clienti possono controllare le notifiche da funzionalità specifiche:

**Notifiche del Blog**
- Nuovo post del blog pubblicato (immediato, digest settimanale o mensile)
- Sottoscrizioni specifiche per la categoria
- Preferenze di frequenza

**Programma Fedeltà**
- Notifiche sui punti guadagnati
- Aggiornamenti del livello
- Premi sbloccati
- Punti che scadranno presto
- Bonus di compleanno
- Offerte di campagna

**Programma di Reclutamento**
- Premio assegnato (reclutatore e reclutato)
- Registrazione riuscita del reclutato
- Premio che scadrà presto
- Inviti al reclutamento

**Programma Affiliato**
- Commissioni guadagnate
- Commissioni approvate o rifiutate
- Pagamento processato, completato o fallito
- Rapporti di prestazioni mensili

### Notifiche SMS (Richiesta di Iscrizione Esplicita)

Tutte le notifiche SMS richiedono **un'iscrizione esplicita** in base alle regolamentazioni TCPA. I clienti devono attivamente selezionare la casella di iscrizione SMS:

- **SMS transazionali** — Ordine spedito, consegnato (richiede iscrizione)
- **SMS di marketing** — Promozioni, offerte speciali (richiede iscrizione separata)

Anche gli SMS transazionali richiedono l'iscrizione perché l'invio di messaggi di testo non richiesti è regolamentato in modo più rigoroso rispetto alle email.

## Gestione delle Preferenze dei Clienti nell'Amministrazione

### Visualizzare Tutte le Preferenze

Naviga verso **Customers > Communication Preferences** per visualizzare tutte le preferenze dei clienti:

| Colonna | Descrizione |
|--------|-------------|
| **Email dell'Utente** | Indirizzo email del cliente (collega all'amministrazione utente) |
| **Stato Email** | ✓ verde se le email sono abilitate, ○ grigio se disabilitate |
| **Stato SMS** | ✓ verde se gli SMS sono abilitati, ○ grigio se disabilitati |
| **Stato Marketing** | Etichetta "Opted In" o "Opted Out" |
| **Stato di Verifica** | 📧✓ se l'email è verificata, 📱✓ se l'SMS è verificato |
| **Fonte del Consenso** | Dove il cliente ha dato il consenso (registrazione, checkout, centro preferenze) |
| **Aggiornato a** | Ultimo momento in cui le preferenze sono state modificate |

### Filtrare le Preferenze

Utilizza il pannello laterale di filtro per trovare clienti:

- **Email Abilitata** — Sì/No
- **SMS Abilitata** — Sì/No
- **Email Marketing** — Sì/No (iscritto al marketing)
- **SMS Marketing** — Sì/No (iscritto al marketing SMS)
- **Email Verificata** — Sì/No (ha verificato l'indirizzo email)
- **SMS Verificata** — Sì/No (ha verificato il numero di telefono)
- **Fonte del Consenso** — Registrazione, Checkout, Centro Preferenze, API, Migrato
- **Codice Lingua** — Lingua preferita per le comunicazioni

### Cercare le Preferenze

Cerca i clienti per:
- Email dell'utente
- Nome utente
- Nome
- Cognome
- Token di annullamento

### Azioni di Gruppo

Seleziona diversi clienti e applica azioni di gruppo:

**✓ Marca l'Email come Verificata**
- Verifica manualmente gli indirizzi email dei clienti
- Utile quando si importano clienti da un altro sistema
- Invalida la cache delle preferenze per applicare immediatamente i cambiamenti

**🚫 Annulla l'iscrizione a Tutto il Marketing**
- Disattiva tutte le comunicazioni di marketing (email, SMS, tutte le app)
- Mantieni le email transazionali abilitate
- Usa questa opzione per i clienti che richiedono di essere completamente annullati
- Rispetta il diritto di ritirare il consenso del GDPR

**📥 Esporta le Preferenze in CSV**
- Esporta le preferenze dei clienti in un foglio di calcolo
- Include tutti i campi delle preferenze e le impostazioni specifiche delle app
- Utile per audit di conformità e analisi
- Formato: CSV con intestazioni

## Centro delle Preferenze Self-Service del Cliente

I clienti possono gestire le loro preferenze da `/accounts/preferences/` quando sono connessi.

### Funzionalità del Centro delle Preferenze

**Azioni Veloci**
- **Iscriviti a Tutto il Marketing** — Abilita tutte le comunicazioni di marketing con un clic
- **Annulla l'iscrizione a Tutto** — Disattiva tutte le comunicazioni di marketing (le comunicazioni transazionali rimangono abilitate)

**Carte delle Preferenze**
- **Email Transazionali** — Solo lettura (sempre abilitate, contrassegnate come "Obbligatorio")
- **Comunicazioni di Marketing** — Attiva/Disattiva con etichetta di verifica
- **Preferenze del Blog** — Abilita/Disabilita, seleziona frequenza (immediata, settimanale, mensile)
- **Programma Fedeltà** — Abilita/Disabilita tipi specifici di notifiche
- **Programma di Reclutamento** — Abilita/Disabilita notifiche sui premi
- **Programma Affiliato** — Abilita/Disabilita notifiche sulle commissioni e i pagamenti
- **Notifiche SMS** — Iscriviti/Annulla l'iscrizione agli SMS (mostra lo stato di verifica)

**Aggiornamenti in Tempo Reale**
- I cambiamenti vengono salvati immediatamente tramite AJAX
- Non è necessario un rinfresco della pagina
- Feedback visivo quando sono stati salvati

### Procedura di Verifica Email

Quando un cliente abilita le email di marketing:

1. Il cliente attiva "Email di Marketing" su ON
2. Il sistema invia un'email di verifica con un link unico
3. Il cliente clicca sul link di verifica
4. L'email viene contrassegnata come verificata (compare l'etichetta 📧✓)
5. Le email di marketing saranno ora inviate

**I clienti non verificati NON riceveranno email di marketing** anche se l'interruttore è su ON. Questo garantisce la conformità alla doppia iscrizione del GDPR.

## Annullamento Istantaneo

Tutte le email di marketing includono un link per annullare l'iscrizione nel piè di pagina. Cliccando su questo link:

1. Porta il cliente a `/accounts/unsubscribe/<token>/` (nessun login richiesto)
2. Mostra da cosa si sta annullando l'iscrizione
3. Permette un feedback opzionale (motivo dell'annullamento)
4. Disattiva le comunicazioni di marketing
5. Mantieni le email transazionali abilitate
6. Fornisce un link al centro completo delle preferenze

I clienti possono riascriversi in qualsiasi momento tramite il centro delle preferenze.

## Conformità e Requisiti Legali

### Conformità all'Articolo 7 del GDPR

Il sistema garantisce la conformità completa all'Articolo 7 del GDPR:

**✅ Prova del Consenso**
- Orario in cui è stato dato il consenso
- Fonte del consenso (registrazione, checkout, centro preferenze)
- Indirizzo IP del consenso
- User agent (informazioni del browser)

**✅ Consenso Separato**
- Email di marketing e transazionali sono interruttori separati
- Ogni app (blog, fedeltà, ecc.) richiede un consenso individuale

**✅ Ritiro Facile**
- Annullamento istantaneo in tutte le email di marketing
- Centro delle preferenze disponibile per tutti i clienti connessi
- L'annullamento ha effetto immediato

**✅ Consenso Libero**
- Default è opt-out per il marketing (migliore pratica GDPR)
- Nessuna casella pre-selezionata (i clienti devono attivamente iscriversi)

**✅ Consenso Specifico e Informato**
- Descrizione chiara di cosa ogni preferenza controlla
- Preferenze dettagliate a livello di app (non tutto o niente)

**✅ Consenso Verificabile**
- Doppia iscrizione per email di marketing
- Tracciamento dell'audit tramite lo stato EmailOutbox

### Conformità TCPA (Regolamentazioni SMS USA)

Tutte le notifiche SMS richiedono **un'iscrizione esplicita**:

- I clienti devono attivamente selezionare la casella di iscrizione SMS
- Non sono ammesse caselle pre-selezionate
- Descrizione chiara di cosa stanno iscrivendosi
- Annullamento facile tramite il centro delle preferenze
- Tutte le spedizioni SMS sono registrate per l'audit di conformità

### Conformità CAN-SPAM (Regolamentazioni Email USA)

Il sistema garantisce la conformità CAN-SPAM:

- Link per annullare l'iscrizione in ogni email di marketing
- Annullamento processato immediatamente (richiesto entro 10 giorni lavorativi, lo facciamo istantaneamente)
- Nome "Da" chiaro (il nome del tuo negozio)
- Indirizzo fisico nel piè di pagina email
- Nessun titolo ingannevole

## Comprendere lo Stato Email in EmailOutbox

Quando si visualizza **Email System > Email Outbox**, si vedrà come le preferenze influenzano la consegna delle email:

| Stato | Significato | Motivo |
|--------|---------|--------|
| **In Attesa** | Email in coda per l'invio | Le preferenze permettono l'invio di questa email |
| **In Coda** | In coda per l'invio | Le preferenze permettono l'invio di questa email |
| **Saltata** | Email non inviata | Le preferenze del cliente sono disattivate |
| **Inviata** | Consegnata con successo | Email inviata normalmente |

Quando un'email è **saltata**, il campo `skip_reason` mostra il motivo:

- **user_preference_disabled** — Il cliente ha disattivato questo tipo di email nelle preferenze
- **email_not_verified** — Il cliente non ha verificato il proprio indirizzo email
- **email_disabled** — Il cliente ha disattivato tutte le email (interruttore principale)

Questo tracciamento dell'audit è importante per la conformità al GDPR — puoi dimostrare di aver rispettato le preferenze del cliente.

## Impostazioni del Sito per le Preferenze

Naviga verso **Settings > Site Settings** per configurare le impostazioni globali delle preferenze:

**Abilita Doppia Iscrizione per Email di Marketing** (Default: Sì)
- Richiede la verifica dell'indirizzo email prima di inviare email di marketing
- Migliore pratica del GDPR
- Consigliato: Mantieni abilitato

**Stato Predefinito per l'Iscrizione al Marketing** (Default: No - Opt-Out)
- Stato predefinito quando i nuovi clienti si registrano
- Il GDPR richiede l'opt-out predefinito
- Consigliato: Mantieni come opt-out (False)

**Centro delle Preferenze Abilitato** (Default: Sì)
- Permette ai clienti di gestire le proprie preferenze
- Richiesto per il diritto di ritirare il consenso del GDPR
- Consigliato: Mantieni abilitato

**Richiedi Verifica SMS** (Default: No)
- Richiedi la verifica del numero di telefono per le notifiche SMS
- Opzionale ma consigliato per i mittenti di SMS ad alto volume
- Può essere abilitato se si desidera una doppia iscrizione per SMS

**Mostra Motivi di Annullamento** (Default: Sì)
- Raccogli un feedback opzionale quando i clienti si annullano
- Aiuta a comprendere il motivo per cui i clienti si annullano
- Consigliato: Mantieni abilitato per ottenere informazioni

## Migliori Pratiche

### 1. Default a Opt-Out per Marketing

Imponi sempre il marketing a **opt-out** (non selezionato):
- Conforme al GDPR
- Costruisce fiducia con i clienti
- Riduce le lamentele per spam
- Invia solo a clienti attivi

### 2. Richiedi Verifica Email

Mantieni **Doppia Iscrizione** abilitata:
- Garantisce che gli indirizzi email siano validi
- Conferma che i clienti desiderano effettivamente ricevere email di marketing
- Riduce il tasso di rimbalzo
- Richiesto per la conformità al GDPR

### 3. Rispetta le Preferenze Immediatamente

Quando un cliente modifica le preferenze:
- Le modifiche entrano in vigore immediatamente
- La cache delle preferenze viene invalidata
- L'invio successivo delle email controllerà le preferenze aggiornate
- Nessun ritardo nell'adempimento delle richieste di annullamento

### 4. Monitora le Email Saltate

Controlla regolarmente **Email Outbox** per le email saltate:
- Un alto tasso di email saltate indica che i clienti si annullano
- Potrebbe segnalare che il contenuto delle email necessita di miglioramento
- Aiuta a identificare problemi di preferenza

### 5. Audit di Conformità Regolari

Esporta le preferenze periodicamente per la conformità:
1. Naviga verso **Communication Preferences**
2. Seleziona tutti i clienti
3. Scegli **Export Preferences to CSV**
4. Salva per l'audit trail del GDPR

Archivia le esportazioni per **almeno 3 anni** per rispettare i requisiti di conservazione dei dati del GDPR.

### 6. Comunicazione Chiara

Quando si raccoglie il consenso:
- Usa un linguaggio semplice, non gergo legale
- Spiega cosa riceveranno i clienti
- Mostra la frequenza (giornaliera, settimanale, mensile)
- Rende le caselle di iscrizione prominenti ma non pre-selezionate

### 7. Segmenta per Preferenze

Quando si inviano campagne di marketing:
- Invia solo a clienti verificati e iscritti
- Rispetta le preferenze specifiche delle app (non inviare email del blog a clienti che hanno disattivato il blog)
- Usa le preferenze di frequenza (non inviare email immediate a clienti che ricevono digest settimanali)

## Siti Utili

**💡 Controlla le Preferenze Prima di Inviare**

Il sistema controlla automaticamente le preferenze quando invii email utilizzando `EmailSendingService.send_template_email()`. Assicurati che tutte le email utilizzino questo servizio, non chiamate SMTP dirette.

**💡 Lo Stato Saltato è Normale**

Non preoccuparti per le email saltate nell'outbox — ciò significa che il sistema sta funzionando correttamente e rispetta le preferenze dei clienti. È meglio saltare le email non richieste che rischiare sanzioni del GDPR o lamentele per spam.

**💡 Cache delle Preferenze a 5 Minuti**

I controlli delle preferenze sono memorizzati per 5 minuti per le prestazioni. Quando i clienti modificano le preferenze tramite il centro delle preferenze o azioni di amministrazione, la cache viene immediatamente invalidata in modo che le modifiche abbiano effetto subito.

**💡 I Clienti Guest Saltano i Controlli**

I clienti che effettuano il checkout come ospiti (nessun account) riceveranno tutte le email normalmente poiché non hanno un record di preferenze. Questo è intenzionale — si sono iscritti fornendo il loro indirizzo email al checkout.

**💡 Email Transazionali Inviate Sempre**

Le conferme degli ordini, gli aggiornamenti di spedizione e le email di sicurezza dell'account **vengono sempre inviate** indipendentemente dalle preferenze. Questo garantisce che i clienti ricevano informazioni critiche sui loro ordini e account.

**💡 Usa le Azioni di Gruppo con Cura**

L'azione di gruppo "Annulla l'iscrizione a Tutto il Marketing" influisce su **tutte le app** (blog, fedeltà, reclutamento, affiliato). Usa questa solo per i clienti che hanno richiesto esplicitamente di essere completamente annullati. Per preferenze specifiche, modifica i record dei clienti singolarmente.

**💡 Tracciamento dell'Audit per la Conformità**

Il sistema traccia:
- Orario e fonte del consenso
- Indirizzo IP e user agent
- Orario di verifica dell'email
- Ogni modifica delle preferenze tramite lo stato EmailOutbox saltato

Questo tracciamento dell'audit dimostra la conformità al GDPR se le autorità richiedono prove del consenso.

## Argomenti Correlati

- [Gestione Account Cliente](/help/managing-customer-accounts) — Gestione del profilo del cliente
- [Configurazione Email](/help/email-configuration) — Configurazione SMTP e modelli email

Ricorda: Preserva tutto il formattaggio markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.