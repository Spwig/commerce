---
title: Campi e Validazione del Costruttore di Form
---

I campi delle form sono i blocchi costruttivi delle tue form—ogni campo raccoglie un pezzo di dati dagli utenti. Il Form Builder offre 22 tipi di campi che vanno da semplici input di testo a scale di valutazione avanzate e selezionatori di prodotti. Configura ogni campo con etichette, regole di validazione, testo di aiuto e logica condizionale per creare form dinamici che si adattano in base alle risposte degli utenti. I campi possono essere obbligatori o opzionali, validati con pattern regex e stili personalizzati con classi CSS.

Utilizza questa guida per comprendere tutti i tipi di campi disponibili, quando utilizzare ciascuno e come configurare la validazione e la logica condizionale.

## Configurazione di Base dei Campi

Ogni campo condivide queste impostazioni comuni:

**Identità**:
- **Nome del Campo** - Nome macchina per lo storage dei dati (nessuno spazio, usa gli underscore: `email_address`)
- **Tipo di Campo** - Determina il comportamento dell'input e il rendering
- **Assegnazione al Passo** - A quale passo appartiene questo campo (solo per form multi-passo)

**Visualizzazione**:
- **Etichetta** - Domanda o prompt mostrati agli utenti (es. "Qual è il tuo indirizzo email?")
- **Placeholder** - Testo di suggerimento all'interno dell'input (es. "you@example.com")
- **Testo di Aiuto** - Guida aggiuntiva sotto il campo (es. "Mai condivideremo il tuo indirizzo email")
- **Valore Predefinito** - Valore precompilato (gli utenti possono cambiarlo)

**Layout**:
- **Larghezza** - Intera (100%), Metà (50%) o Un Terzo (33%) della larghezza della form
- **Classe CSS** - Classi aggiuntive di stile per un design personalizzato
- **Ordine** - Posizione all'interno del passo (trascina per riordinare)

**Validazione**:
- **Obbligatorio** - Attiva/disattiva lo stato obbligatorio (compare un asterisco rosso sull'etichetta)
- **Lunghezza Min/Max** - Limiti di caratteri (campi di testo)
- **Valore Min/Max** - Limiti numerici (campi numerici)
- **Pattern di Validazione** - Pattern regex personalizzato per una validazione complessa
- **Messaggio di Errore** - Testo personalizzato mostrato quando la validazione fallisce

## Campi di Input di Testo

**Testo Singola Linea** (`text`):
- Input di testo di base per risposte brevi
- Validazione: lunghezza minima/massima, pattern regex
- Caso d'uso: Nomi, indirizzi, codici prodotto, risposte brevi
- Esempio: "Nome Completo", "Indirizzo di Strada", "Nome Azienda"

**Testo Multi-linea** (`textarea`):
- Area di testo espandibile per contenuti più lunghi (3-10 righe)
- Validazione: lunghezza minima/massima
- Caso d'uso: Commenti, feedback, descrizioni dettagliate, messaggi
- Esempio: "Dìci di più sulla tua esperienza", "Note aggiuntive"

**Indirizzo Email** (`email`):
- Validazione specifica per email (richiede @ e dominio)
- Tastiera mobile mostra chiaramente la chiave @
- Caso d'uso: Email di contatto, iscrizioni alla newsletter, creazione account
- Esempio: "Indirizzo Email", "Email di Lavoro"

**Numero di Telefono** (`phone`):
- Formatta automaticamente i numeri di telefono
- Tastiera mobile mostra layout numerico
- Validazione: pattern configurabile (supporta formati internazionali)
- Caso d'uso: Telefono di contatto, contatto d'emergenza, prenotazione appuntamenti
- Esempio: "Numero di Telefono", "Cellulare", "Numero di Contatto"

**Numero** (`number`):
- Input numerico con controlli di incremento/decremento
- Validazione: valore minimo/massimo, incremento passo
- Restituisce numero (non stringa) nelle risposte
- Caso d'uso: Quantità, età, anni di esperienza, importi di budget
- Esempio: "Quanti dipendenti hai?", "La tua età", "Anni in attività"

**URL** (`url`):
- Validazione URL (richiede http:// o https://)
- Tastiera mobile mostra la chiave .com
- Caso d'uso: Sito web, profilo LinkedIn, link al portfolio
- Esempio: "Sito Web Aziendale", "URL del Portfolio"

## Campi di Selezione

**Selezione a Discesa** (`select`):
- Selezione singola da menu a discesa
- Configurazione: array di {value, label} opzioni
- Supporta selezione predefinita
- Caso d'uso: Categorie, stati/paesi, selezione stato
- Esempio: "Seleziona il tuo paese", "Dipartimento", "Come hai sentito parlare di noi?"
- Migliore per: 5+ opzioni (per meno opzioni usa i radio)

**Pulsanti di Selezione** (`radio`):
- Scelta singola da opzioni visibili (tutte le opzioni mostrate)
- Configurazione: array di {value, label} opzioni
- Migliore UX rispetto a select per 2-4 opzioni
- Caso d'uso: Domande sì/no, genere, preferenze con poche opzioni
- Esempio: "Ti consiglieremmo a qualcuno?", "Metodo di contatto preferito"

**Casella di Controllo** (`checkbox`):
- Singola casella di controllo (on/off)
- Restituisce true/false nelle risposte
- Caso d'uso: Accettazione di termini, accordi, singola preferenza
- Esempio: "Accetto i termini e le condizioni", "Iscriviti alla newsletter"

**Gruppo di Caselle di Controllo** (`checkbox_group`):
- Selezione multipla da opzioni (gli utenti possono selezionare 0, 1 o molte)
- Configurazione: array di {value, label} opzioni
- Restituisce array di valori selezionati
- Caso d'uso: Preferenze multi-selezione, interessi, funzionalità necessarie
- Esempio: "Quali argomenti ti interessano?", "Seleziona tutti i pertinenti"

## Campi di Valutazione

**Valutazione a Stelle** (`rating_stars`):
- Scala visiva di valutazione a stelle (tipicamente 1-5 stelle)
- Configurazione:
  - `max_stars`: 3-10 stelle (default: 5)
  - `allow_half`: true/false per valutazioni a mezza stella
  - `icon`: fa-star (default) o fa-heart
  - `color`: codice colore esadecimale (default: #FFD700 oro)
- Caso d'uso: Valutazioni prodotto, qualità del servizio, punteggi di soddisfazione
- Esempio: "Valuta la tua esperienza", "Come è stato il nostro servizio?"

**Scala Likert** (`rating_likert`):
- Scala di valutazione di affermazioni: fortemente in disaccordo → fortemente d'accordo
- Configurazione:
  - `scale_type`: 5_point (1-5) o 7_point (1-7)
  - `labels`: personalizza il testo degli estremi (sinistra: "Fortemente in Disaccordo", destra: "Fortemente d'Accordo")
- Restituisce valore numerico (1-5 o 1-7)
- Caso d'uso: Affermazioni di sondaggio, scale di accordo, misurazione del sentimenti
- Esempio: "Il prodotto soddisfa le mie esigenze", "Il servizio clienti è stato utile"

**Punteggio Netto Promotore (NPS)** (`rating_nps`):
- Scala 0-10: "Non affatto probabile" a "Estremamente probabile"
- Configurazione:
  - `low_label`: testo dell'estremo sinistro (default: "Non affatto probabile")
  - `high_label`: testo dell'estremo destro (default: "Estremamente probabile")
- Restituisce valore 0-10 (0-6 = detrattori, 7-8 = passivi, 9-10 = promotori)
- Caso d'uso: Sondaggi NPS, probabilità di raccomandazione, misurazione della fedeltà
- Esempio: "Quanto probabilmente ti consiglieresti a un amico?"

## Campi Avanzati

**Caricamento File** (`file`):
- Caricamento singolo o multipli file
- Configurazione:
  - `max_size_mb`: limite di dimensione per file (default: 5MB)
  - `allowed_types`: array di estensioni (es. ["pdf", "doc", "docx", "jpg", "png"])
  - `max_files`: numero massimo di file (1 per singolo, 2+ per multipli)
- Restituisce percorso file(s) nelle risposte
- I file sono archiviati in `/media/form_uploads/{form-slug}/`
- Caso d'uso: Caricamento di CV, invio di documenti, allegati di foto
- Esempio: "Carica il tuo CV", "Allega documenti di supporto"

**Selettore di Prodotti** (`product_select`):
- Selezione multipla dal tuo catalogo prodotti
- Configurazione:
  - `category_filters`: limita a specifiche categorie (array di ID categoria)
  - `max_selections`: 1 per prodotto singolo, 2+ per multipli
  - `display_mode`: "list" (default) o "grid" (con miniature)
- Restituisce ID/SKU prodotti nelle risposte
- Caso d'uso: Raccomandazioni prodotto, liste dei desideri, sondaggi feedback, pacchetti
- Esempio: "Quali prodotti ti interessano?", "Seleziona i tuoi prodotti preferiti"

**Data** (`date`):
- Interfaccia per selezione data (popup del calendario)
- Restituisce formato ISO (YYYY-MM-DD)
- Validazione: data minima/massima
- Caso d'uso: Date di nascita, date di eventi, prenotazione appuntamenti, scadenze
- Esempio: "Data di Nascita", "Data di Appuntamento Preferita"

**Ora** (`time`):
- Selettore di orario (ore e minuti)
- Restituisce formato orario ISO (HH:MM)
- Caso d'uso: Orari di appuntamento, finestre di disponibilità
- Esempio: "Ora Preferita", "Disponibile Dopo"

**Data & Ora** (`datetime`):
- Selettore combinato di data e orario
- Restituisce data/orario ISO completo
- Caso d'uso: Pianificazione eventi, prenotazione appuntamenti
- Esempio: "Ora di Inizio dell'Evento", "Finestra di Consegna"

## Campi di Layout (Non Input)

**Intestazione di Sezione** (`heading`):
- Testo intestazione per organizzare le sezioni della form
- Configurazione: livello intestazione (h2, h3, h4)
- Nessuna raccolta dati
- Caso d'uso: Suddivisione di form lunghi in sezioni logiche
- Esempio: "Informazioni Personali", "Dettagli di Contatto", "Preferenze"

**Paragrafo Descrittivo** (`paragraph`):
- Blocco di testo ricco per istruzioni o informazioni
- Nessuna raccolta dati
- Supporta formattazione di base (grassetto, corsivo, link)
- Caso d'uso: Istruzioni per passo, disclaimer legali, spiegazioni
- Esempio: Notifica sulla privacy, spiegazione del consenso GDPR

**Linea di Separazione** (`divider`):
- Linea orizzontale visiva separatore
- Nessuna raccolta dati
- Caso d'uso: Organizzazione visiva tra sezioni

**Campo Nascosto** (`hidden`):
- Campo invisibile con valore programmato
- Configurazione: `default_value` (obbligatorio)
- Nessuna etichetta o testo di aiuto mostrato agli utenti
- Caso d'uso: Parametri UTM, dati di tracciamento, ID sessione, codici di riferimento
- Esempio: Campo nascosto con valore proveniente da parametro URL

## Regole di Validazione dei Campi

**Campi Obbligatori**:
- Attiva/disattiva casella "Obbligatorio" nelle impostazioni del campo
- Compare un asterisco rosso (*) accanto all'etichetta
- La form non può essere inviata se i campi obbligatori sono vuoti
- Messaggio personalizzato: "Questo campo è obbligatorio" (o messaggio personalizzato)

**Lunghezza Min/Max** (campi di testo):
- Imposta il numero minimo di caratteri: impedisce risposte troppo corte
- Imposta il numero massimo di caratteri: impedisce input eccessivo
- Esempio: Campo messaggio richiede min 10 caratteri (impedisce risposte tipo "ok")

**Valore Min/Max** (campi numerici):
- Imposta il valore minimo numerico: impedisce età negative, quantità
- Imposta il valore massimo numerico: limita l'input a una gamma ragionevole
- Esempio: Campo età richiede min 18, max 120

**Pattern di Validazione** (regex):
- Espressione regolare personalizzata per validazione complessa
- Pattern comuni:
  - Codice postale: `^{5}(-{4})?$` (formato USA)
  - Telefono: `^{3}{3}-{4}$` (formato USA)
  - Codice prodotto: `^[A-Z]{2}{4}$` (2 lettere, 4 numeri)
- Richiesto un messaggio di errore personalizzato quando si usano i pattern

**Validazione File**:
- Dimensione massima file: impedisce caricamenti pesanti (default 5MB)
- Tipi consentiti: elenco specifico di estensioni (sicurezza)
- Esempio: Campo CV consente ["pdf", "doc", "docx"], max 2MB

## Logica Condizionale

Crea form dinamici dove i campi appaiono/scompaiono in base alle risposte degli utenti:

**Come Funzionano le Regole Condizionali**:
1. L'utente risponde al "campo sorgente" (il trigger)
2. Il sistema valuta la regola: operatore + valore di confronto
3. Se la condizione è vera, l'azione viene eseguita (mostra/nasconde/obbliga campo o passo)
4. Più regole possono concatenarsi (regola A attiva regola B)

**Operatori Disponibili**:
- **Uguale** (`equals`): corrispondenza esatta (es. paese uguale a "US")
- **Non Uguale** (`not_equals`): qualsiasi valore tranne il valore
- **Contiene** (`contains`): testo include sottocarattere (senza distinzione tra maiuscole e minuscole)
- **Maggiore Di** (`greater_than`): confronto numerico (es. età > 18)
- **Minore Di** (`less_than`): confronto numerico (es. valutazione < 3)
- **Vuoto** (`is_empty`): campo non ha valore
- **Non Vuoto** (`is_not_empty`): campo ha qualsiasi valore
- **In Lista** (`in_list`): valore è uno di ["Opzione1", "Opzione2"]

**Azioni Disponibili**:
- **Mostra Campo** - Mostra campo nascosto
- **Nascondi Campo** - Nasconde campo (il valore viene cancellato se nascosto)
- **Obbliga Campo** - Rende il campo obbligatorio
- **Non Obbliga Campo** - Rende il campo opzionale
- **Imposta Valore** - Popola il campo con un valore
- **Mostra Passo** - Mostra passo nascosto (solo per form multi-passo)
- **Nascondi Passo** - Nasconde passo (solo per form multi-passo)
- **Salta a Passo** - Salta a un passo specifico (solo per form multi-passo)

**Esempi di Regole**:
- SE `contact_method` UGUALE A "phone" ALLORA mostra_campo `phone_number`
- SE `rating` MINORE DI "3" ALLORA obbliga_campo `improvement_feedback`
- SE `country` IN_LIST ["US", "CA"] ALLORA mostra_passo `shipping_details`
- SE `budget` MAGGIORE DI "10000" ALLORA mostra_campo `enterprise_features`

**Creare Regole Condizionali**:
1. Clicca sul tab "Regole Condizionali" nel pannello di destra
2. Clicca su "Aggiungi Regola"
3. Seleziona il campo sorgente (trigger)
4. Seleziona l'operatore (come confrontare)
5. Inserisci il valore di confronto (contro cui confrontare)
6. Seleziona l'azione (cosa fare)
7. Seleziona l'obiettivo (campo o passo interessato)
8. Opzionale: Imposta la priorità (le regole con priorità più alta vengono valutate prima)
9. Salva la regola

**Priorità delle Regole**:
- Numeri più alti vengono valutati prima (priorità 100 prima di priorità 10)
- Usa la priorità quando le regole si contraddicono o si concatenano
- Esempio: Regola A (priorità 100) mostra il campo, Regola B (priorità 50) lo obbliga (A viene eseguita prima, quindi B)

## Pattern dei Campi Comuni

**Form di Contatto**:
- Nome Completo (testo, obbligatorio)
- Email (email, obbligatorio)
- Telefono (telefono)
- Soggetto (selezione con opzioni: "Vendite", "Supporto", "Partnership")
- Messaggio (textarea, obbligatorio, min 10 caratteri)

**Feedback sul Prodotto**:
- Prodotto (product_select, selezione singola)
- Valutazione Generale (rating_stars, 5 stelle)
- Condizionale: SE valutazione < 3 ALLORA obbliga "Cosa possiamo migliorare?" (textarea)
- Raccomandazione (rating_nps)

**Candidatura al Lavoro**:
- Passo 1: Personale (nome, email, telefono)
- Passo 2: Curriculum Vitae (caricamento file, consente ["pdf", "doc"], max 2MB)
- Passo 3: Disponibilità (data di inizio, gruppo di caselle di controllo per giorni lavorativi)
- Condizionale: SE "years_experience" > 5 ALLORA mostra_campo "esperienza_di_leader"

## Consigli

- **Utilizza i tipi di campo appropriati** - Campo email per email (non testo), fornisce validazione e tastiere mobili migliore
- **Mantieni le etichette brevi** - Usa il testo di aiuto per i dettagli, non le etichette
- **Raggruppa i campi correlati** - Usa intestazioni e linee di separazione per un'organizzazione visiva
- **Testa la validazione** - Anteprima la form e prova a inviare dati non validi
- **Limita le dimensioni di caricamento file** - Massimo 5MB per prevenire sovraccarico del server da file grandi
- **Utilizza la logica condizionale con moderazione** - Troppi regole confondono gli utenti; mantieni le form semplici
- **Imposta valori massimi realistici** - Massimo età di 120, massimo quantità di 100 (prevenire errori di digitazione come 1000)
- **Fornisci esempi di pattern** - Se si utilizza la validazione regex, mostra un esempio nel testo di aiuto
- **Rende evidenti i campi obbligatori** - Nome e email per form di contatto, sempre obbligatori
- **Utilizza pulsanti radio per 2-4 opzioni** - Seleziona per 5+ opzioni (migliora l'esperienza utente)
- **Campi a metà larghezza per input brevi** - Telefono e codice postale possono essere a metà larghezza, risparmia spazio verticale
- **Selezionatori di prodotti per liste dei desideri** - Permette ai clienti di selezionare più prodotti per le raccomandazioni

Ricorda: Preserva tutto il formattaggio markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici esattamente come mostrato nelle regole di conservazione.