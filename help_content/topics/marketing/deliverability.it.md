---
title: Runbook per la consegnabilità delle email
---

Inviare un'email è facile. Farla arrivare nella casella di posta in arrivo invece che nella cartella spam è il vero lavoro — e i provider di caselle di posta come Gmail e Yahoo applicano ora requisiti tecnici rigorosi prima di considerarla. Questo runbook illustra cosa configurare, in quale ordine, affinché le tue conferme d'ordine e le campagne arrivino dove i clienti possono vederle.

Nessuna di queste operazioni è un compito da eseguire una sola volta. La consegnabilità è una reputazione che si costruisce nel tempo e si può perdere rapidamente — l'elenco di controllo alla fine vale la pena di essere rivisto ogni volta che qualcosa sembra fuori posto.

## Perché è importante

Ogni grande provider di caselle di posta valuta le email in entrata in base alla reputazione del mittente prima di decidere se consegnarle, spostarle nella cartella spam o rifiutarle del tutto. Dal 2024, Gmail e Yahoo hanno formalizzato questo processo in **requisiti espliciti per i mittenti in bulk** per chiunque invii un volume significativo:

- **Autenticare il tuo dominio** — record SPF, DKIM e DMARC validi.
- **Rendere facile la disiscrizione** — un opt-out funzionante e a bassa frizione in ogni email di marketing.
- **Mantenere bassi i reclami per spam** — i mittenti in bulk che superano circa lo 0,3% di reclami rischiano di avere le email rifiutate o spostate direttamente nella cartella bulk; l'obiettivo più sicuro è ben sotto lo 0,1%.

Se non si soddisfano questi requisiti, a risentirne non sono solo le campagne di marketing — una reputazione del dominio danneggiata può trascinare anche le email transazionali (conferme d'ordine, reset della password) nella cartella spam, poiché Gmail e Yahoo giudicano sempre più la reputazione a livello di dominio di invio, non solo per tipo di messaggio. I passaggi seguenti illustrano come soddisfare tutti e tre i requisiti.

## Passaggio 1: Autenticare il tuo dominio di invio

SPF, DKIM e DMARC sono record TXT DNS che dimostrano ai server di posta in ricezione che le email che dichiarano di provenire dal tuo dominio sono state effettivamente inviate da te. Il modo in cui li configuri dipende dalla modalità di invio utilizzata dal tuo store — tutti e tre sono configurati sotto **Configurazione email** nella barra laterale di amministrazione (questo apre l'elenco degli account email; consulta [Configurazione email](email-configuration) per la guida completa alla configurazione dell'account).

| Modalità di invio | Come funziona l'autenticazione |
|---|---|
| **SMTP integrato** (il server email di Spwig) | Spwig genera automaticamente una coppia di chiavi DKIM per il tuo dominio. Aggiungi un account email e il **Passaggio 4** della procedura guidata di configurazione mostra lo stato di SPF, DKIM e DMARC oltre al record esatto da aggiungere, con copia negli appunti e istruzioni specifiche per provider per Cloudflare, GoDaddy, Namecheap e AWS Route 53. Lo stesso record DNS DKIM viene mostrato anche nella pagina di amministrazione dell'account, sotto **Chiavi DKIM configurate**, se hai bisogno di ritrovarlo. |
| **SMTP generico** (un provider portato dall'utente come SendGrid, Mailgun, Amazon SES o Google Workspace, connesso tramite credenziali SMTP) | L'autenticazione avviene in parte nel dashboard di quel provider. Il passaggio DNS della procedura guidata di configurazione include istruzioni a schede specifiche per Gmail, Outlook, SendGrid, Mailgun e Amazon SES — ciascuna spiega cosa configurare nella console del provider (ad esempio, verificare un dominio di invio in SendGrid) e quali record DNS risultanti aggiungere presso il tuo host DNS. |
| **Gateway di posta ospitato da Spwig** | Disponibile nei piani ospitati da Spwig come opzione di invio gestita. Firma le email in uscita con DKIM automaticamente e predefinisce l'invio da un indirizzo sul dominio verificato di Spwig, quindi funziona senza alcuna configurazione. Se vuoi inviare dal tuo dominio tramite il gateway, parla con il tuo provider di hosting per verificarlo — si tratta di un servizio gestito, non di un flusso DNS self-service. |

![Passaggio 4 della procedura guidata di configurazione dell'account email, che mostra la convalida SPF/DKIM/DMARC, le schede dei provider DNS e un record DKIM espanso pronto per la copia](/static/core/admin/img/help/deliverability/wizard-dns-step.webp)

![Pannello delle chiavi DKIM configurate di un account email SMTP integrato esistente, con il record TXT DNS e un pulsante Copia record DNS](/static/core/admin/img/help/deliverability/dkim-dns-record.webp)

Indipendentemente dalla modalità utilizzata, **l'aggiunta del record DNS stesso è sempre un passaggio esterno** — lo esegui presso il tuo registrar di dominio o host DNS (Cloudflare, GoDaddy, Namecheap, Route 53, o ovunque puntino i nameserver del tuo dominio), non all'interno di Spwig.

Spwig può dirti esattamente cosa aggiungere e verificare che sia attivo, ma non può accedere al tuo registrar per aggiungerlo al posto tuo.

Alcune cose da sapere prima di iniziare:

- **Le modifiche DNS non sono immediate.** La propagazione può richiedere da pochi minuti a 48 ore. Il passaggio di validazione della procedura guidata mostrerà un record come non riuscito o mancante finché non sarà effettivamente propagato — questo è previsto, non è un segno che qualcosa non va.
- **È consentito un solo record SPF per dominio.** Se ne hai già uno (da Google Workspace, un altro provider di posta, ecc.), aggiungi il tuo nuovo mittente al record esistente con `include:` anziché creare un secondo record TXT SPF — due record SPF romperanno l'autenticazione per tutti.
- **DMARC richiede che SPF o DKIM siano già superati.** Configuralo per ultimo, una volta verificati sia SPF che DKIM.

## Passaggio 2: Utilizzare un'identità di invio reale

Una volta autenticato il tuo dominio, assicurati che ciò che i destinatari vedono effettivamente lo supporti:

- **Indirizzo mittente** — usa un indirizzo sul tuo dominio autenticato (`orders@yourstore.com`), mai un indirizzo di un provider gratuito (`yourstore@gmail.com`). Un indirizzo mittente di un provider gratuito non può essere autenticato dai tuoi record SPF/DKIM/DMARC in alcun modo, e i provider di posta in arrivo lo trattano come un forte segnale di spam da parte di un negozio.
- **Nome mittente** — usa il nome riconoscibile del tuo negozio, non un'etichetta generica come "Notifiche" o "Non rispondere".
- **Rispondi a** — imposta un indirizzo monitorato. Un indirizzo `noreply@` non monitorato che rimbalza o scarta silenziosamente le risposte è di per sé un lieve segnale di reputazione, e blocca l'unico canale che i clienti hanno per dirti che qualcosa è andato storto.

Imposta tutti e tre sotto **Configurazione Email > (il tuo account) > Configurazione Mittente** — consulta [Configurazione Email](email-configuration) per la descrizione completa dei campi.

## Passaggio 3: Riscaldare prima di scalare

Un dominio o un IP senza storico di invio non ha ancora reputazione — buona o cattiva — e i provider di posta in arrivo sono cauti con l'ignoto. Inviare un primo massiccio invio da un dominio completamente nuovo appare statisticamente identico a uno spammer che avvia una nuova campagna, e può finire nella cartella spam anche se ogni casella tecnica è spuntata.

- Inizia in piccolo. Invia le tue prime campagne al tuo pubblico più coinvolto e più propenso ad aprire, anziché all'intera lista in una volta — consulta [Pubblici](audiences) per creare un segmento iniziale mirato.
- Aumenta il volume gradualmente nelle prime settimane anziché passare direttamente agli invii all'intera lista.
- Se stai migrando un elenco esistente da un'altra piattaforma, trattalo come il primo giorno per quanto riguarda la reputazione — lo storico di invio della tua vecchia piattaforma non si trasferisce con il dominio.

## Passaggio 4: Mantieni la tua lista pulita

Ogni reclamo o rimbalzo ti costa reputazione, e entrambi sono in gran parte una funzione di chi è sulla tua lista e di come ci è finito:

- **Invia email solo a persone che hanno dato il consenso.** I contatti importati, le liste acquistate e gli indirizzi estratti sono il modo più rapido per far aumentare i reclami di spam e i rimbalzi hard.
- **Usa il doppio opt-in.** Il flusso di consenso marketing di Spwig verifica l'indirizzo email di un abbonato prima di inviargli email marketing — consulta [Preferenze di Comunicazione](communication-preferences) per vedere come è configurato.
- **Lascia che la soppressione automatica di Spwig faccia il suo lavoro.** Spwig monitora i rimbalzi hard, i reclami di spam e i rimbalzi soft ripetuti e smette automaticamente di inviare email a quegli indirizzi, senza necessità di configurazione — consulta [Igiene della Lista e Soppressioni](list-hygiene) per capire esattamente come funziona e quando (raramente) sovrascriverlo.
- **Potare periodicamente gli abbonati inattivi** anziché inviare email agli stessi indirizzi non coinvolti all'infinito — una lista in diminuzione che apre e clicca vale più per la tua reputazione di una grande che non lo fa.

## Passaggio 5: Monitorare


I problemi di deliverability emergono nei numeri prima ancora che un cliente ti segnali che una email non è arrivata.

Apri il [Report](campaign-reports) di una campagna dopo ogni invio e monitora:

| Metrica | Cosa monitorare |
|---|---|
| **Tasso di rimbalzo** | La prevalenza di rimbalzi soft è normale; un aumento della quota di **rimbalzi hard** indica che la tua lista sta accumulando indirizzi obsoleti o non validi. |
| **Segnalazioni di spam** | Dovrebbe restare vicino allo zero per ogni invio. Mantienilo ben al di sotto della soglia di circa lo 0,3% che attiva le misure di enforcement per i mittenti in blocco su Gmail e Yahoo — considera anche un piccolo picco come un segnale da indagare immediatamente. |
| **Tasso di apertura / tasso di clic rispetto alle aperture** | Un calo improvviso e inspiegabile tra invii alla stessa lista (non solo per una singola campagna) può essere un segnale precoce che le email stanno finendo nella cartella spam anziché nella casella di posta, anche prima che i numeri di rimbalzo o segnalazioni si muovano. |

Controlla anche periodicamente la card **Indirizzi soppressi** nella dashboard di Campaign Studio — un flusso costante è un normale decadimento della lista, ma un picco improvviso merita un'indagine prima del tuo prossimo invio (vedi [Igiene della lista](list-hygiene)).

![La card statistica degli indirizzi soppressi nella dashboard di Campaign Studio](/static/core/admin/img/help/deliverability/suppressed-addresses-card.webp)

Se qualcosa registra un picco: metti in pausa e verifica prima che i tuoi record DNS siano ancora validi (un rinnovo di dominio scaduto o una modifica accidentale ai DNS possono rompere silenziosamente SPF/DKIM), poi esamina cosa è cambiato nel contenuto o nel pubblico dell'invio che lo ha causato.

## Passo 6: Igiene del contenuto

L'autenticazione e la qualità della lista ti fanno entrare dalla porta; il contenuto continua a influenzare come vieni trattato una volta dentro.

- **Evita i pattern che attivano gli spam filter** nelle righe oggetto — TUTTI MAIUSCOLI, punteggiatura eccessiva ("!!!") e frasi come "agisci ora" o "soldi gratis" pesano ancora a tuo sfavore con gli spam filter, anche da un dominio autenticato.
- **Non inviare email solo con immagini.** Un'email che è una singola immagine senza testo reale è un classico pattern di spam; mantieni una quantità significativa di contenuto testuale reale accanto a qualsiasi immagine.
- **Anteprima prima dell'invio.** Controlla come l'email viene effettivamente renderizzata — incluso su mobile — prima che vada alla tua lista completa.
- **Il link di disiscrizione è già gestito.** Spwig aggiunge automaticamente un link di disiscrizione funzionante, senza necessità di login, nel footer di ogni email di marketing — non devi aggiungerne uno tuo (vedi [Preferenze di comunicazione](communication-preferences) per capire esattamente come funziona quel flusso). Non rimuoverlo o nasconderlo; un link di disiscrizione mancante o rotto è di per sé una violazione delle regole dei mittenti in blocco di Gmail e Yahoo, indipendentemente dai tuoi altri numeri.

## "Le mie email finiscono nello spam" — checklist di troubleshooting

Segui questi passaggi in ordine:

1. **Ricontrolla i tuoi record DNS.** Apri il passo DNS della procedura guidata di configurazione dell'account (o il pannello DKIM nella pagina di amministrazione dell'account per SMTP integrato) e conferma che SPF, DKIM e DMARC mostrino tutti ancora come superati.

Un rinnovo di dominio, una migrazione del provider DNS o una modifica non correlata al tuo file di zona possono rompere silenziosamente uno di questi.
2. **Controlla i numeri di rimbalzo e segnalazioni nel report della campagna** per gli invii interessati — vedi [Report delle campagne](campaign-reports).


Un picco in uno dei due indicatori segnala un problema di qualità della lista o dei contenuti, non di autenticazione.
3. **Controlla l'elenco delle soppressioni** ([Igiene della lista](list-hygiene)) per un aumento improvviso: se una parte significativa della tua lista ha avuto problemi per un po' di tempo, la consegnabilità al resto della lista ne risente anch'essa.
4. **Verifica che l'indirizzo mittente sia sul tuo dominio autenticato**, non su un indirizzo di un provider gratuito o su un dominio che non corrisponde a quello per cui sono stati configurati SPF/DKIM/DMARC.
5. **Invia un'email di test a un indirizzo Gmail e a un indirizzo Yahoo/Outlook che controlli tu** e verifica la cartella effettiva in cui viene recapitata, non solo se è arrivata.
6. **Se hai recentemente modificato drasticamente il volume di invio o il pubblico,** trattalo come una nuova fase di riscaldamento: riduci il volume e aumentalo in modo più graduale.
7. **Se tutto quanto sopra è corretto e il problema persiste,** potrebbe trattarsi di una limitazione specifica del provider piuttosto che di un errore nella tua configurazione: una volta risolto il problema alla base (di solito reclami o rimbalzi), potrebbe volerci un po' di tempo perché si risolva da solo.

## Suggerimenti

- Correggi l'autenticazione DNS prima di qualsiasi altra cosa: ogni altra leva per la consegnabilità (contenuti, igiene della lista, riscaldamento) conta meno se SPF/DKIM/DMARC non vengono superati.
- Considera la validazione DNS della procedura guidata di configurazione come un controllo puntuale, non come un'operazione una tantum: rieseguala ogni volta che migri i provider DNS o rinnovi un dominio tramite un diverso registrar.
- Una lista pulita che apre e clicca supererà sempre una lista più grande che non lo fa: resisti alla tentazione di importare una vecchia lista non verificata "per sicurezza".
- Osserva i tuoi numeri in relazione ai tuoi invii passati, non a un benchmark generico del settore: la tua storia è il segnale più affidabile di un problema reale.
- Se sei su un piano ospitato da Spwig, la firma DKIM e la gestione della reputazione del gateway di posta ospitato sono gestite per te: la tua responsabilità rimanente riguarda la qualità della lista e i contenuti, non i DNS.