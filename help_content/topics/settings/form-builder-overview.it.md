---
title: Panoramica del Costruttore di Moduli
---

Il Costruttore di Moduli crea moduli personalizzati per la raccolta di dati - moduli di contatto, sondaggi, applicazioni, registrazioni e altro ancora. Crea moduli visivamente con campi trascinabili, configura regole di convalida, attiva flussi di lavoro multi-step e raccogli risposte con analisi dettagliate. I moduli si integrano in modo impeccabile con gli elementi del Page Builder, incorporandosi ovunque nel tuo sito. Tutte le consegne vengono salvate nel database con metadati completi (indirizzo IP, browser, tempo per completare) per l'analisi e l'esportazione.

Utilizza il Costruttore di Moduli quando devi raccogliere dati strutturati dai clienti, che si tratti di semplice informazioni di contatto o di complessi applicazioni multi-pagina.

## Cosa è il Costruttore di Moduli?

Il Costruttore di Moduli è uno strumento visivo a trascinamento per creare moduli personalizzati senza codice:

**Tipi di Moduli Supportati**:
- Moduli di contatto (nome, email, messaggio)
- Sondaggi dei clienti (valutazioni, feedback, NPS)
- Registrazioni dei prodotti (garanzia, supporto)
- Candidature per lavoro (caricamento del CV, multi-step)
- Registrazioni per eventi (informazioni sull'assistente, preferenze)
- Richieste di servizio (richieste dettagliate)
- Iscrizioni alla newsletter (con caselle di selezione per le preferenze)

**Funzionalità Principali**:
- **22 tipi di campo** - Testo, email, telefono, caricamento file, valutazioni, selezionatori di prodotti e altro
- **Moduli multi-step** - Suddividi i moduli lunghi in passaggi logici con tracciamento del progresso
- **Logica condizionale** - Mostra/nascondi campi in base alle risposte dell'utente
- **Regole di convalida** - Campi obbligatori, lunghezza minima/massima, pattern regex personalizzati
- **Protezione da spam** - Campi honeypot o Google reCAPTCHA v3
- **Analisi delle risposte** - Traccia il tempo di completamento, indirizzo IP, browser, referrer
- **Esportazione CSV** - Scarica tutte le risposte per l'analisi in Excel/Google Sheets
- **Multi-lingua** - Traduci etichette e messaggi del modulo in tutti i linguaggi attivi

## Creare il Primo Modulo

Naviga a **Impostazioni > Pagine > Moduli** per accedere al gestore dei moduli:

**Passo 1: Crea Nuovo Modulo**
- Fai clic su **+ Crea Nuovo Modulo**
- Inserisci il nome del modulo (identificatore interno, non mostrato ai clienti)
- Inserisci il titolo del modulo (mostrato come titolo sopra al modulo)
- Opzionale: Aggiungi descrizione (testo di aiuto mostrato sotto il titolo)

**Passo 2: Aggiungi Campi**
- Fai clic su **Modifica Progettazione del Modulo** per aprire il costruttore visivo
- Trascina i tipi di campo dalla barra laterale sinistra sul canvas
- Fai clic sul campo per configurarlo nel pannello di destra
- Imposta etichetta, placeholder, testo di aiuto
- Abilita/disabilita lo stato obbligatorio
- Aggiungi regole di convalida

**Passo 3: Configura le Impostazioni del Modulo**
- Imposta il testo del pulsante di invio (predefinito: "Invia")
- Personalizza il messaggio di successo (mostrato dopo l'invio)
- Scegli la protezione da spam (raccomandato honeypot)
- Abilita/disabilita "Richiedi Login" se necessario
- Abilita "Modulo multi-step" per moduli complessi

**Passo 4: Attiva il Modulo**
- Abilita lo stato **Attivo**
- Solo i moduli attivi accettano le consegne
- Salva il modulo

**Passo 5: Utilizza nel Page Builder**
- Aggiungi l'elemento **Modulo** a qualsiasi pagina
- Seleziona il tuo modulo dal menu a discesa
- Il modulo eredita lo stile della pagina
- Le consegne vengono inviate automaticamente al backend

## Moduli a Singola Pagina vs Moduli Multi-step

**Moduli a Singola Pagina** (predefinito):
- Tutti i campi visualizzati contemporaneamente
- Scorrimento per vedere tutti i campi
- Pulsante di invio in fondo
- Ideale per: Moduli di contatto, sondaggi brevi, raccolta dati semplice

**Moduli Multi-step**:
- Campi organizzati in passaggi numerati
- Barra di progresso che mostra il passaggio corrente
- Pulsanti di navigazione Indietro/Avanti
- Invio solo sul passaggio finale
- Opzionale: Salva risposte parziali (modalità bozza)
- Ideale per: Candidature per lavoro, registrazioni, sondaggi complessi, flussi di checkout

**Abilitare Moduli Multi-step**:
1. Abilita "Modulo multi-step" nelle impostazioni del modulo
2. Fai clic sulla scheda **Passaggi** nel pannello di destra
3. Aggiungi un passaggio (es. "Informazioni personali", "Dettagli di contatto", "Preferenze")
4. Assegna i campi ai passaggi utilizzando il menu a discesa dei passaggi quando si modifica il campo
5. Riordina i passaggi trascinandoli
6. Imposta le proprietà del passaggio: titolo, descrizione, saltabile

**Vantaggi dei Moduli Multi-step**:
- Riduce l'abbandono del modulo (psicologico: "solo 3 domande su questa pagina")
- Gruppo logico migliora l'esperienza utente
- Indicatore di progresso motiva il completamento
- Salvataggio parziale opzionale per moduli lunghi

## Impostazioni del Modulo Spiegate

**Impostazioni di Base**:
- **Nome Interno** - Come identifichi il modulo nell'amministrazione (non visibile ai clienti)
- **Slug** - Identificatore amichevole per URL (generato automaticamente, utilizzato in endpoint API)
- **Titolo del Modulo** - Titolo visualizzato sopra al modulo
- **Descrizione** - Testo di aiuto opzionale mostrato sotto il titolo
- **Testo del Pulsante di Invio** - Personalizza l'etichetta del pulsante (es. "Invia Messaggio", "Candidati Ora")

**Messaggi**:
- **Messaggio di Successo** - Mostrato dopo l'invio riuscito (predefinito: "Grazie per la tua consegna!")
- **Messaggio di Errore** - Mostrato se l'invio fallisce (predefinito: "Si è verificato un errore. Per favore riprova.")

**Sicurezza e Accesso**:
- **Attivo** - Solo i moduli attivi accettano le consegne (i moduli non attivi mostrano "Modulo non disponibile")
- **Richiedi Login** - Limita solo agli utenti autenticati (gli utenti anonimi vedono il prompt di login)

**Protezione da Spam**:
- **Nessuna** - Nessuna protezione (non raccomandato, i bot invieranno spam)
- **Campo Honeypot** - Campo invisibile che cattura i bot (raccomandato per la maggior parte dei commercianti)
- **Google reCAPTCHA v3** - Richiede chiave del sito e chiave segreta da Google (protezione più forte)

**Funzionalità Avanzate**:
- **Modulo multi-step** - Abilita un flusso di lavoro passo dopo passo
- **Salva Risposte Parziali** - Permette agli utenti di salvare il progresso e riprendere in seguito (solo moduli multi-step)

## Opzioni di Protezione da Spam

**Campo Honeypot (Raccomandato)**:
- Campo invisibile aggiunto al modulo
- I bot lo compilano (gli utenti non possono vederlo)
- Le consegne con campo honeypot compilato vengono rifiutate
- Nessuna configurazione richiesta
- Nessuna frustrazione CAPTCHA per gli utenti
- Effettiva contro il 95%+ dei bot di spam

**Google reCAPTCHA v3**:
- Punteggio di background invisibile (0.0-1.0)
- Nessun "clicca sul semaforo" challenge
- Richiede configurazione:
  1. Crea account su google.com/recaptcha/admin
  2. Genera chiave del sito e chiave segreta
  3. Inserisci le chiavi nelle impostazioni del costruttore di moduli
- Più robusto del honeypot
- Utilizza quando honeypot non è sufficiente

**Nessuna**:
- Nessuna protezione da spam
- Utilizza solo per moduli interni o test
- I moduli pubblici saranno spammati pesantemente

## Gestione delle Risposte del Modulo

Visualizza tutte le consegne a **Impostazioni > Pagine > Moduli > [Nome del Modulo] > Risposte**:

**Visualizzazione Elenco Risposte**:
- Stato: bozza, inviata, completata
- Mittente: email (se autenticato) o "Anonimo"
- Indirizzo IP e posizione (se GeoIP abilitato)
- Data/ora di invio
- Tempo per completare (secondi)

**Dettaglio Risposta**:
- Tutti i valori dei campi con etichette
- Metadati: browser, referrer, lingua
- Tracciamento del progresso (multi-step): passaggio corrente, passaggi completati
- Risultati delle azioni (se il modulo attiva azioni)

**Filtraggio Risposte**:
- Filtra per modulo, stato, intervallo di date
- Cerca per email del mittente o indirizzo IP
- Ordina per data di invio, tempo di completamento

**Esportazione Risposte**:
- Fai clic sul pulsante **Esporta in CSV**
- Scarica `{form-slug}_responses_{date}.csv`
- Righe di intestazione: Submitted At, User, IP, Status, [Etichette dei Campi]
- Una risposta per riga
- Apri in Excel, Google Sheets o strumenti di analisi dei dati

## Utilizzo dei Moduli nelle Pagine

**Inserimento dei Moduli**:
1. Apri la pagina nel Page Builder
2. Aggiungi l'elemento **Modulo** dal pannello degli elementi
3. Seleziona il modulo dal menu a discesa
4. Personalizza lo stile del contenitore del modulo (sfondo, padding, bordo)
5. Salva e pubblica la pagina

**Il Modulo Viene Renderto Con**:
- Titolo e descrizione del modulo (dalle impostazioni del modulo)
- Tutti i campi nell'ordine (singola pagina) o passaggio corrente (multi-step)
- Pulsante di invio con testo personalizzato
- Messaggi di successo/errore dopo l'invio

**Ereditarietà dello Stile**:
- I moduli ereditano lo stile del tema della pagina
- I pulsanti utilizzano lo stile dei pulsanti del tema
- I campi di input utilizzano lo stile degli input del tema
- È possibile aggiungere una classe CSS personalizzata ai campi per uno stile specifico

## Interfaccia del Costruttore di Moduli

**Barra Laterale Sinistra - Libreria dei Campi**:
- Organizzati per categoria (Testo, Selezione, Valutazione, Avanzato)
- Trascina il campo sul canvas o fai clic per aggiungerlo
- Cerca per trovare rapidamente i tipi di campo

**Canvas Principale - Editor dei Campi**:
- Maniglia di trascinamento (≡) per riordinare i campi
- Fai clic sul campo per selezionarlo e modificarlo
- Pulsante di cancellazione (×) su ogni campo
- Anteprima visiva del campo come configurato
- Stato vuoto con istruzioni per la zona di trascinamento

**Barra Laterale Destra - Pannello delle Proprietà**:
- **Scheda Impostazioni del Modulo** - Informazioni di base, messaggi, protezione da spam
- **Scheda Impostazioni del Campo** - Configura il campo selezionato (etichetta, convalida, ecc.)
- **Scheda Passaggi** - Gestisci i passaggi (solo moduli multi-step)
- **Scheda Regole Condizionali** - Aggiungi logica di visualizzazione/nascondimento basata sulle risposte

**Funzionalità della Barra degli Strumenti**:
- **Annulla/Rifai** - Storia completa delle modifiche
- **Anteprima** - Testa la funzionalità del modulo
- **Salva** - Salva automaticamente ogni 3 secondi durante la modifica
- **Traduzioni** - Traduci il testo del modulo in altre lingue

## Esempi Comuni di Moduli

**Modulo di Contatto**:
- Campi: Nome Completo (obbligatorio), Email (obbligatorio), Telefono, Messaggio (obbligatorio)
- Pulsante di invio: "Invia Messaggio"
- Successo: "Grazie per averci contattato! Risponderemo entro 24 ore." 

**Sondaggio sul Feedback dei Prodotti**:
- Passo 1: Valutazione a stelle, accordo su scala Likert
- Passo 2: Punteggio NPS, suggerimenti per miglioramenti
- Condizionale: Se valutazione < 3, richiedi feedback sui miglioramenti

**Candidatura per Lavoro**:
- Passo 1: Informazioni personali (nome, email, telefono)
- Passo 2: Esperienza (caricamento del CV, anni di esperienza, referenze)
- Passo 3: Disponibilità (data di inizio, aspettative salariali)
- Salva parziale abilitato (i candidati possono riprendere in seguito)

**Iscrizione alla Newsletter con Preferenze**:
- Email (obbligatorio)
- Gruppo di caselle di selezione: Interessi (Prodotti, Vendite, Aggiornamenti del Blog)
- reCAPTCHA abilitato (prevenire iscrizioni false)

## Consigli

- **Inizia con una singola pagina** - Aggiungi multi-step solo se il modulo supera 10 campi
- **Utilizza honeypot prima** - Aggiorna solo a reCAPTCHA se lo spam persiste
- **Testa prima di pubblicare** - Utilizza la modalità anteprima per verificare la convalida e il flusso
- **Esporta regolarmente** - Scarica il CSV delle risposte settimanalmente per il backup
- **Monitora il tempo di completamento** - Se la media è >5 minuti, il modulo potrebbe essere troppo lungo
- **Utilizza la logica condizionale** - Nascondi i campi irrilevanti per ridurre la percezione della lunghezza del modulo
- **Abilita il salvataggio parziale per moduli lunghi** - Riduce l'abbandono su applicazioni multi-step
- **Traduci le etichette del modulo** - Utilizza il sistema di traduzione integrato per siti multilingua
- **Richiedi login per dati sensibili** - Impedisce lo spam anonimo, collega le consegne agli account utente
- **Mantieni i messaggi di successo specifici** - "Risponderemo entro 24 ore" è meglio di "Grazie"