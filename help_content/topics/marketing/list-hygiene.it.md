---
title: Igiene della lista e soppressioni
---

Ogni indirizzo email che subisce un hard bounce, segna il tuo messaggio come spam o che non riceve i tuoi messaggi ripetutamente mette a rischio l'intera lista: i fornitori di mailbox giudicano la tua reputazione di mittente in base a quanto pulita è la tua spedizione, e una lista sporca significa che più *ogni* campagna finisce nella posta indesiderata. Campaign Studio ti protegge automaticamente da questo con l'**igiene della lista**: monitora gli indirizzi non recapitabili e quelli che segnalano problemi e smette di inviare email di marketing a loro, senza bisogno di alcuna configurazione da parte tua.

Questo è diverso dagli annullamenti. Un indirizzo annullato ha ritirato il consenso; un indirizzo **soppresso** è un indirizzo che Spwig ha appreso essere non sicuro o impossibile da inviare, indipendentemente dal consenso.

## Come gli indirizzi vengono soppressi

Spwig aggiunge un indirizzo alla **lista delle soppressioni** automaticamente quando:

| Scatenante | Cosa significa |
|---------|---------------|
| **Hard bounce** | L'indirizzo non esiste, o il dominio ha rifiutato di accettare la posta per esso - permanentemente non recapitabile. |
| **Segnalazione di spam** | Un destinatario ha contrassegnato la tua email come spam o posta indesiderata. |
| **Ripetuti soft bounce** | L'indirizzo ha subito un soft bounce (posta di posta piena, server temporaneamente non disponibile) 5 volte entro un arco di 30 giorni. Un singolo soft bounce viene considerato un problema temporaneo e ignorato - solo un modello di fallimenti ripetuti attiva la soppressione. |
| **Bloccato manualmente** | Hai aggiunto l'indirizzo personalmente. |

Una volta che un indirizzo viene soppresso, Spwig smette di inviarlo ulteriori **campagne** o **giornate** email immediatamente - non è necessaria alcuna altra azione da parte tua.

## Da dove proviene il segnale

Spwig può apprendere di un rimbalzo o di una lagnanza da diversi posti diversi, mostrati come **Fonte** su ciascun indirizzo soppresso:

- **Rifiutato al momento dell'invio** - il tuo server email ha rifiutato l'indirizzo immediatamente quando Spwig ha provato ad inviare ad esso.
- **Webhook del provider** - se hai connesso un fornitore di email (ad esempio SendGrid, Amazon SES, Mailgun o Postmark), quel fornitore segnala i rimbalzi e le lamentele a Spwig man mano che accadono.
- **Portale email** - se il tuo negozio invia attraverso il portale email ospitato da Spwig, Spwig estrae i report di rimbalzo dal portale per tuo conto.
- **Aggiunto manualmente** - hai immessoo l'indirizzo personalmente dall'amministrazione.

Non hai bisogno di configurare nulla per beneficiare di questo - in qualsiasi modo invii la posta, Spwig osserva i fallimenti e mantiene la tua lista pulita.

## Il pannello di controllo di Campaign Studio

Apri **Campaign Studio** e cerca la scheda **Indirizzi soppressi**. Mostra il numero totale di indirizzi attualmente soppressi, più quanti ne sono nuovi negli ultimi 30 giorni. Clicca sulla scheda per aprire l'elenco completo delle soppressioni.

![La scheda dello stato degli indirizzi soppressi nel pannello di controllo di Campaign Studio, che mostra un totale e un conteggio "nuovi negli ultimi 30 giorni"](/static/core/admin/img/help/list-hygiene/dashboard-suppressed-card.webp)

Un conteggio che cresce costantemente è normale - ogni lista accumula alcuni indirizzi non validi nel tempo man mano che le persone cambiano lavoro, chiudono account o abbandonano le caselle di posta. Un picco improvviso merita un'indagine; consulta [Uscita email](email-outbox) per verificare se una spedizione specifica abbia avuto un numero insolito di fallimenti.

## L'elenco delle soppressioni

Clicca su **Soppressioni** per vedere ogni indirizzo soppresso, il motivo per cui è stato soppresso e da dove proviene il segnale.

![L'elenco delle soppressioni che mostra gli indirizzi soppressi con le colonne Ragione e Fonte](/static/core/admin/img/help/list-hygiene/suppressions-list.webp)

Usa i filtri a destra per restringere l'elenco per **Ragione** o **Fonte** - ad esempio, per rivedere ogni indirizzo bloccato manualmente, o tutto ciò che è arrivato attraverso un webhook del provider.

## Aggiunta manuale di un indirizzo

Per bloccare un indirizzo personalmente - un indirizzo noto per illecito, un concorrente che sta estratto il tuo bollettino, o qualsiasi altro che vuoi tenere fuori dalla tua lista - clicca su **+ Aggiungi indirizzo soppresso** e compila:


- **Email** — l'indirizzo da bloccare
- **Reason** — scegli **Manually blocked** per un'aggiunta manuale
- **Source** — scegli **Added manually**
- **Detail** — una nota facoltativa che spiega il motivo (utile per i tuoi registri e per lo staff che esaminerà l'elenco in seguito)

Salva la voce e Spwig smetterà immediatamente di inviare a quell'indirizzo qualsiasi email di campagna o percorso.

## Quando dovrei sbloccare un indirizzo?

Lo sblocco (de-suppressione) di un indirizzo dovrebbe essere un'operazione rara e deliberata. Fallo solo quando sei sicuro che il problema sottostante sia effettivamente risolto — ad esempio:

- Un cliente ti comunica che la sua casella di posta era piena e che ora è stata svuotata.
- Un indirizzo è stato soppresso a causa di una serie di rimbalzi morbidi (soft-bounce) che sai essere stati causati da un'interruzione temporanea presso il loro provider di posta, non da una casella inesistente.
- Hai bloccato un indirizzo manualmente e in seguito decidi che il blocco era un errore.

Per sbloccare un indirizzo, aprilo nell'elenco delle Soppressioni ed elimina la voce — questo rimuove il blocco, consentendo all'indirizzo di ricevere nuovamente le email. Non sbloccare un indirizzo con rimbalzo duro (hard-bounce) solo perché è scomodo perdere un abbonato; l'indirizzo non esiste e inviarci di nuovo causerà solo un altro rimbalzo, danneggiando la tua reputazione una seconda volta. Allo stesso modo, sbloccare un indirizzo segnalato per spam raramente è utile — quel destinatario ha comunicato al suo provider di posta che non desidera ricevere le tue email, e inviarci di nuovo comporta il rischio di un'altra segnalazione.

## Cosa non è interessato

La soppressione si applica solo alle **campagne di marketing e ai percorsi** inviati tramite Campaign Studio. Non influisce sulle **email transazionali** — le conferme d'ordine, gli aggiornamenti di spedizione, il ripristino della password e altre email che il tuo negozio invia come parte di un'azione di ordine o account vengono sempre inviate, anche a un indirizzo soppresso. La soppressione esiste per proteggere la reputazione del mittente del tuo marketing; non è un elenco di blocco generale per le email del tuo negozio.

## Suggerimenti

- Non contrastare il sistema sbloccando manualmente ogni rimbalzo duro che vedi — un rimbalzo duro significa che l'indirizzo è scomparso e riaggiungerlo alle tue spedizioni causerà solo un altro rimbalzo.
- Controlla l'elenco delle Soppressioni dopo un invio massiccio se il tasso di apertura sembra insolitamente basso — un'ondata di rimbalzi morbidi su un dominio condiviso (ad esempio, un server di posta aziendale con problemi) può essere un segno di un problema temporaneo di consegna da indagare con il tuo provider.
- Se stai migrando a Spwig da un'altra piattaforma, non importare manualmente l'intero vecchio elenco di blocco come soppressioni — lascia che Spwig impari dai rimbalzi e dalle segnalazioni reali su questo elenco, in modo da non bloccare accidentalmente indirizzi che avrebbero ricevuto le email senza problemi.
- Esamina occasionalmente la colonna **Source** — un gran numero di voci **Provider webhook** conferma che la segnalazione dei rimbalzi del tuo provider di posta è connessa e funzionante.
- Mantieni il campo **Detail** significativo quando aggiungi un blocco manuale; è l'unico registro del motivo per cui quella decisione è stata presa una volta trascorso del tempo.
