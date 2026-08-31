---
title: Test A/B
---

Il **test A/B** di Campaign Studio ti consente di provare da due a quattro **varianti** — diverse versioni della stessa campagna — su una porzione del tuo pubblico prima di procedere con l'invio completo. Modifica solo l'oggetto o progetta contenuti completamente diversi per ogni variante. Spwig divide un campione della tua lista in modo uniforme tra le varianti, monitora le prestazioni di ciascuna e invia automaticamente la variante con le migliori prestazioni a tutti coloro che non hanno visto il test.

## Configurazione di un test

Innanzitutto, crea la tua campagna come al solito nel builder visuale di Campaign Studio: scrivi un oggetto, progetta i tuoi contenuti e scegli il **Segmento** a cui vuoi raggiungere. Questa campagna diventa il **contenitore** del test. Una volta associato un test A/B, il contenitore stesso non viene mai inviato direttamente: il suo ruolo è quello di contenere le impostazioni e il pubblico a cui è destinato è esattamente il pool su cui viene eseguito il test.

Due posizioni aprono la procedura guidata del test A/B:

- Il pulsante **Test A/B** nella barra degli strumenti del builder visuale.
- L'icona **Test A/B** sulla scheda della campagna in **Campaign Studio > Campagne**.

Una volta che un test esiste su una campagna, lo stesso pulsante ti porta direttamente ai suoi risultati invece che alla procedura guidata, e la scheda della campagna acquisisce un piccolo badge **A/B** in modo da poterlo individuare a colpo d'occhio nell'elenco.

## Cosa testare

Il primo passo della procedura guidata chiede cosa dovrebbe differire tra le varianti:

| Opzione | Cosa cambia | Misurato da |
|--------|--------------|-------------|
| **Oggetto** | Ogni variante invia esattamente gli stessi contenuti — solo l'oggetto differisce. Il test più comune. | Tasso di apertura |
| **Contenuto** | Ogni variante è un design separato che crei tu stesso nel builder visuale. | Tasso di clic |

![Il passaggio "Cosa vuoi testare?", con Oggetto selezionato](/static/core/admin/img/help/ab-testing/ab-test-what-to-test.webp)

## Scelta delle varianti

Quello che inserisci successivamente dipende da ciò che hai scelto:

- **Oggetto** — digita un oggetto per ogni variante (2–4). Vengono mostrate due righe all'inizio; fai clic su **Aggiungi un altro oggetto** per un terzo o quarto.
- **Contenuto** — scegli semplicemente quante varianti vuoi (2–4). Ogni variante inizia come una copia esatta del design attuale del tuo contenitore, quindi devi modificare solo ciò che stai testando.

In entrambi i casi, Spwig etichetta le varianti **A**, **B**, **C** e **D** nell'ordine in cui le inserisci — le vedrai come "Variante A", "Variante B" e così via da qui in poi.

![Il passaggio Varianti con tre oggetti inseriti per le varianti A, B e C](/static/core/admin/img/help/ab-testing/ab-test-variants.webp)

Per un test di contenuto, non progetti le varianti nella procedura guidata stessa — dopo aver creato il test, la scheda di ogni variante nell'hub dei risultati ha una piccola icona a matita che la apre nello stesso builder visuale utilizzato per il contenitore. Questo è disponibile solo mentre il test è ancora in **Bozza**; una volta avviato il test, i design vengono bloccati in modo che ciò che stai misurando non cambi durante il test.

## Impostazioni del test

L'ultimo passo della procedura guidata copre come viene eseguito e deciso il test:

| Impostazione | Cosa fa |
|---------|--------------|
| **Campione di test** | La quota del tuo pubblico utilizzata per il test, divisa uniformemente tra le varianti: 20%, 30%, 50% o 100%. Il resto — il **holdout** — riceve il vincitore successivamente. Scegliendo il 100% si testa l'intera lista in una volta sola, quindi non c'è più holdout a cui inviare un vincitore. |
| **Vincitore deciso da** | **Tasso di apertura** o **Tasso di clic**. Predefinito su tasso di apertura per un test di oggetto e tasso di clic per un test di contenuto, poiché è ciò che ciascuno misura realmente — ma puoi cambiarlo in entrambi i casi. |
| **Finestra di test (ore)** | Quanto tempo raccogliere aperture e clic prima di scegliere un vincitore, da 1 a 168 ore (una settimana completa). |
| **Invia automaticamente il vincitore al resto del pubblico** | Attivato per impostazione predefinita. Quando selezionato, Spwig invia la variante vincente all'holdout non appena la finestra termina, senza ulteriori azioni da parte tua. |

Una breve scheda di riepilogo in fondo riassume le tue scelte prima di confermare.

![La fase Impostazioni con le opzioni di campione, metrica, finestra e invio automatico configurate, oltre a una scheda di riepilogo](/static/core/admin/img/help/ab-testing/ab-test-settings.webp)

## Avvio del test

Fai clic su **Crea test** per salvare la configurazione: in questo momento non viene inviato nulla. Verrai reindirizzato al centro risultati del test con lo stato **Bozza**, dove ogni variante mostra zero destinatari finora e due pulsanti: **Avvia test** e **Annulla test**.

![Un test appena creato in stato Bozza, con tre varianti pronte per l'avvio](/static/core/admin/img/help/ab-testing/ab-test-draft.webp)

Fai clic su **Avvia test** quando sei pronto. Spwig divide il campione di test equamente tra le varianti e invia un'email a ciascuna immediatamente: non devi fare altro; un processo in background verifica lo stato una volta trascorsa la finestra di test e decide il vincitore in autonomia. Lo stato della campagna contenitore rimane **Bozza** durante tutto questo processo: è un comportamento atteso, poiché sono le varianti (e in seguito il vincitore) a essere effettivamente inviate, mai la campagna contenitore.

Il tuo pubblico deve essere sufficientemente ampio da garantire a ogni variante un numero significativo di destinatari. Spwig impedisce l'avvio di un test se una qualsiasi variante avrebbe zero persone, ma un test davvero utile richiede più del minimo indispensabile: punta a diverse centinaia di destinatari o più prima di affidarti al risultato.

## Durante l'esecuzione del test

Una volta avviato, il centro passa allo stato **In test** e mostra "Test in esecuzione — il vincitore viene deciso automaticamente intorno a" la data e l'ora in cui termina la finestra. I conteggi dei destinatari e le percentuali di apertura/click in tempo reale si aggiornano a ogni visita, insieme a un grafico a barre che confronta la percentuale di apertura e di click di ogni variante affiancate — non solo la metrica scelta per decidere il vincitore.

![Un test in esecuzione che mostra i conteggi dei destinatari in tempo reale, le percentuali di apertura/click e un grafico di confronto](/static/core/admin/img/help/ab-testing/ab-test-running.webp)

Puoi anche monitorare ogni test dalla **Dashboard di Campaign Studio**: il suo pannello *Test A/B recenti* elenca i tuoi test in esecuzione e quelli decisi di recente — ciascuno con il livello di confidenza a colpo d'occhio — e collega direttamente ai risultati, accanto a schede che contano quanti test sono in esecuzione e quanti sono stati decisi negli ultimi 30 giorni.

## Lettura dei risultati

Quando la finestra di test termina, Spwig seleziona la variante con la percentuale più alta sulla metrica scelta, segna il test come **Completato** e — se **Invia automaticamente il vincitore** era selezionato e c'è un gruppo di controllo a cui inviare — invia quella variante a tutti coloro che non hanno fatto parte del test. La scheda della variante vincente è evidenziata e reca un badge **Vincitore**; il grafico di confronto rimane in posizione così da poter vedere come si sono confrontate le varianti.

![Un test completato con la variante vincente evidenziata e un badge Vincitore](/static/core/admin/img/help/ab-testing/ab-test-complete.webp)

Tieni presente che i numeri in questa pagina si riferiscono sempre al campione di test, non all'intera lista: con un campione del 20%, stai leggendo come ha risposto un quinto del tuo pubblico, non tutti.

## Quanto è affidabile il risultato?

Una percentuale di apertura o click più alta non significa sempre che una variante sia genuinamente migliore: con un pubblico piccolo, una variante può emergere per puro caso. Pertanto, accanto al vincitore, Spwig mostra **quanto è sicuro che il risultato sia reale**, in base alla dimensione del divario e al numero di destinatari. Vedrai una di queste tre valutazioni:

- **Risultato chiaro** — Spwig è sicuro al 95% o più che la variante in testa superi genuinamente le altre. Questo è un risultato su cui puoi agire.
- **Troppo vicino per decidere** — c'è un leader, ma il divario è così piccolo da poter essere dovuto al caso. La percentuale mostrata indica il livello di sicurezza di Spwig, al di sotto della soglia del 95%. Considera la possibilità di ripetere il test con un pubblico più ampio o una finestra di test più lunga prima di trarre conclusioni.
- **Dati insufficienti** — troppi pochi destinatari (o troppe poche aperture e click) per distinguere le varianti. Questo è comune con liste piccole; amplia il pubblico o lascia che il test continui più a lungo.

![Test completato con un risultato chiaro — la variante vincente reca un badge di confidenza e il riepilogo riporta "statisticamente chiaro"](/static/core/admin/img/help/ab-testing/ab-test-confidence.webp)

La stessa lettura è visibile anche mentre un test è ancora in corso, così puoi osservare se un risultato si consolida — o meno — prima della chiusura della finestra di test. Poiché la confidenza dipende fortemente dalla dimensione del pubblico, questa è la ragione pratica per cui è consigliabile puntare a diverse centinaia o più di destinatari per test: su un elenco molto piccolo, anche una differenza apparentemente grande verrà di solito letta come "troppo ravvicinata per decidere".

Tieni presente che, quando l'invio automatico è attivo, Spwig invia comunque la variante con il tasso più alto al resto del tuo pubblico anche se il risultato non è conclusivo — la lettura della confidenza serve a indicarti quanto fidarti dell'esito, non a bloccare l'invio.

## Annullamento di un test

**Annulla test** è disponibile mentre un test è in stato **Bozza** o **In test**, e lo interrompe senza che venga mai inviato un vincitore. È previsto per i casi in cui hai cambiato idea o hai commesso un errore nella configurazione — non è qualcosa da usare con leggerezza, poiché una volta annullato un test (o completato normalmente), non è presente un pulsante per impostarne uno nuovo sulla stessa campagna. Se desideri eseguire un altro confronto in seguito, crea una nuova campagna per farlo.

## Suggerimenti

- Inizia con un test dell'**Oggetto** — è il più semplice da configurare ed è la ragione più comune per cui si esegue un test A/B.
- Usa un test del **Contenuto** quando vuoi confrontare design o offerte genuinamente diversi, non solo la formulazione dell'oggetto.
- Completa la progettazione di ogni variante di un test del contenuto — utilizzando l'icona della matita su ciascuna scheda — prima di cliccare su **Avvia test**. Non è possibile modificare il design di una variante una volta che il test è in corso.
- Lascia il **Campionamento test** al di sotto del 100% se vuoi che Spwig invii automaticamente il vincitore al resto della tua lista successivamente — al 100% non resta alcun gruppo di controllo a cui raggiungere.

- Concedi alla finestra di test tempo sufficiente per coprire le abitudini di lettura normali dei tuoi iscritti (24 ore coprono comodamente un'intera giornata di fusi orari e caselle di posta) anziché decidere un vincitore basandoti solo sulle prime uno o due ore.