---
title: Configurazione delle impostazioni del negozio
---

Le impostazioni del negozio rappresentano il punto centrale per configurare l'identità, la localizzazione, la marca e le preferenze operative del tuo negozio. Vai a **Impostazioni > Impostazioni del negozio** per iniziare.

![scheda generale delle impostazioni del negozio](/static/core/admin/img/help/store-settings/store-settings-general.webp)

## Scheda Generale

La **scheda Generale** contiene le impostazioni principali per l'identità del tuo negozio.

### Identità del Negozio

- **Nome del Negozio** — Il nome visualizzato nei titoli delle pagine, negli email e nell'intestazione dell'amministratore.
- **Slogan** — Una breve descrizione del tuo negozio, utilizzata per l'ottimizzazione SEO e il condividi sui social.
- **URL del Sito** — L'indirizzo web pubblico del tuo negozio. Viene utilizzato negli email, nella generazione della mappa del sito e nel collegamento.

### Informazioni di Contatto

- **Email di Contatto** — Riceve le notifiche degli ordini e viene visualizzata nelle comunicazioni con i clienti.
- **Numero di Telefono** — Numero di telefono opzionale per il supporto visualizzato nel piè di pagina e negli email.

### Indirizzo Aziendale

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

### Lingua Predefinita

Scegli la lingua principale del tuo negozio tra 10 opzioni supportate:

| Lingua | Codice |
|----------|------|
| Inglese | en |
| Spagnolo | es |
| Francese | fr |
| Tedesco | de |
| Portoghese | pt |
| Giapponese | ja |
| Cinese Semplice | zh-hans |
| Cinese Tradizionale | zh-hant |
| Russo | ru |
| Arabo | ar |

La lingua predefinita controlla la lingua dell'interfaccia amministrativa e la riserva per i contenuti del negozio.

### Fuso Orario

Seleziona il fuso orario del tuo negozio per ottenere timestamp degli ordini precisi, promozioni programmate e report.

### Valuta

- **Valuta Predefinita** — La valuta principale per i prezzi e la contabilità.
- **Multi-Valuta** — Attiva per consentire ai clienti di visualizzare i prezzi nella valuta preferita con conversione automatica utilizzando tassi di cambio in tempo reale.

Configura valute aggiuntive in **Impostazioni > Impostazioni del negozio > Valuta**.

## Impostazioni E-Commerce

### Acquisto senza Account

Consenti acquisti senza creare un account:
- Flusso di checkout più veloce
- Minor attrito per i clienti per la prima volta
- Cattura di meno dati dei clienti

### Tempo di Creazione Account

Controlla quando i clienti vengono invitati a creare un account:

| Opzione | Descrizione |
|--------|-------------|
| **Dopo l'acquisto (Consigliato)** | Invito per la creazione di un account dopo un ordine riuscito — sfrutta la buona volontà post-acquisto per la migliore conversione |
| **Durante il checkout** | Creare un account prima del pagamento |
| **Prima del checkout** | Richiedere un account prima dello shopping (non consigliato - riduce la conversione) |

Puoi inoltre impostare un messaggio personalizzato **Crea Account** per spiegare i vantaggi della registrazione.

### Impostazioni di Gestione Magazzino

- **Traccia il Magazzino** — Attiva il monitoraggio globale del magazzino
- **Soglia di Scarsa Scorta** — Il livello di scorte a cui vengono inviate le notifiche di scarsezza all'email dell'amministratore (valore predefinito: 10 unità)

## Intelligenza del Magazzino

![scheda Intelligenza del Magazzino che mostra i campi Tempo di Riapprovvigionamento Predefinito e Moltiplicatore Scorte di Sicurezza](/static/core/admin/img/help/store-settings/ecommerce-inventory-intelligence.webp)

Queste impostazioni regolano i calcoli automatici di riapprovvigionamento, scorte di sicurezza e velocità di vendita, e controllano come vengono gestite le situazioni di sottoscorta e scarsa scorta.

- **Tempo di Riapprovvigionamento Predefinito (giorni)** — Quanti giorni ci vorrebbero tipicamente per ricevere il rifornimento dal tuo fornitore una volta che hai effettuato l'ordine (valore predefinito: 14).

La previsione utilizza questo valore per segnalare i prodotti che devono essere riordinati *ora* per evitare un'esaurimento prima che il nuovo stock arrivi.
- **Moltiplicatore Scorte di Sicurezza** — Un buffer applicato sopra la domanda prevista per assorbire picchi di vendita o ritardi del fornitore.

Ad esempio, un moltiplicatore di `1.5` include un buffer del 50% rispetto al tuo inventario di sicurezza calcolato; `2.0` lo raddoppia.

Aumenta questo valore per i prodotti in cui esaurirsi è costoso (best seller, articoli stagionali); riducilo per gli articoli a scarse vendite che non si vuole ordinare in eccesso.
- **Finestra di calcolo della velocità (giorni)** — La finestra di riferimento che Spwig utilizza per calcolare la velocità di vendita di ciascun prodotto, che a sua volta determina le raccomandazioni per il riordino e i valori dei giorni di scorta (valore predefinito: 30).

Una finestra più breve reagisce più velocemente ai cambiamenti recenti della domanda; una finestra più lunga smussa i picchi stagionali, in modo che una singola settimana di attività non comprometta la previsione.
- **Consenti gli ordini in backorder di default** — Il settaggio iniziale per gli ordini in backorder applicato ai nuovi prodotti (disattivato per impostazione predefinita).

Ogni prodotto può comunque sovrascrivere questo settaggio singolarmente sulla propria pagina prodotto, e i prodotti esistenti mantengono il settaggio che avevano già — modificare questo settaggio cambia solo il default con cui i nuovi prodotti iniziano, non aggiorna retroattivamente il tuo catalogo.
- **Frequenza delle notifiche per scorte basse** — Quanto spesso l'app mobile Spwig riceve notifiche per scorte basse: **In tempo reale** invia una notifica push non appena un prodotto supera il proprio limite di scorte basse; **Riepilogo giornaliero** e **Riepilogo settimanale** inviano invece una singola notifica push che riassume tutti i prodotti attualmente in scorte basse su quel programma.

Questo settaggio è attivo solo quando **Notifiche per scorte basse** (Impostazioni email, qui sotto) è abilitato — con gli avvisi disattivati, non vengono inviate notifiche su alcuna frequenza.

### Documenti e fatture

![scheda Documenti e Fatture che mostra i campi ID fiscale / Numero P.IVA, Testo piè di fattura e Testo piè di documento di imballaggio compilati con valori di esempio](/static/core/admin/img/help/store-settings/ecommerce-documents-invoicing.webp)

Questi campi popolano le fatture e i documenti di imballaggio che Spwig genera per gli ordini — ad esempio quando un commerciante scarica o invia via email una fattura PDF, oppure stampa un documento di imballaggio per una spedizione.

- **ID fiscale / Numero P.IVA** — Il numero di identificazione fiscale aziendale. Stampa sulle fatture generate in modo che siano conformi ai requisiti locali per la documentazione fiscale.
- **Testo piè di fattura** — Testo libero visualizzato in fondo a ogni fattura generata. Esempi d'uso comune: termini di pagamento ("Pagamento entro 30 giorni"), un messaggio di ringraziamento o i dettagli per un bonifico bancario.
- **Testo piè di documento di imballaggio** — Testo libero visualizzato in fondo a ogni documento di imballaggio generato. Esempi d'uso comune: istruzioni per il reso o un messaggio al team di magazzino/fulfillment.
- **Larghezza logo documento (px)** — La larghezza del logo del tuo negozio come appare su fatture e documenti di imballaggio PDF generati (valore predefinito: 200px). L'altezza si adatta automaticamente per mantenere le proporzioni del logo. L'immagine del logo proviene dalla tua **Logo** (Brand, sopra) — i loghi SVG non vengono disegnati sui documenti PDF, quindi carica una versione PNG o JPG del tuo logo se utilizzi un disegno vettoriale sul negozio.

## Impostazioni Email

Configura le impostazioni di invio email in **Impostazioni > Account Email** e **Impostazioni > Modelli Email**. Consulta [Configurazione Email](/help/email-configuration) per i dettagli completi.

Impostazioni email chiave disponibili nelle Impostazioni del Negozio:

- **Email di Conferma Ordine** — Attiva o disattiva le email di conferma automatica
- **Email di Notifica Spedizione** — Attiva o disattiva le notifiche sugli aggiornamenti di spedizione
- **Avvisi per Scorte Basse** — Invia avvisi all'email amministratore quando le scorte scendono sotto la soglia
- **Modalità di Invio Email** — Live (consegna normale), Fermato (tieni tutte le email), o Solo Registra (registra ma non invia)
- **Email di Riferimento di Prova** — Reindirizza tutte le email in uscita a un indirizzo unico per il test

## Impostazioni Sicurezza

### Autenticazione a Due Fattori (2FA)

Controlla se i dipendenti devono utilizzare l'autenticazione a due fattori:

| Impostazione | Descrizione |
|-------------|-------------|
| **Opzionale** | I dipendenti possono scegliere di attivare la 2FA ma non è richiesto |
| **Consigliato** | I dipendenti vedranno una richiesta che li incoraggia a impostare la 2FA |
| **Obbligatorio** | I dipendenti non possono accedere all'amministrazione fino a quando la 2FA non è attivata |

- **Periodo di tolleranza (giorni)** — Il numero di giorni entro cui il personale deve attivare l'autenticazione a due fattori dopo l'attivazione dell'applicazione
- **Consenti dispositivi attendibili** — Consentire al personale di saltare la verifica dell'autenticazione a due fattori su dispositivi riconosciuti per un numero di giorni definito

## Consenso ai cookie

Configura la cornetta di consenso ai cookie visualizzata ai visitatori del negozio:

- **Consenso ai cookie abilitato** — Visualizza o nasconde la cornetta dei cookie
- **Posizione della cornetta** — Dove appare la cornetta a schermo (barra in basso, finestra a comparsa, ecc.)
- **Modalità di consenso** — Notifica semplice, opt-in o opt-out
- **Titolo e testo della cornetta** — Intestazione e descrizione personalizzabili visualizzati ai visitatori
- **Descrizioni delle categorie** — Descrizioni distinte per i cookie analitici, di marketing e funzionali

Tutti i campi del testo della cornetta supportano le traduzioni per i negozi multilingua.

## Comunicazioni

La scheda **Comunicazioni** controlla come il tuo negozio ottiene, conferma e consente ai clienti di gestire il consenso per le email e SMS di marketing. Queste impostazioni definiscono il tuo atteggiamento in termini di conformità legale (GDPR per le email, TCPA per gli SMS), quindi valutale con il tuo consulente legale prima del lancio - Spwig fornisce i controlli, non il consiglio.

![Scheda Comunicazioni che mostra le schede Email di marketing, Preferenze & Annulla iscrizione, e Consenso SMS](/static/core/admin/img/help/store-settings/communications-tab.webp)

### Consenso per la posta elettronica di marketing

- **Abilita doppia conferma per le email di marketing** — Quando attivo, un cliente che si iscrive alle email di marketing riceve un'email di conferma e deve cliccare sul collegamento in essa prima che Spwig gli invii qualsiasi messaggio di marketing. Quando disattivato, l'attivazione della casella di spunta per l'iscrizione alle email di marketing è sufficiente. Abilitato per impostazione predefinita, in linea con le migliori pratiche GDPR.
- **Stato predefinito per l'iscrizione alle email di marketing** — Lo stato iniziale di iscrizione alle email di marketing applicato ai nuovi account clienti. Disattivato per impostazione predefinita (GDPR opt-out), quindi i nuovi clienti iniziano non iscritti alle email di marketing fino a quando non si iscrivono attivamente.

Quando la doppia conferma è attiva, l'iscrizione attiva un'email di conferma con un collegamento di verifica. Fino a quando il cliente non lo clicca, viene registrato come iscritto ma non confermato, e le email di marketing non li coinvolgono - le email transazionali (conferme d'ordine, aggiornamenti sulle spedizioni, reset della password) non vengono mai influenzate da questo settaggio.

### Preferenze & Annulla iscrizione

- **Abilita centro preferenze dei clienti** — Quando attivo, i clienti possono gestire le loro preferenze per email e SMS da una pagina accessibile autonomamente collegata dal pannello del loro account. Quando disattivato, questa pagina e la sua API di supporto restituiscono non disponibili e il collegamento del pannello è nascosto. I collegamenti per l'annulla iscrizione a un clic nelle tue email funzionano comunque - questo sistema di emergenza è richiesto per la conformità e non è influenzato da questo pulsante.
- **Raccogli le ragioni per l'annulla iscrizione** — Quando attivo, la pagina di annullamento iscrizione a un clic richiede al cliente una breve ragione prima della conferma: *Ricevo troppe email*, *Il contenuto non è rilevante per me*, *Non mi sono iscritto a questo*, *Non sono più interessato*, o *Altro*. La ragione scelta dal cliente viene registrata nella traccia del consenso in modo da poter revisionare i modelli di annullamento iscrizione nel tempo.

### Consenso SMS

- **Richiedi la verifica SMS** — Quando attivo (predefinito), un cliente deve verificare il numero del telefono con un codice unico prima che Spwig gli invii qualsiasi SMS, compresi i testi di marketing. Quando disattivato, l'attivazione della casella di spunta per l'iscrizione SMS è sufficiente a iniziare a inviare. Questo default è stato modificato in **attivo** per la sicurezza TCPA - disattivalo solo se hai un altro passo di verifica nel tuo flusso di iscrizione.

## Modalità manutenzione

Abilita la modalità manutenzione per disattivare temporaneamente il tuo negozio:
- Visualizza un messaggio di manutenzione personalizzato ai visitatori
- Puoi collegare una **Pagina di manutenzione** creata nel Page Builder per un'esperienza di marca completa durante la manutenzione
- Limita l'accesso agli utenti amministratori solo
- Utile durante aggiornamenti o migrazioni importanti

## Social media

Collega i profili social del tuo negozio. Appaiono nel piè di pagina e nei modelli di email:

- **URL Facebook**
- **URL Twitter**
- **URL Instagram**
- **URL LinkedIn**

## Impostazioni SEO predefinite

Mantieni tutti i formati markdown, i percorsi immagini, i blocchi di codice e i termini tecnici.

Impostare i tag meta predefiniti utilizzati quando le pagine non dispongono delle proprie impostazioni SEO:

- **Meta Titolo** — Titolo predefinito della pagina (massimo 60 caratteri)
- **Meta Descrizione** — Descrizione predefinita visualizzata nei risultati di ricerca (massimo 160 caratteri)
- **Meta Parole Chiave** — Parole chiave predefinite separate da virgola

## Impostazioni Fiscali

Configurare la riscossione delle tasse a **Impostazioni > Impostazioni Fiscali**:

1. **Metodo di Calcolo** — Per indirizzo di spedizione, indirizzo di fatturazione o posizione del negozio
2. **Aliquote IVA** — Definire aliquote per regione e classe di prodotto fiscale
3. **Visualizzazione Prezzi** — Mostrare i prezzi con l'IVA, senza l'IVA o entrambi

## Suggerimenti

- Imposta correttamente il fuso orario prima di elaborare gli ordini — influisce su tutti i timestamp e sui report.
- Abilita il checkout come ospite per migliorare i tassi di conversione.
- Compila l'indirizzo aziendale per calcoli precisi di spedizione e tasse.
- Carica sia un logo che un favicon per un'esperienza professionale e di marchio.
- Usa la tempistica di creazione del account **Dopo l'acquisto** per i migliori tassi di registrazione.
- Abilita l'enforcement dell'autenticazione a due fattori per il personale per proteggere l'amministrazione del negozio.
- Testa i flussi email utilizzando l'impostazione **Test Redirect Email** prima di andare in produzione.
- Imposta il **Tempo di Riacquisto Predefinito** per corrispondere al fornitore più lento — la previsione del riordino applica questo singolo valore su tutto il tuo catalogo, quindi procedi con il prodotto con il tempo di consegna più lungo.
- Compila la tua **ID Fiscale / Numero P.IVA** e il testo del piè di pagina prima che vada in produzione la tua prima fattura reale a un cliente — entrambi i campi sono vuoti per impostazione predefinita.
- Lascia attivo **Abilita Conferma Doppia per le Email di Marketing** a meno che non tu abbia un motivo specifico per disattivarlo — è la scelta predefinita più sicura per il GDPR e protegge la reputazione del mittente tenendo fuori le email non verificate.
- Lascia **Stato Predefinito per l'adesione al Marketing** spento. Selezionare automaticamente l'accettazione del marketing per nuovi account compromette il requisito GDPR per l'adesione, anche se un cliente potrebbe tecnicamente deselezionarla.
- Non disattivare **Abilita Centro delle Preferenze dei Clienti** solo per semplificare il tuo pannello account — senza di esso, i clienti possono comunque disiscriversi da un singolo tipo di messaggio, ma perdono la capacità di regolare le preferenze in modo più preciso (es. mantenere gli aggiornamenti di spedizione ma eliminare la newsletter).
- Mantieni **Richiedi Verifica SMS** attivo a meno che il flusso di iscrizione non confermi già i numeri di telefono in un altro modo (es. accesso basato su SMS) — l'impostazione esiste appositamente per tenerti all'interno delle regole TCPA.

## Risoluzione dei Problemi

**Le modifiche non appaiono sul negozio:**
- Cancella la cache del browser
- Esegui una cancellazione cache dal pannello amministrativo
- Verifica se la modalità manutenzione è attiva accidentalmente

**Le email non vengono inviate:**
- Verifica le impostazioni del tuo provider email nella configurazione email
- Controlla che l'**Modalità di Invio Email** sia impostata su **Live**
- Assicurati che l'**Email di Reindirizzamento di Prova** sia vuota se desideri che le email vengano inviate a destinatari reali

**La conversione della valuta non funziona:**
- Verifica che il tuo fornitore di tassi di cambio sia connesso
- Controlla le credenziali API nelle impostazioni del tasso di cambio
- Prova a aggiornare i tassi manualmente

**Le email di marketing non raggiungono i clienti che si sono iscritti:**
- Verifica se **Abilita Conferma Doppia per le Email di Marketing** è attivo — se sì, il cliente deve cliccare sul collegamento di conferma nell'email di verifica prima che le email di marketing riprendano
- Chiedi al cliente di verificare la cartella spam/posta indesiderata per l'email di conferma
- Conferma che l'adesione al marketing del cliente è ancora attiva nelle sue preferenze — un clic di disiscrizione la riporta a zero

**I clienti dicono che non riescono a trovare il centro preferenze:**
- Verifica che **Abilita Centro delle Preferenze dei Clienti** sia attivo — quando è disattivato, il collegamento del pannello è nascosto e la pagina non è disponibile per impostazione predefinita
- Il collegamento di disiscrizione in qualsiasi email di marketing funziona comunque, indipendentemente da questa impostazione, quindi indica ai clienti di andare su di esso come backup