---
title: Guida per la consegna via email
---

<!-- screenshots-needed:
- url: /admin/email_system/emailaccount/add/
  filename: wizard-dns-step.webp
  description: Fase 4 (Configurazione DNS) della procedura guidata per l'account email, per il provider SMTP integrato, che mostra le righe di sintesi per la convalida SPF/DKIM/DMARC e le schede per i provider DNS (Cloudflare/GoDaddy/Namecheap/Route 53/Altro) con almeno un pannello "Dettagli" espanso in modo che un record TXT copiabile sia visibile.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/email_system/emailaccount/{account_id}/change/
  filename: dkim-dns-record.webp
  description: Modulo di modifica per un account email SMTP integrato esistente, scorruto verso il pannello "Chiavi DKIM configurate", che mostra il nome e il valore del record TXT DNS e il pulsante "Copia record DNS".
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: suppressed-addresses-card.webp
  description: scheda delle indirizzi "suppressed" nel pannello di controllo di Campaign Studio, per la sezione "monitor" di questa guida.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
-->

Inviare un'email è facile. Ottenere che venga recapitata nella casella di posta in arrivo invece che nella cartella della posta indesiderata è il compito vero — e i fornitori di caselle di posta come Gmail e Yahoo ora applicano requisiti tecnici severi prima di considerarla. Questa guida illustra cosa configurare, nell'ordine giusto, in modo che le conferme d'ordine e le campagne arrivino dove i clienti possono vederle.

Nulla di questo è un compito unico. La consegna è un fattore che costruisci nel tempo e puoi perderlo velocemente — il controllo alla fine è da rivedere ogni volta che qualcosa sembra non andare a posto.

## Perché è importante

Ogni fornitore principale di caselle di posta valuta la reputazione del mittente prima di decidere se consegnare, riporre in una cartella della posta indesiderata o rifiutarla. Dal 2024, Gmail e Yahoo hanno reso espliciti i **requisiti per gli invii di massa** per chiunque invii volumi significativi:

- **Autentica il tuo dominio** — registrazioni SPF, DKIM e DMARC valide.
- **Rendi facile l'annullamento dell'iscrizione** — un'opzione di annullamento iscrizione funzionante, a basso impatto, in ogni email di marketing.
- **Mantieni basso il numero di lamenteze per posta indesiderata** — gli invii di massa che superano circa lo 0,3% di lamenteze rischiano di essere rifiutati o messi in cartella di massa; il target più sicuro è ben al di sotto dello 0,1%.

Se non riesci a soddisfarli, non sono solo le campagne di marketing a soffrirne — una reputazione danneggiata del dominio può far finire nella cartella della posta indesiderata anche la posta transazionale (conferme d'ordine, riacquisto della password), poiché Gmail e Yahoo giudicano sempre di più la reputazione a livello del dominio mittente, non solo per tipo di messaggio. I passaggi seguenti sono come si soddisfano tutti e tre.

| Modalità di invio | Come funziona l'autenticazione |
|---|---|
| **SMTP integrato** (il server email di Spwig) | Spwig genera automaticamente una coppia di chiavi DKIM per il tuo dominio. Aggiungi un account email e **Step 4** della procedura guidata mostra lo stato di SPF, DKIM e DMARC, nonché l'esatto record da aggiungere, con copia-incidente e istruzioni specifiche per il provider, per Cloudflare, GoDaddy, Namecheap e AWS Route 53. Lo stesso record DKIM DNS viene visualizzato anche nella pagina admin dell'account, in seguito, sotto **Chiavi DKIM configurate**, se hai bisogno di trovarlo nuovamente. |
| **SMTP generico** (un provider a tua scelta come SendGrid, Mailgun, Amazon SES o Google Workspace, connesso tramite le credenziali SMTP) | L'autenticazione avviene in parte nel pannello del provider. Il passo DNS della procedura guidata include istruzioni a schede per Gmail, Outlook, SendGrid, Mailgun e Amazon SES — ciascuna spiega cosa configurare nel pannello del provider (es. la verifica di un dominio di invio in SendGrid) e quali record DNS aggiungere presso il tuo host DNS. |
| **Portale email ospitato da Spwig** | Disponibile sui piani ospitati da Spwig come opzione di invio gestita. firma le email in uscita con DKIM automaticamente e predefinisce l'invio da un indirizzo sul dominio verificato di Spwig, quindi funziona con zero configurazione. Se vuoi inviare da un tuo dominio tramite il gateway, parla con il tuo provider di hosting per verificare — è un servizio gestito, non un flusso DNS self-serve. |

Qualunque sia la modalità utilizzata, **aggiungere il record DNS in sé è sempre un passo esterno** — lo fai presso il tuo registratore di dominio o host DNS (Cloudflare, GoDaddy, Namecheap, Route 53, o ovunque i nameserver del tuo dominio siano indirizzati), non all'interno di Spwig. Spwig può dirti esattamente cosa aggiungere e validare che sia attivo, ma non può raggiungere il tuo registratore e aggiungerlo per te.

Qualche cosa da sapere prima di iniziare:

- **I cambiamenti DNS non avvengono istantaneamente.** La propagazione può richiedere da pochi minuti a 48 ore. Il passo di convalida della procedura guidata mostrerà un record come non riuscito o mancante finché non si è veramente propagato — è normale, non un segno che qualcosa vada male.
- **È consentito un solo record SPF per dominio.** Se ne hai già uno (da Google Workspace, un altro mailer, ecc.), aggiungi il tuo mittente esistente al record esistente con `include:` invece di creare un secondo record TXT SPF — due record SPF romperanno l'autenticazione per tutti.
- **DMARC ha bisogno che SPF o DKIM siano già passati.** Impostalo per ultimo, una volta che SPF e DKIM siano entrambi verificati.

## Fase 2: Usa un'identità di invio reale

Una volta che il tuo dominio è autenticato, assicurati che ciò che vedono i destinatari lo supporti:

- **Indirizzo mittente** — usa un indirizzo sul tuo dominio autenticato (`orders@yourstore.com`), mai un indirizzo del provider gratuito (`yourstore@gmail.com`). Un indirizzo mittente del provider gratuito non può essere autenticato affatto dai tuoi record SPF/DKIM/DMARC, e i fornitori di inbox lo trattano come un segnale forte di spam da un negozio.
- **Nome mittente** — usa il nome riconoscibile del tuo negozio, non un'etichetta generica come "Notifiche" o "Nessuna risposta".
- **Rispondi a** — imposta un indirizzo monitorato. Un indirizzo `noreply@` non monitorato che rimbalza o cancella silenziosamente le risposte è un segnale di reputazione lieve, e blocca l'unico canale che i clienti hanno per dirti che qualcosa è andato storto.

Imposta e tutti e tre sotto **Configurazione Email > (il tuo account) > Configurazione Mittente** — vedi [Configurazione Email](email-configuration) per la panoramica completa dei campi.

## Fase 3: Riscalda prima di aumentare i volumi

Un dominio o IP senza storia di invio non ha ancora una reputazione — buona o cattiva — e i fornitori di inbox sono cauti con l'ignoto. Inviare un'enorme prima battaglia da un dominio appena creato sembra statisticamente identico a uno spammer che inizia una nuova campagna, e può finire nella cartella della posta indesiderata anche se ogni casella tecnica è verificata.

- Inizia con un numero più piccolo.

Invia le prime campagne al tuo pubblico più coinvolto e più propenso ad aprire, anziché all'intera lista in una sola volta — consulta [Audiences](audiences) per creare un segmento iniziale mirato.
- Aumenta il volume gradualmente nelle prime settimane, invece di passare direttamente a invii all'intera lista.
- Se stai migrando un elenco esistente da un'altra piattaforma, trattalo come il primo giorno anche ai fini della reputazione — la cronologia di invio della tua vecchia piattaforma non viene trasferita con il dominio.

## Fase 4: Mantieni la lista pulita

Ogni reclamo o rimbalzo costa reputazione, e entrambi dipendono in gran parte da chi è nella tua lista e da come è arrivato lì:

- **Invia solo a chi ha dato il consenso.** I contatti importati, le liste acquistate e gli indirizzi estratti sono il modo più rapido per far aumentare i reclami per spam e i rimbalzi definitivi.
- **Usa la doppia conferma (double opt-in).** Il flusso di consenso marketing di Spwig verifica l'indirizzo email di un abbonato prima di inviargli email marketing — consulta [Communication Preferences](communication-preferences) per vedere come è configurato.
- **Lascia che la soppressione automatica di Spwig faccia il suo lavoro.** Spwig monitora i rimbalzi definitivi, i reclami per spam e i rimbalzi temporanei ripetuti e smette automaticamente di inviare a quegli indirizzi, senza necessità di configurazione — consulta [List Hygiene and Suppressions](list-hygiene) per capire esattamente come funziona e quando (raramente) sovrascriverlo.
- **Riduci periodicamente gli abbonati inattivi** invece di inviare a indirizzi non coinvolti all'infinito — una lista in diminuzione che apre e clicca vale più per la tua reputazione di una grande che non lo fa.

## Fase 5: Monitoraggio

I problemi di consegnabilità emergono nei numeri prima che un cliente ti dica che un'email non è arrivata.

Apri il [Report](campaign-reports) di una campagna dopo ogni invio e osserva:

| Metrica | Cosa monitorare |
|---|---|
| **Tasso di rimbalzo** | La presenza di rimbalzi temporanei è normale; un aumento della quota di **rimbalzi definitivi** significa che nella tua lista si stanno accumulando indirizzi obsoleti o non validi. |
| **Reclami per spam** | Dovrebbe restare vicino a zero per ogni invio. Mantienolo ben al di sotto della soglia di circa 0,3% che attiva l'applicazione delle regole per i mittenti in massa su Gmail e Yahoo — considera anche un piccolo picco come qualcosa da indagare immediatamente. |
| **Tasso di apertura / tasso di clic su apertura** | Un calo improvviso e inspiegabile tra invii alla stessa lista (non solo una campagna) può essere un segnale precoce che le email stanno finendo nella cartella spam invece che nella casella di posta, anche prima che i numeri di rimbalzo o reclami si muovano. |

Controlla anche periodicamente la scheda **Indirizzi soppressi** nella dashboard di Campaign Studio — un flusso costante è un normale decadimento della lista, ma un picco improvviso vale la pena di essere indagato prima del tuo prossimo invio (vedi [List Hygiene](list-hygiene)).

Se qualcosa aumenta: metti in pausa e verifica prima che i tuoi record DNS siano ancora validi (un rinnovo di dominio scaduto o una modifica DNS accidentale possono rompere silenziosamente SPF/DKIM), poi guarda cosa è cambiato nel contenuto o nel pubblico dell'invio che l'ha causato.

## Fase 6: Igiene del contenuto

L'autenticazione e la qualità della lista ti fanno entrare; il contenuto influisce ancora su come vieni trattato una volta dentro.

- **Evita i pattern che attivano lo spam** nelle righe oggetto — TUTTI MAIUSCOLI, punteggiatura eccessiva ("!!!") e frasi come "agisci ora" o "soldi gratis" pesano ancora contro di te con i filtri spam, anche da un dominio autenticato.
- **Non inviare email solo con immagini.** Un'email che è una singola immagine senza testo reale è un classico pattern spam; mantieni una quantità significativa di contenuto testuale reale accanto a qualsiasi immagine.
- **Anteprima prima di inviare.** Controlla come l'email viene effettivamente renderizzata — incluso su mobile — prima che vada alla tua lista completa.
- **Il link per l'annullamento dell'iscrizione è già gestito.** Spwig aggiunge automaticamente un link funzionante per l'annullamento dell'iscrizione, senza necessità di login, nel piè di pagina di ogni email marketing — non devi aggiungerne uno tuo (vedi [Communication Preferences](communication-preferences) per capire esattamente come funziona quel flusso). Non rimuoverlo o nasconderlo; un link per l'annullamento dell'iscrizione mancante o rotto è di per sé una violazione delle regole per i mittenti in massa di Gmail e Yahoo, indipendentemente dai tuoi altri numeri.

## "Le mie email finiscono nello spam" — checklist di risoluzione

Segui questi passaggi in ordine:

1. **Ricontrolla i record DNS.** Apri il passaggio DNS della procedura di configurazione dell'account (o il pannello DKIM nella pagina di amministrazione dell'account per SMTP integrato) e conferma che SPF, DKIM e DMARC mostrino tutti lo stato "passato". Il rinnovo di un dominio, la migrazione a un provider DNS o una modifica non correlata al file di zona possono interrompere silenziosamente uno di questi.
2. **Controlla i numeri di rimbalzo e reclami nel report della campagna** per le invii interessati — vedi [Report delle campagne](campaign-reports). Un aumento di uno dei due indica un problema di qualità dell'elenco o di contenuto, anziché di autenticazione.
3. **Controlla l'elenco delle soppressioni** ([Igiene dell'elenco](list-hygiene)) per un aumento improvviso — se una parte significativa del tuo elenco ha avuto problemi per un po' di tempo, la consegnabilità al resto dell'elenco ne risente.
4. **Conferma che l'indirizzo mittente sia sul tuo dominio autenticato**, non su un indirizzo di un provider gratuito o su un dominio che non corrisponde a quello per cui sono stati configurati SPF/DKIM/DMARC.
5. **Invia un'email di test a un indirizzo Gmail e a un indirizzo Yahoo/Outlook che controlli** e verifica la cartella effettiva in cui viene archiviata, non solo se è arrivata.
6. **Se hai recentemente modificato drasticamente il volume di invio o il pubblico,** trattalo come un nuovo warm-up — riduci il volume e aumenta gradualmente.
7. **Se tutto quanto sopra è corretto e il problema persiste,** potrebbe trattarsi di una limitazione specifica del provider anziché di un errore nella tua configurazione — questo può richiedere del tempo per risolversi da solo una volta risolto il problema sottostante (di solito reclami o rimbalzi).

## Suggerimenti

- Correggi l'autenticazione DNS prima di qualsiasi altra cosa — ogni altra leva per la consegnabilità (contenuto, igiene dell'elenco, warm-up) conta meno se SPF/DKIM/DMARC non passano.
- Considera la validazione DNS della procedura di configurazione come un controllo puntuale, non un'operazione una tantum — rieseguala ogni volta che migri i provider DNS o rinnovi un dominio tramite un registratore diverso.
- Un elenco pulito che apre e clicca supererà sempre un elenco più grande che non lo fa — resisti alla tentazione di importare un vecchio elenco non verificato "per sicurezza".
- Osserva i tuoi numeri in relazione ai tuoi invii passati, non a un benchmark generico del settore — la tua storia personale è il segnale più affidabile di un problema reale.
- Se sei su un piano ospitato da Spwig, la firma DKIM e la gestione della reputazione del gateway email ospitato sono gestite per te — la tua responsabilità rimanente è la qualità dell'elenco e il contenuto, non i DNS.