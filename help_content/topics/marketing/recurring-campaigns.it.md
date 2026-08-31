---
title: Campagne ricorrenti
---

Le **Campagne ricorrenti** di Campaign Studio ti consentono di configurare una newsletter una sola volta — un riepilogo settimanale dei prodotti, un digest mensile del blog — e di farla inviare automaticamente da Spwig secondo un programma ripetuto, invece di creare e inviare manualmente una nuova campagna ogni volta.

## Broadcast vs. ricorrente

Ogni campagna in Campaign Studio ha un **Tipo di campagna**:

| Tipo | Comportamento |
|------|-----------|
| **Broadcast** | Inviata una sola volta — immediatamente o in una data e ora programmate specifiche. Utilizzala per un annuncio, una vendita o un lancio di prodotto una tantum. |
| **Ricorrente** | Funziona come un modello che viene inviato secondo un programma ripetuto. Ogni invio è una copia fresca e datata chiamata **occorrenza** — il modello stesso non viene mai inviato direttamente. |

Per trasformare una campagna in una ricorrente, aprila in **Campaign Studio > Campagne** e imposta **Tipo di campagna** su **Ricorrente**, quindi salva. Una sezione **Programma** appare sulla campagna quando la riapri — viene visualizzata solo per le campagne ricorrenti.

![Tipo di campagna impostato su Ricorrente](/static/core/admin/img/help/recurring-campaigns/campaign-type-selector.webp)

## Impostazione del programma

Una volta che una campagna è ricorrente, la sua sezione **Programma** controlla quando viene inviata:

| Campo | Descrizione |
|-------|-------------|
| **Attivo** | Attiva o disattiva la ricorrenza senza eliminare il programma. |
| **Frequenza** | **Giornaliera**, **Settimanale** o **Mensile**. |
| **Intervallo** | Invia ogni N unità di frequenza — ad esempio, intervallo `2` con frequenza **Settimanale** significa ogni 2 settimane. |
| **Giorno della settimana** | Il giorno in cui inviare per una frequenza settimanale (`0` = Lunedì … `6` = Domenica). |
| **Giorno del mese** | Il giorno in cui inviare per una frequenza mensile (`1`–`28`, in modo che ogni mese abbia quel giorno). |
| **Ora di invio** | L'ora del giorno in cui la campagna viene inviata. |
| **Fuso orario** | Un nome di fuso orario IANA, ad esempio `Europe/London` o `America/New_York` — l'ora di invio viene interpretata in questa zona, non in quella del server. |

![Sezione programma settimanale su una campagna ricorrente](/static/core/admin/img/help/recurring-campaigns/schedule-section.webp)

Non appena salvi un programma attivo, questo si **attiva** — Spwig calcola il prossimo orario di invio e lo mostra in **Prossimo esecuzione**. Non è necessario attivare nulla manualmente; un task in background controlla i programmi scaduti e invia l'occorrenza quando arriva il momento. **Ultima esecuzione** e **Occorrenze inviate** si aggiornano automaticamente dopo ogni invio, così puoi vedere che il programma è attivo.

## La politica per assenza di nuovi contenuti

Le newsletter ricorrenti spesso presentano contenuti dinamici — più comunemente un blocco **Post del blog** (o una **Griglia prodotti**) impostato su **Nuovi dall'ultimo invio** nel builder visivo, che recupera solo i post pubblicati — o i prodotti aggiunti — dall'ultimo invio della campagna. Questo solleva una domanda ovvia: cosa succede se un'esecuzione programmata arriva e non c'è nulla di nuovo da presentare?

Spwig risponde a questo con la **Politica per assenza di nuovi contenuti** del programma:

| Politica | Cosa succede | Ideale per |
|--------|---------------|----------|
| **Salta questa spedizione** *(predefinita)* | L'occorrenza viene saltata completamente — non viene inviato nulla. La pianificazione passa direttamente alla sua prossima esecuzione programmata. | Un digest di blog o prodotti, in modo che agli iscritti non venga mai inviato un'e-mail che ripete semplicemente ciò che hanno già visto. |
| **Invia comunque (ometti blocchi vuoti)** | L'e-mail viene inviata secondo la pianificazione, indipendentemente. Qualsiasi blocco che non ha nulla di nuovo — come un blocco "Nuovi post dal precedente invio" vuoto — non renderà nulla in quella posizione. | Newsletter che hanno sempre altri contenuti degni di essere inviati (un messaggio di benvenuto, sezioni evergreen o diversi blocchi dinamici) anche se un blocco risulta vuoto. |
| **Mantieni e invia in ritardo** | L'invio viene posticipato. Spwig controlla di nuovo una volta al giorno per contenuti nuovi, fino al **Finestra di attesa (giorni)**. Se nuovi contenuti appaiono entro quella finestra, l'occorrenza viene inviata in ritardo; se la finestra scade senza nulla di nuovo, quell'occorrenza viene abbandonata e la pianificazione passa al suo prossimo slot. | Una cadenza che si desidera proteggere (ad es. inviare sempre *qualcosa* alla fine) senza attivare un numero vuoto nel momento in cui non c'è stato nulla di nuovo da pubblicare quella settimana. |

Solo le campagne che utilizzano contenuti a delta — un blocco Post del blog o una Griglia di prodotti impostata su **Nuovi dal precedente invio** — attivano questo controllo. Una campagna ricorrente senza tali blocchi è sempre considerata avere contenuti nuovi e viene inviata normalmente secondo la pianificazione.

**Finestra di attesa (giorni)** si applica solo alla politica **Mantieni e invia in ritardo** — imposta quanti giorni Spwig continuerà a riprovare prima di rinunciare a quell'occorrenza.

## Test A/B di ogni occorrenza

Una newsletter ricorrente è un luogo naturale per testare A/B le tue **righe di oggetto** — invii a una cadenza regolare allo stesso pubblico, quindi puoi continuare a imparare quale formulazione ottiene più aperture. Spwig può eseguire un nuovo test A/B delle righe di oggetto su **ogni occorrenza** automaticamente.

Configuralo nella sezione **Pianificazione**:

1. In **Righe di oggetto A/B**, inserisci **due a quattro** righe di oggetto, una per riga. Lascialo vuoto per inviare le occorrenze normalmente con l'oggetto del modello.
2. Imposta il **Campione % test A/B** — la quota del pubblico di ogni occorrenza utilizzata per il test, divisa equamente tra gli oggetti. Il resto è il gruppo di controllo che riceve il vincitore.
3. Scegli il **Metrica vincitore A/B** (tasso di apertura o di clic), la **Finestra di test A/B (ore)** per raccogliere i risultati prima di decidere e se **inviare automaticamente il vincitore** al gruppo di controllo.

Da quel momento, ogni volta che la pianificazione si attiva, quell'occorrenza divide il suo pubblico, invia ogni riga di oggetto a una fetta, attende la finestra di test, quindi sceglie l'oggetto vincente e lo invia a tutti gli altri — senza ulteriori azioni da parte tua. Ogni occorrenza è un test autonomo, quindi ottieni una lettura fresca a ogni invio e puoi osservare quali oggetti vincono nel corso delle settimane. Il risultato di ogni occorrenza appare sotto **Cronologia occorrenze** di seguito, collegando direttamente alla sua pagina dei risultati con i tassi per variante, il vincitore e quanto è sicuro Spwig (vedi [Test A/B](ab-testing) per come leggere quei risultati).

Due cose da sapere:

- **Il test A/B qui è solo per le righe di oggetto.** Per confrontare design completamente diversi, usa un test A/B di trasmissione una tantum — la procedura guidata completa, che supporta varianti di contenuto, è per le campagne di trasmissione.
- Se il pubblico di un'occorrenza è **troppo piccolo per essere diviso** tra le varianti, Spwig invia silenziosamente quell'occorrenza come una normale newsletter — una settimana magra non significa mai un invio perso.

## Cronologia occorrenze

Ogni volta che una campagna ricorrente invia effettivamente, Spwig crea un'**occorrenza** con data — un record di campagna reale e indipendente con il proprio oggetto, destinatari e statistiche di invio (inviati, falliti, saltati, aperture, clic). L'occorrenza prende il nome dal modello con la data di invio aggiunta, ad es. "Weekly Blog Digest — 2026-08-19".

La pagina di modifica della campagna ricorrente elenca la sua **Storia degli eventi** — gli eventi più recenti, ciascuno con un collegamento all'account della campagna relativo, in modo da poter esaminare esattamente cosa è stato inviato e come ha ottenuto i risultati.

![Elenchi della storia degli eventi in una campagna ricorrente](/static/core/admin/img/help/recurring-campagne/occurrence-history.webp)

## Suggerimenti

- Abbinare una campagna ricorrente a un blocco **Articoli del blog** impostato su **Nuovi dall'ultima spedizione** per un digest "self-maintaining" - scritti gli articoli, Spwig si occupa dell'email.
- Iniziare con **Salta questa spedizione** per i digest dei contenuti. È il default più sicuro: i sottoscrittori non riceveranno mai un ripetizione del contenuto dell'ultima volta.
- Passare a **Invia lo stesso** solo se il tuo modello ha un altro contenuto che vale la pena inviare autonomamente, anche quando il blocco dinamico è vuoto.
- Usare **Ritieni e invia in ritardo** quando è accettabile saltare un momento della cadenza, ma non è accettabile saltare diversi momenti di seguito - imposta la finestra di attesa in base a quanto tempo sei disposto a gestire.
- Controlla **Prossima esecuzione alle** dopo aver salvato un piano per confermare che sia andato a buon fine nel giorno e orario che ti aspettavi, specialmente quando si lavora in più fusi orari.
- Esamina regolarmente la **Storia degli eventi** - un modello che continua a saltare è un segno che la fonte del tuo contenuto dinamico (ad esempio, il blog) è andata inesistente.