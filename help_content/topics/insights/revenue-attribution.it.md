---
title: Assegnazione del ricavo
---

L'assegnazione del ricavo ti mostra da dove provengono veramente le tue vendite - non solo l'ultimo collegamento che un cliente ha cliccato prima di acquistare, ma ogni canale che ha avuto un ruolo nel portarlo qui. Se un cliente legge un articolo del blog che hai condiviso sui social, quindi torna una settimana più tardi tramite una ricerca su Google, e infine acquista dopo aver cliccato un collegamento in una newsletter, tutti e tre i contatti hanno contribuito a quella vendita. Questo pannello attribuisce loro tutti, utilizzando un modello che scegli, in modo da poter vedere il tuo marketing come funziona realmente, invece di come pretende che funzioni "l'ultimo clic vince".

![Il pannello di assegnazione del ricavo: il selettore del modello di assegnazione, la striscia KPI con il badge "Confronta con il ricavo netto", il ricavo per canale, il ricavo nel tempo, il flusso del percorso del cliente e la tabella delle campagne](/static/core/admin/img/help/revenue-attribution/dashboard-overview.webp)

## Dove trovarlo

Vai a **Intuizioni > Assegnazione del ricavo** nel menu laterale. Intuizioni è un gruppo di menu dedicato sopra Prodotti, quindi Assegnazione del ricavo ha la sua casa separata rispetto ai tuoi report sugli ordini e sui clienti.

Intuizioni è accessibile solo con la categoria di autorizzazione **Intuizioni e Analisi**. Se non la vedi nel menu laterale, chiedi a un amministratore del negozio di concederti questa autorizzazione - consulta [Ruoli e autorizzazioni del personale](/help/staff-roles) per come gestire l'accesso del personale.

## Comprensione dell'assegnazione multi-tocco

La maggior parte dei negozi è abituata a pensare in termini di "da dove proviene questo ordine?" come se ci fosse una sola risposta. In realtà, i clienti raramente acquistano al loro primo accesso. Scoprono il tuo marchio in un modo, tornano in un altro modo e convertono in un terzo modo - a volte in diversi accessi distribuiti su giorni o settimane. Ogni accesso è un **tocco**: un arrivo registrato nel tuo negozio che porta un segnale su dove proviene (un collegamento email, un risultato di ricerca, un post sui social, un collegamento affiliato e così via).

**L'assegnazione multi-tocco** significa riconoscere ogni tocco in quel percorso e decidere quanto merito ciascuno di essi per la vendita finale, invece di assegnare l'intera quota di credito al canale che ha avuto l'ultimo clic. Questo è importante perché la segnalazione dell'ultimo clic sottostima sistematicamente i canali che svolgono il lavoro di scoperta iniziale - il tuo blog, la tua presenza nei risultati di ricerca organica, i tuoi post sui social - perché raramente diventano l'ultimo clic prima del checkout.

## Scegliere un modello di assegnazione

Il selettore del modello in cima al pannello è il controllo più importante della pagina. Clicca su qualsiasi modello e tutti i numeri sul pannello - la striscia KPI, le barre per canale, il grafico, la tabella delle campagne - si riassegnano istantaneamente per adattarsi. Questo è un'anteprima in tempo reale: cambiare i modelli qui cambia il modo in cui guardi i tuoi ricavi esistenti, non riscrive registri o modifica il modello predefinito salvato del tuo negozio.

![Il selettore del modello di assegnazione - Ultimo tocco, Primo tocco, Lineare, Decadimento nel tempo e Posizione 40/20/40 - con l'indicatore "Riassegna in tempo reale · nessun rielaborazione"](/static/core/admin/img/help/revenue-attribution/model-switcher.webp)

| Model | Cosa fa | Ideale per |
|-------|---------------|----------|
| **Ultimo tocco** | Assegna completamente il merito all'ultimo canale prima dell'ordine, ignorando i contatti precedenti (tranne le visite 'dirette' pure, che vengono saltate a favore dell'ultimo vero canale) | Una visione rapida e familiare - come la maggior parte degli strumenti di analisi base segnala il fatturato |
| **Primo tocco** | Assegna completamente il merito al canale che per primo ha portato il cliente nel tuo negozio | Capire cosa sta guidando la scoperta dei nuovi clienti e la crescita in cima al ciclo di acquisto |
| **Lineare** | Suddivide il merito in modo equo in ogni tocco del percorso | Una visione equilibrata, senza opinioni, quando non si vuole favorire alcun canale specifico |
| **Decadimento nel tempo** | Assegna più merito ai contatti più vicini all'ordine, meno a quelli più indietro | Campagne con un lasso di considerazione breve, dove i richiami recenti contano di più |
| **Posizione 40/20/40** | Assegna il 40% di merito al primo tocco, il 40% all'ultimo tocco e suddivide i restanti 20% tra tutto il resto | Riconoscere sia "chi ci ha trovati" che "chi ha chiuso la vendita", mantenendo comunque il merito del percorso centrale |

Non esiste un unico modello "corretto" - ognuno risponde a una domanda diversa. Un approccio comune è verificare **Primo tocco** per capire cosa sta guidando la scoperta, quindi **Ultimo tocco** o **Posizione 40/20/40** per capire cosa sta guidando le conversioni, e utilizzare entrambe le visualizzazioni insieme invece di scegliere una e ignorare le altre.

## Lettura della striscia KPI

Sotto il selettore del modello, quattro numeri riassumono il periodo selezionato e il modello:

- **Fatturato attribuito** - il fatturato totale attribuito a tutti i canali per il modello corrente. Ha un badge di **Confronto con il fatturato netto** quando i dati si allineano correttamente con il fatturato netto reale del negozio per il periodo - in altre parole, il modello sta suddividendo il fatturato reale tra i canali, non inventandone o perdendone alcuno.
- **Ordini** - quanti ordini rientrano nell'intervallo di date selezionato.
- **Media dei contatti per ordine** - il numero medio di contatti registrati per ordine. Un numero superiore a 1 conferma che la maggior parte dei percorsi dei tuoi clienti coinvolge più di una visita, esattamente per questo motivo l'attribuzione multi-tocco è importante per il tuo negozio.
- **Canale principale** - qualsiasi canale attualmente abbia la maggiore fetta di fatturato attribuito sotto il modello selezionato, con la sua percentuale di quota e il fatturato.

## Fatturato per canale

La scheda **Fatturato per canale** mostra un'asta orizzontale per ogni canale, dimensionata in base al fatturato attribuito. Passa il modello di attribuzione e osserva che le barre si riassestino in modo fluido in base al punteggio - questo è lo stesso fatturato sottostante, ma suddiviso in base a un insieme diverso di regole, quindi un canale che sembra forte sotto **Ultimo tocco** potrebbe scivolare diverse posizioni sotto **Primo tocco** se principalmente svolge un ruolo di supporto.

## Fatturato nel tempo

Il grafico **Fatturato nel tempo** suddivide il fatturato attribuito per canale in ciascun giorno dell'intervallo selezionato, in modo da poter vedere non solo quanto vale ogni canale, ma anche quando contribuisce. Utilizzalo per individuare modelli stagionali, confermare l'impatto di una campagna è caduto nei giorni che ti aspettavi, o verificare se il contributo di un canale sta crescendo o riducendosi nel periodo.

## Come effettivamente i clienti arrivano

Il pannello **Come effettivamente i clienti arrivano** è un diagramma del flusso del percorso che collega il canale che per primo ha portato un cliente (a sinistra) al canale presente quando ha effettuato l'acquisto (a destra). Nastri più spessi significano che più reddito è passato attraverso quel percorso. Questo è il modo più chiaro per vedere percorsi a più passaggi in un colpo d'occhio - ad esempio, un nastro spesso da Ricerca organica a Email ti dice che la ricerca sta portando le persone dentro, ma la tua email marketing è quella che le sta facendo tornare per acquistare.

![Il diagramma del flusso del percorso del cliente, con la lente "Influenzato" selezionata, che mostra i canali del primo tocco a sinistra che scorrono al canale in cui ogni ordine si è convertito](/static/core/admin/img/help/revenue-attribution/journey-flow-sankey.webp)

Usa l'interruttore **Attribuito** / **Influenzato** sopra il grafico per passare alle lenti:

- **Attribuito** suddivide il ricavo di ogni ordine in base al modello selezionato, in modo che i totali siano pari al 100% del ricavo attribuito — gli stessi valori visualizzati altrove nel pannello di controllo.
- **Influenzato** attribuisce *ogni* canale che ha interagito con un ordine con il *valore completo* di quell'ordine, contato una volta per ordine.

Questo non somma mai al 100% — un canale può essere "influenzato" da un ricavo che viene conteggiato completamente anche per un altro canale.

Viene utilizzato per evidenziare la portata di un canale che la segnalazione dell'ultimo clic nasconde del tutto, ad esempio un articolo di blog o un condivisione su social che ha reso qualcuno interessato anche se non ha cliccato durante l'ultima visita.

## Campagne

La tabella **Campagne** suddivide il ricavo, gli ordini e il valore medio degli ordini (AOV) per ciascuna delle tue campagne contrassegnate — collegamenti o codici che hai contrassegnato con un nome di campagna, compresi i codici per sconti contrassegnati da campagna (vedi [Idee per campagne con sconti](/help/voucher-campaign-ideas)). Utilizzala per paragonare il funzionamento di promozioni individuali, codici di influencer o azioni di marketing tra loro, indipendentemente dal canale che le ha trasmesse.

## Intervallo di date e esportazione dei tuoi dati

Utilizza il selettore dell'intervallo di date nell'angolo in alto a destra per passare da **Ultimi 7 giorni**, **Ultimi 14 giorni**, **Ultimi 30 giorni**, **Ultimi 90 giorni** e **Mese fino ad oggi**. L'intero pannello di controllo si aggiorna per il nuovo periodo.

Clicca su **Esporta CSV** per scaricare la suddivisione per canale per il modello e l'intervallo di date attualmente selezionati — utile per prendere i numeri in un foglio di calcolo o condividerli con un'agenzia partner.

## Come vengono registrati i contatti

Spwig cattura automaticamente un contatto ogni volta che un visitatore arriva nel tuo negozio con un segnale di origine riconoscibile, e solo quando il visitatore ha dato il **consenso all'analisi** nel banner dei cookie del tuo negozio (se non gestisci un banner di consenso, il tracciamento è attivo per default, come previsto dalla tua politica del negozio). Questo mantiene l'attribuzione del ricavo sullo stesso piano di privacy rispetto al resto delle analisi del tuo negozio.

Molti canali vengono contrassegnati automaticamente, senza bisogno di configurazione:

| Canale | Come viene identificato |
|---------|----------------------|
| **Email** | Collegamenti nei tuoi email di marketing (non email di ordine o spedizione) |
| **Ricerca organica / a pagamento** | Referrer dei motori di ricerca, o valori `utm_medium` che segnalano una campagna di ricerca a pagamento |
| **Social organico / a pagamento** | Referrer dei network social, o valori `utm_medium` sociali |
| **Affiliazione** | Collegamenti generati attraverso il tuo programma di affiliazione |
| **Segnala un amico** | Collegamenti generati attraverso il tuo programma di referral dei clienti |
| **Campagna** | Ogni collegamento o codice che porta un tag di campagna, compresi i codici per sconti contrassegnati da campagna |
| **Collegamento esterno** | Un collegamento in entrata da un altro sito web che non è altrimenti categorizzato |
| **Diretto** | Nessun segnale di origine presente — il visitatore ha digitato l'indirizzo, ha usato un segnalibro o è arrivato da un'app senza referrer |

Gli articoli di blog che vengono condivisi automaticamente sui tuoi account social connessi vengono automaticamente contrassegnati, in modo che il traffico che generano venga visualizzato nel giusto canale sociale invece di andare perso come Diretto o Collegamento esterno.

Puoi inoltre contrassegnare i tuoi collegamenti manualmente utilizzando parametri standard `utm_source`, `utm_medium` e `utm_campaign` su qualsiasi URL che punta al tuo negozio — utile per materiali stampati, newsletter di partner o qualsiasi canale non contrassegnato automaticamente da Spwig.

## Limitazioni da tenere a mente

- **L'attribuzione segue un browser, non una persona.** Se un cliente effettua ricerche sul telefono e acquista sul laptop, si tratta di due percorsi diversi rispetto al tracciamento — non esiste alcun modo per collegare l'attività su dispositivi diversi.

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

Ciò significa che alcune credenziali che "dovrebbero" andare a un tocco precedente su un altro dispositivo finiranno su Direct.
- **Direct è dove arriva il ricavo non registrato.** Una percentuale elevata di Direct non significa necessariamente che le persone digitino l'URL del vostro sito a memoria - può anche significare che i precedenti contatti di un cliente siano avvenuti su un altro dispositivo, oppure che il collegamento utilizzato non abbia etichette.
- **Il rifiuto del consenso significa che nessun tocco viene registrato.** Gli utenti che rifiutano il consenso all'analisi nella vostra finestra dei cookie non vengono tracciati, quindi i loro ordini appariranno come Direct anche se sono arrivati tramite un canale che di solito riconoscerebbe.

## Suggerimenti

- Controlla più modelli prima di trarre conclusioni - un canale che sembra debole sotto **Ultimo tocco** può essere il vostro canale di scoperta più forte sotto **Primo tocco**.
- Se **Direct** rappresenta una percentuale elevata del vostro fatturato, controllate se potreste etichettare con `utm_source`/`utm_medium`/`utm_campaign` di più collegamenti del vostro marketing - il traffico non etichettato non ha altra scelta.
- Utilizzate la lente **Influenced** sul grafico del percorso quando decidete se continuare a investire in un canale come la ricerca organica o i contenuti del blog che raramente riceve il clic finale ma che inizia costantemente i percorsi.
- Confrontate l'**Avg. tocchi / ordine** nel tempo - un numero in crescita di solito significa che i clienti impiegano più tempo per decidere, un segnale utile quando si pianificano la posta elettronica di follow-up o il timing del ritargeting.
- Esportate il file CSV per il modello e il periodo di cui state facendo rapporto prima di passare nuovamente a un altro modello, poiché l'esportazione riflette esattamente il modello selezionato nel momento in cui cliccate su **Esporta CSV**.