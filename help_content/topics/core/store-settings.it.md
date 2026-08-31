---
title: Configurazione delle impostazioni del negozio
---

Le impostazioni del negozio rappresentano il luogo centrale per configurare l'identità, la localizzazione, la marca e le preferenze operative del tuo negozio. Vai a **Impostazioni > Impostazioni del negozio** per iniziare.

![Scheda delle impostazioni generali del negozio](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Scheda Generale

La **Scheda Generale** contiene le impostazioni principali per l'identità del tuo negozio.

### Identità del negozio

- **Nome del negozio** — Il nome visualizzato nei titoli delle pagine, negli email e nell'intestazione dell'amministratore.
- **Slogan** — Una breve descrizione del tuo negozio, utilizzata per l'ottimizzazione SEO e il condividi sui social.
- **URL del sito** — L'indirizzo web pubblico del tuo negozio. Viene utilizzato negli email, nella generazione della mappa del sito e nel collegamento.

### Informazioni di contatto

- **Email di contatto** — Riceve le notifiche degli ordini e viene visualizzata nelle comunicazioni con i clienti.
- **Numero di telefono** — Numero di telefono opzionale per il supporto visualizzato nel piè di pagina e negli email.

### Indirizzo aziendale

Inserisci il tuo indirizzo completo (via, città, stato, CAP, paese). Viene utilizzato per:
- Calcoli per l'origine spedizione
- Calcoli per le tasse
- Obblighi legali e fatture

## Marchio

### Logo

Carica il logo del tuo negozio (PNG o SVG consigliati, dimensioni ~200x50px con sfondo trasparente). Il logo viene visualizzato in:
- L'intestazione del negozio
- I modelli di email
- Il pannello amministrativo

### Icona (Favicon)

Carica un'icona quadrata (ICO o PNG, 32x32px). Viene visualizzato come:
- Icona della scheda del browser
- Icona del segnalibro
- Icona del desktop mobile

## Localizzazione

### Lingua predefinita

Scegli la lingua principale del tuo negozio tra 10 opzioni supportate:

| Lingua | Codice |
|----------|------|
| Inglese | en |
| Spagnolo | es |
| Francese | fr |
| Tedesco | de |
| Portoghese | pt |
| Giapponese | ja |
| Cinese semplificato | zh-hans |
| Cinese tradizionale | zh-hant |
| Russo | ru |
| Arabo | ar |

La lingua predefinita controlla la lingua dell'interfaccia amministrativa e la riserva per i contenuti del negozio.

### Fuso orario

Seleziona il fuso orario del tuo negozio per ottenere timestamp degli ordini precisi, promozioni programmate e report.

### Valuta

- **Valuta predefinita** — La valuta principale per i prezzi e la contabilità.
- **Multi-valuta** — Attiva per consentire ai clienti di visualizzare i prezzi nella valuta preferita con conversione automatica utilizzando tassi di cambio in tempo reale.

Configura ulteriori valute in **Impostazioni > Impostazioni del negozio > Valuta**.

## Impostazioni per l'e-commerce

### Acquisto senza account

Consenti acquisti senza creare un account:
- Flusso di checkout più veloce
- Minor attrito per i clienti per la prima volta
- Cattura di meno dati dei clienti

### Tempo di creazione account

Controlla quando i clienti vengono invitati a creare un account:

| Opzione | Descrizione |
|--------|-------------|
| **Dopo l'acquisto (consigliato)** | Invito per la creazione di un account dopo un ordine riuscito — sfrutta la buona volontà post-acquisto per la migliore conversione |
| **Durante il checkout** | Crea un account prima del pagamento |
| **Prima del checkout** | Richiedi un account prima dello shopping (non consigliato - riduce la conversione) |

Puoi inoltre impostare un messaggio personalizzato **Account Creation Message** per spiegare i vantaggi della registrazione.

### Impostazioni di default per l'inventario

- **Traccia l'inventario** — Attiva il monitoraggio globale del magazzino
- **Soglia di magazzino basso** — Il livello di magazzino al quale vengono inviate le notifiche di magazzino basso all'email dell'amministratore (valore predefinito: 10 unità)

## Intelligenza dell'inventario

![scheda Intelligenza dell'inventario che mostra i campi Default Reorder Lead Time, Safety Stock Multiplier, Velocity Calculation Window, Allow Backorders by Default, e Low Stock Alert Frequency](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Queste impostazioni regolano i calcoli automatici di rifornimento, stock di sicurezza e velocità di vendita, e controllano come vengono gestite le situazioni di esaurimento e stock basso.

- **Default Reorder Lead Time (Giorni)** — Quanti giorni ci vorrebbero tipicamente per ricevere il rifornimento dal tuo fornitore una volta che ordini (valore predefinito: 14).

La previsione utilizza questo per segnalare i prodotti che necessitano di un rifornimento immediato per evitare un'esaurimento prima che il nuovo stock arrivi.
- **Moltiplicatore di Sicurezza** — Un buffer applicato sopra la domanda attesa per assorbire picchi di vendite o ritardi del fornitore.

Ad esempio, un moltiplicatore di `1.5` aggiunge un buffer del 50% rispetto al tuo stock di sicurezza calcolato; `2.0` lo raddoppia.

Aumenta questo valore per i prodotti dove l'esaurimento è costoso (best seller, articoli stagionali); riducilo per gli articoli a bassa rotazione che non vuoi ordinare in eccesso.
- **Finestra di Calcolo della Velocità (Giorni)** — La finestra di riferimento che Spwig utilizza per calcolare la velocità di vendita di ciascun prodotto, che a sua volta determina le raccomandazioni per il rifornimento e i dati sulle scorte (valore predefinito: 30).

Una finestra più breve reagisce più velocemente ai cambiamenti recenti della domanda; una finestra più lunga smussa i picchi stagionali in modo che una singola settimana affollata non distorca la previsione.
- **Consenti gli Ordini in Backorder di Default** — Il settaggio iniziale per gli ordini in backorder applicato ai nuovi prodotti (disattivato per default).

Ogni prodotto può comunque sovrascrivere questo settaggio singolarmente sulla propria pagina prodotto, e i prodotti esistenti mantengono qualsiasi settaggio abbiano già — modificare questo settaggio cambia solo il default con cui i nuovi prodotti iniziano, non aggiorna retroattivamente il tuo catalogo.
- **Frequenza delle Notifiche per Scorte Basse** — Quanto spesso l'app mobile di Spwig riceve notifiche per scorte basse: **In tempo reale** invia una notifica push non appena un prodotto supera il proprio limite di scorte basse; **Riepilogo Giornaliero** e **Riepilogo Setimanale** inviano invece una singola notifica di sintesi che riassume tutti i prodotti attualmente in scorte basse su quel programma.

Questo settaggio ha effetto solo mentre **Notifiche per Scorte Basse** (Impostazioni Email, sotto) è attivo — con gli avvisi disattivati, nessuna notifica viene inviata su alcuna frequenza.

### Documenti & Fatturazione

![Scheda Documenti & Fatturazione che mostra i campi ID fiscale / Numero P.IVA, Testo piè di fattura, Testo piè di lettera di vettura e Larghezza Logo Documento compilati con valori di esempio](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Questi campi popolano le fatture e le lettere di vettura che Spwig genera per gli ordini — ad esempio quando un commerciante scarica o invia via email una fattura in PDF, o stampa una lettera di vettura per una spedizione.

- **ID fiscale / Numero P.IVA** — Il tuo numero di identificazione fiscale aziendale. Stampa sulle fatture generate in modo che siano conformi ai requisiti locali per la documentazione fiscale.
- **Testo piè di fattura** — Testo libero visualizzato in fondo a ogni fattura generata. Esempi comuni: termini di pagamento ("Pagamento entro 30 giorni"), un messaggio di ringraziamento o i dettagli per un bonifico bancario.
- **Testo piè di lettera di vettura** — Testo libero visualizzato in fondo a ogni lettera di vettura generata. Esempi comuni: istruzioni per il reso o un messaggio per il team di magazzino/fulfillment.
- **Larghezza Logo Documento (px)** — La larghezza del logo del tuo negozio come appare sulle fatture e lettere di vettura in PDF generate (valore predefinito: 200px). L'altezza si adatta automaticamente per mantenere le proporzioni del logo. L'immagine del logo proviene comunque dal tuo **Logo** (Brand, sopra) — i loghi SVG non vengono disegnati sui documenti PDF, quindi carica una versione PNG o JPG del tuo logo se utilizzi un disegno vettoriale sul negozio.

## Impostazioni Email

Configura le impostazioni di invio email in **Impostazioni > Account Email** e **Impostazioni > Modelli Email**. Consulta [Configurazione Email](/help/email-configuration) per i dettagli completi.

Impostazioni email chiave disponibili nelle Impostazioni del Negozio:

- **Email di Conferma Ordine** — Attiva o disattiva le email di conferma automatiche
- **Email di Notifica Spedizione** — Attiva o disattiva le notifiche sugli aggiornamenti di spedizione
- **Avvisi per Scorte Basse** — Invia avvisi all'email amministrativa quando le scorte scendono sotto la soglia
- **Modalità di Invio Email** — Live (consegna normale), Fermato (tieni tutte le email), o Solo Registra (registra ma non invia mai)
- **Email di Ridirittura di Prova** — Tutte le email in uscita vengono indirizzate a un indirizzo unico per il test

## Impostazioni Sicurezza

### Autenticazione a Due Fattori (2FA)

Controlla se i dipendenti devono utilizzare l'autenticazione a due fattori:

Mantieni tutti i formati markdown, i percorsi immagine, i blocchi di codice e i termini tecnici.

| Impostazione | Descrizione |
|---------|-------------|
| **Facoltativo** | Il personale può scegliere di abilitare 2FA, ma non è obbligatorio |
| **Consigliato** | Il personale visualizza un prompt che li incoraggia a configurare 2FA |
| **Obbligatorio** | Il personale non può accedere all'admin finché 2FA non è abilitato |

- **Periodo di grazia (giorni)** — Numero di giorni che il personale ha a disposizione per configurare 2FA dopo l'attivazione dell'obbligo
- **Consenti dispositivi fidati** — Consente al personale di saltare la verifica 2FA su dispositivi riconosciuti per un numero predefinito di giorni

## Consenso Cookie

Configura il banner di consenso cookie mostrato ai visitatori dello storefront:

- **Consenso Cookie Abilitato** — Mostra o nasconde il banner dei cookie
- **Posizione del Banner** — Dove appare il banner sullo schermo (barra inferiore, popup nell'angolo, ecc.)
- **Modalità di Consenso** — Notifica semplice, opt-in o opt-out
- **Titolo e Testo del Banner** — Intestazione e descrizione personalizzabili mostrate ai visitatori
- **Descrizioni delle Categorie** — Descrizioni separate per cookie analitici, di marketing e funzionali

Tutti i campi di testo del banner supportano le traduzioni per i negozi multilingua.

## Comunicazioni

La scheda **Comunicazioni** controlla come il tuo negozio ottiene, conferma e consente ai clienti di gestire il consenso per email e SMS di marketing. Queste impostazioni definiscono la tua postura di conformità legale (GDPR per le email, TCPA per gli SMS), quindi rilevale con il tuo legale prima del lancio — Spwig fornisce i controlli, non i consigli.

![Scheda Comunicazioni che mostra le card Consenso Email Marketing, Preferenze e Disiscrizione e Consenso SMS](/static/core/admin/img/help/store-settings/communications-tab.webp)

### Consenso Email Marketing

- **Abilita Double Opt-In per le Email di Marketing** — Quando attivo, a un cliente che si iscrive alle email di marketing viene inviata un'email di conferma e deve cliccare il link contenuto al suo interno prima che Spwig gli invii qualsiasi messaggio di marketing. Quando disattivo, spuntare la casella di opt-in per il marketing è sufficiente di per sé. Abilitato per impostazione predefinita, in linea con le migliori pratiche GDPR.
- **Stato Predefinito di Opt-In Marketing** — Lo stato iniziale di opt-in marketing applicato ai nuovi account cliente creati. Disattivato per impostazione predefinita (opt-out GDPR), quindi i nuovi clienti iniziano non iscritti alle email di marketing finché non si iscrivono attivamente.

Quando il double opt-in è attivo, l'iscrizione attiva un'email di conferma con un link di verifica. Finché il cliente non lo clicca, viene registrato come iscritto ma non confermato, e le invii di marketing lo saltano — le email transazionali (conferme ordine, aggiornamenti di spedizione, reset password) non sono mai influenzate da questa impostazione.

### Preferenze e Disiscrizione

- **Abilita Centro Preferenze Cliente** — Quando attivo, i clienti possono gestire le proprie preferenze email e SMS da una pagina di self-service collegata dalla loro dashboard account. Quando disattivo, quella pagina e la sua API di supporto restituiscono non disponibile e il link nella dashboard viene nascosto. I link di disiscrizione con un clic nelle tue email continuano a funzionare in entrambi i casi — quella via di fuga è richiesta per la conformità e non è influenzata da questa opzione.
- **Raccogli Motivi di Disiscrizione** — Quando attivo, la pagina di disiscrizione con un clic chiede al cliente un breve motivo prima di confermare: *Ricevo troppe email*, *Il contenuto non è rilevante per me*, *Non mi sono mai iscritto a questo*, *Non sono più interessato*, o *Altro*. Il motivo selezionato dal cliente viene registrato nella traccia di audit del consenso in modo da poter rivedere i modelli di disiscrizione nel tempo.

### Consenso SMS

- **Richiedi Verifica SMS** — Quando attivo (impostazione predefinita), un cliente deve verificare il proprio numero di telefono con un codice monouso prima che Spwig gli invii qualsiasi SMS, inclusi i testi di marketing. Quando disattivo, spuntare la casella di opt-in SMS è sufficiente di per sé per iniziare a inviare. Questa impostazione predefinita è stata cambiata a **attivo** per la sicurezza TCPA — disattivala solo se hai un altro passaggio di verifica nel tuo flusso di registrazione.

## Modalità di Manutenzione

Abilita la modalità di manutenzione per mettere il tuo negozio offline temporaneamente:
- Visualizza un messaggio di manutenzione personalizzato ai visitatori
- Puoi collegare una **Pagina di Manutenzione** creata nel Page Builder per un'esperienza di manutenzione completamente brandizzata
- Limita l'accesso solo agli utenti admin
- Utile durante aggiornamenti importanti o migrazioni

## Social Media

Collega i profili dei social media del tuo negozio. Appaiono nel piè di pagina e nei modelli di email:

- **URL Facebook**
- **URL Twitter**
- **URL Instagram**
- **URL LinkedIn**

## Impostazioni SEO

Imposta i tag meta predefiniti utilizzati quando le pagine non hanno le proprie impostazioni SEO:

- **Titolo Meta** — Titolo predefinito della pagina (massimo 60 caratteri)
- **Descrizione Meta** — Descrizione predefinita visualizzata nei risultati di ricerca (massimo 160 caratteri)
- **Parole chiave Meta** — Parole chiave predefinite separate da virgola

## Impostazioni sulle tasse

Configura la riscossione delle tasse a **Impostazioni > Impostazioni sulle tasse**:

1. **Metodo di calcolo** — Per indirizzo di spedizione, indirizzo di fatturazione o posizione del negozio
2. **Aliquote fiscali** — Definisci aliquote in base alla regione e alla classe di prodotto soggetta a tasse
3. **Visualizzazione prezzi** — Mostra prezzi con tasse, senza tasse o entrambi

## Suggerimenti

- Imposta correttamente il fuso orario prima di elaborare qualsiasi ordine — influisce su tutti i timestamp e sui report.
- Abilita il checkout come ospite per migliorare i tassi di conversione.
- Compila l'indirizzo aziendale per calcoli precisi di spedizione e tasse.
- Carica sia un logo che un favicon per un'esperienza professionale e marchiata.
- Usa la tempistica di creazione del account **Dopo l'acquisto** per ottenere tassi di registrazione migliori.
- Abilita l'enforcement dell'autenticazione a due fattori per il personale per proteggere l'amministrazione del negozio.
- Testa i flussi email utilizzando l'impostazione **Reindirizzamento email di prova** prima di andare in produzione.
- Imposta la **Tempistica predefinita per il riordino** per corrispondere al fornitore più lento — la previsione del riordino applica questo singolo valore su tutto il tuo catalogo, quindi procedi con il prodotto con il tempo di consegna più lungo.
- Riduci la **Finestra di calcolo della velocità** se effettui promozioni o rifornimenti frequenti e vuoi che la previsione reagisca velocemente agli ultimi giorni di vendite; allargala per una visione più costante e meno soggetta a picchi della domanda.
- Se attivi **Consenti ordinazioni in ritardo di default**, ricorda che imposta solo il punto di partenza per i prodotti creati *dopo* il cambiamento — torna sui prodotti esistenti singolarmente se vuoi attivare le ordinazioni in ritardo su tutto il tuo catalogo attuale.
- Abbinare la **Frequenza delle notifiche di scorte basse** a come gestisci attivamente le scorte: **In tempo reale** per cataloghi a movimento rapido dove ogni rischio di esaurimento deve essere gestito immediatamente, **Riepilogo giornaliero** o **Riepilogo settimanale** per evitare la stanchezza delle notifiche su un catalogo più ampio.
- Compila la tua **ID tassa / Numero IVA** e il testo del piè di pagina prima che vada in produzione la tua prima fattura reale per un cliente — entrambi i campi sono vuoti di default.
- Se il tuo **Logo** è un SVG, carica anche una versione PNG o JPG — la **Larghezza del logo del documento** non ha effetto sui PDF perché Spwig non può disegnare l'arte SVG sui modelli di fatture e fogli di imballaggio generati.
- Lascia **Abilita conferma doppia per le email di marketing** attivo a meno che tu non abbia un motivo specifico per disattivarlo — è il default più sicuro per il GDPR e protegge la reputazione del mittente mantenendo gli indirizzi non verificati lontani dalle tue email di marketing.
- Lascia **Stato predefinito per l'adesione alle email di marketing** disattivato. Selezionare automaticamente il consenso per le email di marketing per nuovi account compromette il requisito del consenso del GDPR anche se un cliente potrebbe tecnicamente deselezionarlo.
- Non disattivare **Abilita Centro delle preferenze dei clienti** solo per semplificare il pannello account — senza di esso, i clienti possono comunque annullare l'iscrizione a un singolo tipo di messaggio, ma perdono la capacità di regolare le preferenze in modo più preciso (es. mantenere gli aggiornamenti di spedizione ma eliminare la newsletter).
- Mantieni **Richiedi verifica SMS** attivo a meno che il flusso di iscrizione non confermi già un altro modo i numeri di telefono (es. accesso basato su SMS) — l'impostazione esiste appositamente per tenerti all'interno delle regole TCPA.

## Risoluzione dei problemi

**Le modifiche non appaiono sul negozio:**
- Cancella la cache del browser
- Esegui una cancellazione cache dal pannello amministrativo
- Verifica se la modalità manutenzione è attiva accidentalmente

**Le email non vengono inviate:**
- Verifica le impostazioni del provider email nel **Configurazione email**
- Controlla che l'**Modalità di invio email** sia impostata su **Live**
- Assicurati che l'**Email di reindirizzamento di prova** sia vuota se vuoi che le email vengano inviate a destinatari reali

**La conversione della valuta non funziona:**
- Verifica che il tuo fornitore dei tassi di cambio sia connesso
- Controlla le credenziali API nelle impostazioni del tasso di cambio
- Prova a aggiornare i tassi manualmente

**Le email di marketing non arrivano ai clienti che si sono iscritti:**
- Verifica se **Abilita doppia conferma per le email di marketing** è attivo — se sì, il cliente deve cliccare sul collegamento di conferma nell'email di verifica prima che la mail di marketing riprenda
- Chiedi al cliente di controllare la cartella della posta indesiderata per l'email di conferma
- Conferma che l'iscrizione del cliente alle email di marketing è ancora attiva nelle sue preferenze — un clic su annulla iscrizione la disattiva

**I clienti dicono che non riescono a trovare il centro preferenze:**
- Verifica che **Abilita centro preferenze clienti** sia attivo — quando è disattivato, il collegamento del pannello di controllo è nascosto e la pagina non è disponibile di proposito
- Il collegamento per annullare l'iscrizione in qualsiasi email di marketing funziona sempre, indipendentemente da questo settaggio, quindi indica ai clienti di andare su di esso come opzione di riserva