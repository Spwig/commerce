---
title: Preferenze di comunicazione
---

Le preferenze di comunicazione consentono ai clienti di controllare quali e-mail e messaggi SMS ricevono dal tuo negozio. Questo sistema garantisce la conformità al GDPR e ti aiuta a rispettare le preferenze di comunicazione dei clienti su tutti i canali.

Accedi a **Clienti > Preferenze di comunicazione** nella barra laterale di amministrazione per gestire le preferenze di comunicazione dei clienti.

## Comprensione delle preferenze di comunicazione

Il sistema di preferenze di comunicazione offre ai clienti un controllo dettagliato sui messaggi che ricevono. Questo include:

- **E-mail transazionali** — Conferme degli ordini essenziali, aggiornamenti di spedizione, e-mail di sicurezza dell'account (sempre attive)
- **E-mail di marketing** — Newsletter, promozioni, raccomandazioni di prodotti (richiede opt-in)
- **Notifiche specifiche dell'app** — Post del blog, punti fedeltà, premi di referral, commissioni di affiliazione
- **Notifiche SMS** — Notifiche tramite messaggio di testo (richiede opt-in esplicito secondo TCPA)

Tutte le comunicazioni di marketing richiedono il consenso del cliente e la verifica dell'e-mail per garantire la conformità al GDPR.

## Tipi di preferenze spiegati

### Comunicazioni transazionali (sempre attive)

I messaggi transazionali sono essenziali per l'account e gli ordini del tuo cliente. Questi **non possono essere disattivati** dai clienti:

| Tipo | Descrizione | Esempi |
|------|-------------|----------|
| **Conferme degli ordini** | Conferma quando l'ordine viene effettuato | L'ordine #12345 è stato ricevuto |
| **Aggiornamenti di spedizione** | Notifiche quando lo stato dell'ordine cambia | Il tuo ordine è stato spedito |
| **Conferme di pagamento** | Pagamento ricevuto, rimborso elaborato | Pagamento di $49.99 confermato |
| **Sicurezza dell'account** | Reimpostazione della password, verifica dell'e-mail | Reimposta la tua password |

### Comunicazioni di marketing (richiede opt-in)

I messaggi di marketing richiedono il consenso del cliente e la verifica dell'e-mail:

| Tipo | Descrizione | Predefinito |
|------|-------------|---------|
| **Newsletter** | Newsletter generali e aggiornamenti | Opt-out |
| **Offerte promozionali** | Saldi, sconti, offerte speciali | Opt-out |
| **Raccomandazioni di prodotti** | Suggerimenti di prodotti personalizzati | Opt-out |
| **Rientro in magazzino** | Notifiche quando i prodotti tornano disponibili | Opt-out |

I clienti devono **verificare il proprio indirizzo e-mail** prima di ricevere qualsiasi e-mail di marketing (requisito di doppio opt-in del GDPR).

### Preferenze specifiche dell'app

I clienti possono controllare le notifiche da funzionalità specifiche:

**Notifiche del blog**
- Nuovo post del blog pubblicato (immediato, digest settimanale o digest mensile)
- Abbonamenti specifici per categoria
- Preferenze di frequenza

**Programma di fedeltà**
- Notifiche di punti guadagnati
- Promozioni di livello
- Premi sbloccati
- Punti in scadenza imminente
- Bonus di compleanno
- Offerte di campagna

**Programma di referral**
- Premio emesso (referente e referito)
- Iscrizione di referral riuscita
- Premio in scadenza imminente
- Inviti di referral

**Programma di affiliazione**
- Commissione guadagnata
- Commissione approvata o rifiutata
- Pagamento elaborato, completato o fallito
- Report di performance mensili

### Notifiche SMS (richiede opt-in esplicito)

Tutte le notifiche SMS richiedono **opt-in esplicito** secondo le normative TCPA. I clienti devono spuntare attivamente la casella di opt-in SMS:

- **SMS transazionali** — Ordine spedito, consegnato (richiede opt-in)
- **SMS di marketing** — Promozioni, offerte speciali (richiede opt-in separato)

Anche gli SMS transazionali richiedono l'opt-in perché l'invio di messaggi di testo non richiesti è regolato più rigorosamente rispetto alle e-mail.

## Gestione delle preferenze dei clienti nell'area di amministrazione

### Visualizzazione di tutte le preferenze

Accedi a **Clienti > Preferenze di comunicazione** per visualizzare tutte le preferenze dei clienti:

| Colonna | Descrizione |
|--------|-------------|
| **Email Utente** | Indirizzo email del cliente (collegato all'admin utente) |
| **Stato Email** | ✓ verde se le email sono abilitate, ○ grigio se disabilitate |
| **Stato SMS** | ✓ verde se gli SMS sono abilitati, ○ grigio se disabilitati |
| **Stato Marketing** | Badge "Iscritto" o "Disiscritto" |
| **Stato Verifica** | 📧✓ se email verificata, 📱✓ se SMS verificato |
| **Origine Consenso** | Dove il cliente ha acconsentito (registrazione, checkout, centro preferenze) |
| **Aggiornato Il** | Ultimo momento in cui le preferenze sono state modificate |

### Filtraggio Preferenze

Usa la barra laterale dei filtri per trovare i clienti:

- **Email Abilitata** — Sì/No
- **SMS Abilitato** — Sì/No
- **Marketing Email** — Sì/No (iscritto al marketing)
- **Marketing SMS** — Sì/No (iscritto al marketing SMS)
- **Email Verificata** — Sì/No (ha verificato il proprio indirizzo email)
- **SMS Verificato** — Sì/No (ha verificato il proprio numero di telefono)
- **Origine Consenso** — Registrazione, Checkout, Centro Preferenze, API, Migrazione
- **Codice Lingua** — Lingua preferita per le comunicazioni

### Ricerca Preferenze

Cerca clienti per:
- Email utente
- Nome utente
- Nome
- Cognome
- Token di disiscrizione

### Azioni di Massa

Seleziona più clienti e applica azioni di massa:

**✓ Segna Email come Verificata**
- Verifica manualmente gli indirizzi email dei clienti
- Utile quando si importano clienti da un altro sistema
- Invalida la cache delle preferenze per applicare le modifiche immediatamente

**🚫 Disiscrivi da Tutto il Marketing**
- Disabilita tutte le comunicazioni di marketing (email, SMS, tutte le app)
- Mantiene abilitate le email transazionali
- Usa questa opzione per i clienti che richiedono la disiscrizione completa
- Rispetta il diritto GDPR di revocare il consenso

**📥 Esporta Preferenze in CSV**
- Esporta le preferenze dei clienti in un foglio di calcolo
- Include tutti i campi delle preferenze e le impostazioni specifiche dell'app
- Utile per audit di conformità e analisi
- Formato: CSV con intestazioni

## Centro Preferenze Self-Service per Clienti

I clienti possono gestire le proprie preferenze in `/accounts/preferences/` quando sono connessi.

### Funzionalità del Centro Preferenze

**Azioni Rapide**
- **Iscriviti a Tutto il Marketing** — Abilita tutte le comunicazioni di marketing con un clic
- **Disiscriviti da Tutto** — Disabilita tutte le comunicazioni di marketing (le transazionali restano abilitate)

**Schede Preferenze**
- **Email Transazionali** — Sola lettura (sempre abilitate, contrassegnate come "Obbligatorie")
- **Comunicazioni di Marketing** — Attiva/disattiva con badge di verifica
- **Preferenze Blog** — Abilita/disabilita, seleziona la frequenza (immediata, settimanale, mensile)
- **Programma Fedeltà** — Abilita/disabilita i singoli tipi di notifica
- **Programma di Referral** — Abilita/disabilita le notifiche sui premi
- **Programma di Affiliazione** — Abilita/disabilita le notifiche su commissioni e pagamenti
- **Notifiche SMS** — Iscriviti/disiscriviti dagli SMS (mostra lo stato di verifica)

**Aggiornamenti in Tempo Reale**
- Le modifiche vengono salvate immediatamente tramite AJAX
- Nessun ricaricamento della pagina richiesto
- Feedback visivo quando salvato

### Processo di Verifica Email

Quando un cliente abilita le email di marketing:

1. Il cliente attiva "Email di Marketing" su ON
2. Il sistema invia un'email di verifica con un link univoco
3. Il cliente clicca sul link di verifica
4. L'email viene contrassegnata come verificata (compare il badge 📧✓)
5. Le email di marketing verranno ora inviate

**I clienti non verificati NON riceveranno email di marketing** anche se l'interruttore è su ON. Questo garantisce la conformità al doppio opt-in GDPR.

## Disiscrizione con Un Clic

Tutte le email di marketing includono un link di disiscrizione nel piè di pagina. Cliccando su questo link:

1. Il cliente viene reindirizzato a `/accounts/unsubscribe/<token>/` (nessun login richiesto)
2. Viene mostrato da cosa si sta disiscrivendo
3. È possibile fornire un feedback opzionale (motivo della disiscrizione)
4. Le comunicazioni di marketing vengono disabilitate
5. Le email transazionali restano abilitate
6. Viene fornito un link al centro preferenze completo

I clienti possono riiscriversi in qualsiasi momento tramite il centro preferenze.

## Conformità e Requisiti Legali

### Conformità all'Articolo 7 del GDPR

Il sistema garantisce la piena conformità all'Articolo 7 del GDPR:


**✅ Prova del consenso**
- Timestamp del momento in cui è stato dato il consenso
- Fonte del consenso (registrazione, checkout, centro preferenze)
- Indirizzo IP del consenso
- User agent (informazioni sul browser)

**✅ Consenso separato**
- Le email di marketing e transazionali sono interruttori separati
- Ogni app (blog, fedeltà, ecc.) richiede un consenso individuale

**✅ Facile revoca**
- Disiscrizione con un clic in tutte le email di marketing
- Centro preferenze disponibile per tutti i clienti connessi
- La disiscrizione ha effetto immediato

**✅ Consenso dato liberamente**
- L'impostazione predefinita per il marketing è opt-out (migliore pratica GDPR)
- Nessuna casella pre-selezionata (i clienti devono optare attivamente)

**✅ Consenso specifico e informato**
- Descrizioni chiare di ciò che ogni preferenza controlla
- Preferenze granulari a livello di app (non tutto o niente)

**✅ Consenso verificabile**
- Double opt-in per le email di marketing
- Traccia di audit tramite il monitoraggio dello stato di EmailOutbox

### Conformità TCPA (Regolamenti SMS USA)

Tutte le notifiche SMS richiedono un **opt-in esplicito**:

- I clienti devono spuntare attivamente la casella di opt-in SMS
- Non sono consentite caselle pre-selezionate
- Descrizione chiara di ciò in cui stanno optando
- Facile opt-out tramite il centro preferenze
- Tutti gli invii SMS sono registrati per l'audit di conformità

### Conformità CAN-SPAM (Regolamenti Email USA)

Il sistema garantisce la conformità CAN-SPAM:

- Link di disiscrizione in ogni email di marketing
- Disiscrizione elaborata immediatamente (richiesti 10 giorni lavorativi, lo facciamo istantaneamente)
- Nome "Da" chiaro (il nome del tuo negozio)
- Indirizzo fisico nel piè di pagina dell'email
- Nessuna riga dell'oggetto ingannevole

## Comprensione dello stato delle email in EmailOutbox

Quando si visualizza **Sistema Email > Casella di uscita email**, si vedrà come le preferenze influenzano la consegna delle email:

| Stato | Significato | Motivo |
|--------|---------|--------|
| **In attesa** | Email in coda per l'invio | Le preferenze consentono questa email |
| **In coda** | Nella coda di invio | Le preferenze consentono questa email |
| **Saltata** | Email non inviata | Preferenza del cliente disabilitata |
| **Inviata** | Consegnata con successo | Email inviata normalmente |

Quando un'email viene **saltata**, il campo `skip_reason` mostra il motivo:

- **user_preference_disabled** — Il cliente ha disabilitato questo tipo di email nelle preferenze
- **email_not_verified** — Il cliente non ha verificato il proprio indirizzo email
- **email_disabled** — Il cliente ha disabilitato tutte le email (interruttore principale)

Questa traccia di audit è importante per la conformità GDPR — puoi dimostrare di aver rispettato le preferenze dei clienti.

## Impostazioni del sito per le preferenze

Vai a **Impostazioni > Impostazioni del sito** per configurare i valori predefiniti globali delle preferenze:

**Abilita Double Opt-In per le email di marketing** (Predefinito: Sì)
- Richiede la verifica dell'email prima di inviare email di marketing
- Migliore pratica GDPR
- Raccomandato: Lascia abilitato

**Stato predefinito di opt-in per il marketing** (Predefinito: No - Opt-Out)
- Stato predefinito quando nuovi clienti si registrano
- Il GDPR richiede l'opt-out come predefinito
- Raccomandato: Lascia come opt-out (False)

**Centro preferenze abilitato** (Predefinito: Sì)
- Consente ai clienti di gestire le proprie preferenze
- Necessario per il diritto GDPR di revocare il consenso
- Raccomandato: Lascia abilitato

**Richiedi verifica SMS** (Predefinito: No)
- Richiede la verifica del numero di telefono per le notifiche SMS
- Facoltativo ma raccomandato per i mittenti SMS ad alto volume
- Può essere abilitato se si desidera il double opt-in per gli SMS

**Mostra motivi della disiscrizione** (Predefinito: Sì)
- Raccoglie feedback facoltativi quando i clienti si disiscrivono
- Aiuta a capire perché i clienti optano per l'uscita
- Raccomandato: Lascia abilitato per ottenere informazioni

## Migliori pratiche

### 1. Predefinito Opt-Out per il marketing

Imposta sempre le comunicazioni di marketing su **opt-out** (non spuntato):
- Conforme al GDPR
- Costruisce fiducia con i clienti
- Riduce le segnalazioni di spam
- Invia solo a clienti coinvolti

### 2. Richiedi la verifica dell'email

Mantieni il **Double Opt-In** abilitato:
- Garantisce che gli indirizzi email siano validi
- Conferma che il cliente desidera effettivamente le email di marketing
- Riduce il tasso di rimbalzo
- Necessario per la conformità GDPR

### 3. Rispetta le preferenze immediatamente

Mantieni tutte le formattazioni markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

Quando un cliente modifica le preferenze:
- Le modifiche hanno effetto immediato
- La cache delle preferenze viene invalidata
- La prossima invio di email verificherà le preferenze aggiornate
- Nessun ritardo nel rispettare le richieste di disiscrizione

### 4. Monitoraggio delle email saltate

Controlla regolarmente la **Cassetta di uscita email** per le email saltate:
- Un alto tasso di salti indica che i clienti stanno disiscrivendosi
- Potrebbe segnalare la necessità di migliorare il contenuto delle email
- Aiuta a identificare problemi di preferenze

### 5. Audit di conformità periodici

Esporta le preferenze periodicamente per la conformità:
1. Vai a **Preferenze di comunicazione**
2. Seleziona tutti i clienti
3. Scegli **Esporta preferenze in CSV**
4. Salva per la traccia di audit GDPR

Conserva le esportazioni per **almeno 3 anni** per rispettare i requisiti di conservazione dei dati GDPR.

### 6. Comunicazione chiara

Quando raccogli il consenso:
- Usa un linguaggio semplice, non gergo legale
- Spiega cosa riceveranno i clienti
- Mostra la frequenza (giornaliera, settimanale, mensile)
- Rendi evidenti le caselle di opt-in ma non precompilate

### 7. Segmentazione per preferenza

Quando invii campagne di marketing:
- Invia solo a clienti verificati e iscritti
- Rispetta le preferenze specifiche dell'app (non inviare email del blog a clienti che hanno disabilitato il blog)
- Usa le preferenze di frequenza (non inviare email immediate agli abbonati al digest settimanale)

## Suggerimenti

**💡 Verifica le preferenze prima dell'invio**

Il sistema verifica automaticamente le preferenze quando invii email utilizzando `EmailSendingService.send_template_email()`. Assicurati che tutti gli invii di email utilizzino questo servizio, non chiamate SMTP dirette.

**💡 Lo stato "Saltato" è normale**

Non allarmarti per le email saltate nella cassetta di uscita — significa che il sistema funziona correttamente e rispetta le preferenze dei clienti. È meglio saltare email indesiderate che rischiare multe GDPR o reclami per spam.

**💡 La cache delle preferenze è di 5 minuti**

Le verifiche delle preferenze sono in cache per 5 minuti per le prestazioni. Quando i clienti modificano le preferenze tramite il centro preferenze o azioni di amministrazione, la cache viene invalidata immediatamente in modo che le modifiche abbiano effetto subito.

**💡 I clienti ospiti bypassano le verifiche**

I clienti che effettuano l'acquisto come ospiti (senza account) riceveranno tutte le email normalmente perché non hanno un record di preferenze. Questo è intenzionale — hanno optato in fornendo la loro email al checkout.

**💡 Le email transazionali vengono sempre inviate**

Le confermi ordini, gli aggiornamenti di spedizione e le email di sicurezza dell'account **vengono sempre inviate** indipendentemente dalle preferenze. Questo assicura che i clienti ricevano informazioni critiche sui loro ordini e account.

**💡 Usa le azioni di massa con cautela**

L'azione di massa "Disiscrivi da tutto il marketing" influisce su **tutte le app** (blog, fedeltà, referral, affiliazione). Usa questa opzione solo per i clienti che hanno richiesto esplicitamente di essere completamente disiscritti. Per preferenze specifiche, modifica i record individuali dei clienti.

**💡 Traccia di audit per la conformità**

Il sistema traccia:
- Timestamp e origine del consenso
- Indirizzo IP e user agent
- Timestamp della verifica email
- Ogni modifica delle preferenze tramite lo stato "saltato" di EmailOutbox

Questa traccia di audit dimostra la conformità GDPR se le autorità richiedono mai prove del consenso.

## Argomenti correlati

- [Gestione degli account dei clienti](/help/managing-customer-accounts) — Gestione del profilo del cliente
- [Configurazione email](/help/email-configuration) — Configurazione SMTP e modelli di email