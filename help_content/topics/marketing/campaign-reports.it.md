---
title: Report delle campagne
---

<!-- screenshots-needed:
- url: /admin/campaigns/{campaign_id}/report/
  filename: engagement-over-time-chart.webp
  description: The report page scrolled to the "Engagement over time" chart card, with a campaign that has several days of send history so all three lines (Sent, Opened, Clicked) show a realistic shape.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: top-links-table.webp
  description: The report page's "Top links" card, with a campaign whose email contains at least 3 distinct links and a realistic spread of Clicks/Unique/CTR values.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipients-list.webp
  description: The Recipients page with the filters panel open and a mixed list of rows (some opened, some clicked, some bounced) so the engagement states are visibly distinct.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipient-activity-modal.webp
  description: The Recipients page with the "Recipient activity" modal open for a recipient who has multiple event types (delivered, opened, at least one clicked entry naming a link).
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: attributed-revenue-card.webp
  description: A close-up of the report page's "Attributed revenue" stat card, for a campaign with a logged Spend so the orders/AOV/revenue-per-email/ROAS sub-line is fully populated.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: dashboard-attributed-revenue-kpi.webp
  description: The Campaign Studio dashboard's stat card grid, scrolled/cropped to show the "Attributed revenue (30d)" tile alongside its neighboring cards, with a non-zero revenue figure.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: report-stat-cards.webp
  description: 'RECAPTURE NEEDED: the existing report-stat-cards.webp only shows 6 cards (Recipients, Delivered, Open rate, Click rate, Bounce rate, Spam complaints). The stat grid now has a 7th "Attributed revenue" card — recapture this shot with a campaign that has both attribution data and a logged Spend so all 7 cards are visible in a realistic state.'
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
-->

Ogni campagna inviata tramite Campaign Studio ha una propria pagina **Report**: un riepilogo in un'unica pagina che mostra quante persone sono state raggiunte, quanti email sono effettivamente arrivati e come i destinatari hanno risposto. Utilizzala per verificare che un invio sia andato a buon fine, individuare tempestivamente un problema di deliverability o confrontare le prestazioni di campagne diverse nel tempo.

## Apertura di un report

Da **Campaign Studio > Campagne**, individua la campagna che desideri controllare e fai clic sull'icona del grafico (**Report**) sulla sua scheda.

![La griglia delle schede statistiche della pagina Report della campagna, che mostra destinatari, consegnati, tasso di apertura, tasso di clic, tasso di rimbalzo e reclami per spam](/static/core/admin/img/help/campaign-reports/report-stat-cards.webp)

Un report mostra dei numeri solo quando una campagna è stata effettivamente inviata: una campagna ancora in **Bozza** mostra tutte le statistiche come zero, poiché non c'è ancora nulla da misurare.

## Le schede statistiche

| Card | Cosa mostra |
|------|---------------|
| **Destinatari** | Quanti abbonati sono stati raggiunti da questa campagna, oltre a una riga secondaria che indica quanti sono stati saltati e, tra questi, quanti sono stati saltati specificamente perché l'indirizzo è presente nella tua [lista di soppressione](list-hygiene). Un salto non è sempre una soppressione — Spwig salta anche un abbonato che non ha un indirizzo email utilizzabile, ad esempio — quindi i due conteggi sono mostrati separatamente. |
| **Consegnate** | Quante email sono state effettivamente accettate dal server di posta in ricezione e non sono mai rimbalzate, oltre al **tasso di consegna** — le email consegnate come percentuale di ogni invio *tentato* da Spwig (accettato dal tuo server di posta o provider, indipendentemente dal fatto che sia poi rimbalzato). |
| **Tasso di apertura** | La percentuale di email *consegnate* che sono state aperte, oltre al conteggio grezzo delle **aperture**. |
| **Tasso di clic** | La percentuale di email *consegnate* su cui è stato fatto clic, oltre al conteggio grezzo dei **clic** e al **tasso di clic su aperture** — i clic come percentuale delle aperture, un indicatore di quanto il tuo contenuto fosse coinvolgente per chi l'ha già aperto. |
| **Tasso di rimbalzo** | La percentuale di invii *tentati* che sono rimbalzati, suddivisa in rimbalzi **hard** e **soft**. |
| **Segnalazioni di spam** | Quanti destinatari hanno segnalato l'email come spam o posta indesiderata, oltre al **tasso di segnalazioni** — le segnalazioni come percentuale della posta *consegnata*. |
| **Ricavi attribuiti** | I ricavi derivanti dagli ordini che Spwig può tracciare fino a questa campagna, oltre al numero di ordini, il valore medio dell'ordine (**AOV**), il ricavo per email consegnata e — una volta registrato il costo della campagna — il suo **ROAS**. Vedi [Ricavi attribuiti](#attributed-revenue) di seguito. |

## Perché i tassi utilizzano denominatori diversi

Il tasso di apertura, il tasso di clic e il tasso di segnalazioni sono tutti misurati rispetto alla posta **consegnata** — i destinatari che avrebbero potuto effettivamente vedere l'email — mentre il tasso di consegna e il tasso di rimbalzo sono misurati rispetto agli invii **tentati**. Questa è una pratica standard nel settore della posta elettronica ed è il motivo per cui nessuno di questi tassi può mai superare il 100%: un'email che è rimbalzata non è mai stata consegnata, quindi non può essere conteggiata nel tuo tasso di apertura o clic, e un'email che non è stata nemmeno tentata (un salto) non viene conteggiata in nessuno di essi.

## Rimbalzi hard vs. rimbalzi soft

- **Rimbalzo hard** — l'indirizzo è permanentemente non consegnabile. Non esiste, oppure il dominio rifiuta di accettare la posta per esso.
- **Rimbalzo soft** — un problema temporaneo: una casella di posta piena, un server di ricezione momentaneamente non disponibile, e simili. I rimbalzi soft si risolvono spesso da soli.

Osserva la ripartizione, non solo il totale. Un aumento del conteggio dei **rimbalzi hard** di solito significa che la tua lista contiene indirizzi obsoleti o digitati erroneamente; un aumento del conteggio dei **rimbalzi soft** è più spesso un'interruzione temporanea dal lato del destinatario. Qualsiasi rimbalzo hard, qualsiasi segnalazione di spam e un indirizzo che accumula rimbalzi soft ripetuti alimentano tutti la [lista di soppressione](list-hygiene) automatica di Spwig — non devi agire tu stesso, ma il report è il luogo in cui noterai per primo un picco che merita un'indagine.

## Ricavi attribuiti

Poiché il tuo negozio e Campaign Studio risiedono nello stesso sistema, Spwig non ha bisogno di una piattaforma di analisi esterna o di un pixel di tracciamento per dirti se una campagna ha effettivamente generato vendite. Quando un cliente fa clic su un link nell'email di questa campagna e atterra sul tuo negozio, Spwig può seguire quella visita fino al checkout e attribuire il ricavo dell'ordine risultante alla campagna — è ciò che mostra la card **Ricavi attribuiti**.

La riga secondaria della card suddivide ulteriormente il dato:

- **Ordini** — quanti ordini sono attribuiti a questa campagna.
- **AOV** — il valore medio dell'ordine tra quegli ordini.
- **Ricavo per email** — ricavi attribuiti divisi per il numero di email *consegnate*, lo stesso denominatore utilizzato dal report per il tasso di apertura e il tasso di clic.
- **ROAS** — ritorno sulla spesa pubblicitaria, mostrato solo una volta che hai inserito un importo di **Spesa** sulla campagna stessa.

Viene calcolato come ricavi attribuiti divisi per la spesa.

Se la spesa è stata registrata in una valuta diversa da quella predefinita del tuo store, Spwig nasconde il ROAS anziché mostrare un valore che non è effettivamente confrontabile in modo omogeneo: inserisci la spesa nella valuta di base del tuo store per visualizzarla.

Ecco alcune cose da sapere su come viene calcolato questo valore:

- **Si basa sui click, non sulle aperture.** Un cliente deve cliccare un link tracciato nell'email e arrivare al tuo store — una semplice apertura non attribuisce mai ricavi. Questa è una scelta deliberata: il tracciamento delle aperture è sempre meno affidabile ora che servizi come Apple Mail Privacy Protection precaricano le immagini per quasi ogni messaggio, gonfiando i conteggi delle aperture indipendentemente dal fatto che qualcuno abbia effettivamente letto l'email.
- **Segue il modello di attribuzione del tuo store.** Di default è **ultimo tocco non diretto** con una finestra di retrospettiva di 90 giorni — lo stesso click deve portare a un ordine entro quella finestra per essere conteggiato, e una visita diretta successiva non cancella il credito già guadagnato dal click di questa campagna.
- **Rispetta il consenso all'analisi.** Vengono tracciati solo i visitatori che hanno accettato il consenso all'analisi nel banner dei cookie del tuo store (se non utilizzi un banner di consenso, il tracciamento segue la politica predefinita del tuo store). Un cliente che ha rifiutato il consenso può comunque acquistare — il suo ordine semplicemente non verrà attribuito a nessun canale, incluso questo.
- **Non è retroattivo.** Il tracciamento dei ricavi copre solo le campagne inviate dopo l'attivazione del tracciamento dell'attribuzione per il tuo store. Una campagna inviata prima di allora non mostrerà ricavi attribuiti qui, anche se ha generato vendite reali, semplicemente perché Spwig non ha dati di click registrati per essa.
- **I test A/B e le campagne ricorrenti aggregano anche i loro ricavi attribuiti** — consulta [Report su un test A/B](#reports-on-an-ab-test) qui sotto.

Troverai anche una card **Ricavi attribuiti (30g)** sulla dashboard di Campaign Studio stessa, che somma i ricavi attribuiti da email di tutte le campagne negli ultimi 30 giorni — un rapido controllo dello stato senza aprire un report individuale. Per una visione a livello di store che includa tutti i canali, non solo l'email — ricerca organica, social, affiliati e altro ancora — consulta la dashboard [Revenue Attribution](/help/revenue-attribution) sotto **Insights**.

## Engagement nel tempo

Sotto le card statistiche, il grafico **Engagement nel tempo** traccia tre linee — **Inviati**, **Aperti** e **Cliccati** — un punto per giorno, coprendo i 30 giorni precedenti a oggi (o meno, se la campagna non è stata inviata per così a lungo — il grafico non inizia mai prima del giorno del primo invio della campagna).

Alcune cose da sapere su come vengono conteggiate le linee:

- **Aperti** e **Cliccati** conteggiano ogni destinatario una sola volta — il giorno della *prima* apertura o del *primo* click — non ogni volta che riaprono l'email o cliccano di nuovo un link. Questo impedisce che il grafico venga distorto da un piccolo numero di persone che aprono la stessa email ripetutamente.
- I totali dietro questo grafico sono coerenti con le card statistiche sopra: **Inviati** riflette la posta che Spwig ha tentato di consegnare, mentre **Aperti** e **Cliccati** sono entrambi misurati rispetto alla posta consegnata, allo stesso modo delle card **Tasso di apertura** e **Tasso di click**.
- Il grafico appare solo quando la campagna ha almeno un invio registrato — una campagna ancora in bozza mostra il messaggio "Nessun invio ancora" al posto del grafico, come le card statistiche.

Usa questo grafico per vedere la *forma* di un invio, non solo i suoi numeri finali — una campagna inviata a un elenco ampio spesso mostra un picco netto nelle aperture nei primi uno o due giorni, per poi diminuire. Un secondo picco giorni dopo può indicare che il server di posta del destinatario ha messo in coda il tuo messaggio, o che la tua riga di oggetto è stata notata più tardi del solito.

## Link principali

Se la tua email contiene link e almeno un destinatario ne ha cliccato uno, una tabella **Link principali** appare sotto il grafico, elencando ogni link tracciato in ordine di popolarità.

| Colonna | Cosa mostra |
|--------|---------------|
| **Link** | L'URL di destinazione così come apparso nella tua email. |
| **Clic** | Il numero totale di volte in cui quel link è stato cliccato, inclusi i clic ripetuti dallo stesso destinatario. |
| **Unici** | Quanti destinatari distinti hanno cliccato quel particolare link almeno una volta. |
| **CTR** | Il **tasso di clic** di quel link — il suo conteggio **Unici** come percentuale delle email consegnate. Questo utilizza lo stesso denominatore della card **Tasso di clic** principale del report, quindi puoi confrontare direttamente l'attrattiva di un singolo link con le prestazioni complessive di clic della campagna. |

Se la tua email fa riferimento a più prodotti o a una combinazione di pulsanti di invito all'azione, questa tabella è il modo più rapido per vedere quale ha effettivamente generato il clic — utile per decidere cosa mettere in risalto la prossima volta.

## Destinatari

Clicca su **Destinatari** in alto nel report per aprire un elenco completo e ricercabile di tutti i destinatari a cui è stata inviata questa campagna, con l'esito della consegna e l'engagement di ciascuna persona.

Due modi per restringere l'elenco:

- **Ricerca** — filtra per indirizzo email (funziona anche con una corrispondenza parziale, quindi è sufficiente digitare parte di un dominio o di un nome).
- **Engagement** — filtra per uno stato alla volta: **Aperta**, **Cliccata**, **Consegnata, non aperta** o **Rimbalzata**. Lascialo su **Tutti** per vedere l'elenco completo.

L'elenco mostra i 100 destinatari corrispondenti più recenti alla volta, dal più recente al più vecchio — il conteggio sopra l'elenco riflette sempre il totale effettivo che corrisponde ai filtri correnti, anche se è maggiore di ciò che viene mostrato. Per un invio di grandi dimensioni, restringi prima l'elenco con Ricerca o Engagement invece di scorrere tutti i destinatari.

### Visualizzazione della cronologia attività di un destinatario

Clicca sull'icona di attività nella riga di qualsiasi destinatario per aprire la sua cronologia **Attività destinatario** — ogni evento tracciato per la copia dell'email di quella persona, in ordine: consegnata, aperta, cliccata (indicando quale link), rimbalzata (con il motivo del rimbalzo), segnalata come spam o disiscritta, ciascuna con il proprio timestamp.

Questo è il modo più rapido per rispondere a una domanda specifica su un singolo cliente — ad esempio, per confermare se un determinato abbonato ha effettivamente ricevuto una campagna prima di contattarlo tramite un altro canale, o per verificare quale link un cliente ha cliccato prima di effettuare un ordine.

## Report su un test A/B

Se la campagna che stai visualizzando è il contenitore per un [test A/B](ab-testing), il suo report aggrega su **tutte le varianti** — l'intero test, combinato, incluso il **Ricavo attribuito** — invece di mostrare una singola variante da sola. Per vedere come ha performato ciascuna variante individuale, apri la pagina dei risultati del test stesso invece del report. Una [campagna ricorrente](recurring-campaigns) funziona allo stesso modo: il suo report aggrega tutte le occorrenze inviate.

## Cosa si intende per buone prestazioni

Non esiste un singolo numero sano che si adatti a ogni negozio o elenco — il pubblico, il settore e i contenuti spostano tutti la linea di base — ma ci sono alcuni schemi da tenere d'occhio su qualsiasi campagna:

- Un **tasso di rimbalzo** composto principalmente da rimbalzi soft, con rimbalzi hard rari, indica un elenco pulito e ben mantenuto. Un improvviso aumento dei rimbalzi hard vale la pena essere indagato prima del prossimo invio.
- I **segnalamenti di spam** vicini allo zero sono l'obiettivo per ogni invio. I segnalamenti danneggiano la reputazione del mittente più di quasi qualsiasi altra cosa — consulta [Igiene dell'elenco](list-hygiene) per capire perché sono importanti oltre a questa singola campagna.
- Un **tasso di clic su apertura** sano rispetto al tuo tasso di apertura ti dice che le persone che hanno aperto hanno trovato il contenuto degno di un'azione — un basso tasso di clic su apertura insieme a un forte tasso di apertura di solito indica che l'oggetto funziona meglio del contenuto all'interno.

## Suggerimenti

- Controlla il report poco dopo l'invio, non immediatamente: le aperture e i clic (e alcuni report di rimbalzo) possono richiedere tempo per essere raccolti dal tuo provider di posta.
- Se **Consegnati** appare inferiore alle aspettative, controlla prima il dettaglio dei salti nella scheda **Destinatari**: un gruppo di salti dovuti a soppressione è spesso la vera spiegazione, non un problema di consegna.
- Usa il report per confrontare una campagna con i tuoi invii passati, anziché con un numero generico del settore: la tua lista, i contenuti e il tuo pubblico sono ciò che definisce il tuo baseline realistico.
- Un picco di reclami su un invio specifico merita un'analisi più approfondita dei contenuti o del targeting di quella campagna, non solo una nota per andare avanti.
- Per una campagna testata con A/B, leggi questo report per il risultato complessivo e la pagina [Risultati test A/B](ab-testing) per sapere quale variante ha effettivamente vinto e di quanto.
- Usa la tabella **Link principali** per trovare il link più cliccato, poi verifica se corrisponde a ciò che *volevi* che i destinatari cliccassero: se un link secondario supera la tua chiamata all'azione principale, potrebbe valere la pena spostarlo più in alto nell'email la prossima volta.
- I filtri **Aperti** e **Cliccati** della pagina **Destinatari** sono un modo rapido per creare un pubblico per il follow-up: ad esempio, verificare chi ha aperto ma non ha cliccato prima di pianificare un invio di promemoria al resto della lista.
- Se hai pagato per una promozione attorno a un invio — un post social sponsorizzato, una menzione di un influencer, un affitto a pagamento di una lista — registralo come **Spesa** della campagna per sbloccare il **ROAS** nel report.

È il modo più rapido per vedere quali tipi di invii valgono davvero la pena di essere ripetuti.