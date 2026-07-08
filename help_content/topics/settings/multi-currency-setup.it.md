---
title: Configurazione multi-valuta
---

La multi-valuta consente ai tuoi clienti di navigare tra i prodotti e completare l'acquisto nella valuta di loro preferenza. I prezzi vengono automaticamente convertiti dalla tua valuta base utilizzando i tassi di cambio da un provider connesso o tassi definiti manualmente.

## Prima di iniziare

Prima di abilitare la multi-valuta, hai bisogno di:

1. **Un provider attivo per i tassi di cambio** - Vai a **Impostazioni > Tabella Valute Multiple > Dashboard Tassi di Cambio** e collega almeno un provider (ad esempio Open Exchange Rates, Fixer.io o ExchangeRate-API). Il provider deve essere attivo e sincronizzato con i tassi.
2. **Almeno due valute** - La tua valuta base più una o più valute aggiuntive che desideri supportare.

## Abilitare la multi-valuta

Vai a **Impostazioni > Valute Multiple** e attiva **Abilita Valute Multiple**. Una volta abilitata, configura le seguenti opzioni:

| Impostazione | Descrizione |
|---------|-------------|
| **Modalità di selezione della valuta** | Come i clienti scelgono la loro valuta. *Auto* rileva dalla loro posizione, *Manuale* permette loro di selezionare da un switcher, *Entrambi* combina le due approcci. |
| **Mostra switcher valuta** | Mostra un selettore di valuta sul tuo negozio online in modo che i clienti possano cambiare valuta manualmente. |
| **Posizione switcher** | Dove appare il switcher valuta (intestazione, piè di pagina o barra laterale). |
| **Mostra informazioni sui tassi di cambio** | Mostra un avviso ai clienti che i prezzi sono conversioni approssimative dalla tua valuta base. |
| **Abilita formattazione locale** | Formatta numeri e simboli di valuta in base alla località di ciascun cliente (es. 1.234,56 per i formati europei). |

## Modalità di checkout

Scegli come funziona la multi-valuta al checkout:

| Modalità | Descrizione |
|------|-------------|
| **Multi-valuta completa** | I clienti navigano, aggiungono al carrello e pagano nella valuta selezionata. Il tasso di cambio viene bloccato al checkout e registrato con l'ordine. Questo è il predefinito. |
| **Solo visualizzazione** | I prezzi vengono visualizzati nella valuta del cliente per comodità, ma il carrello e il pagamento vengono sempre elaborati nella tua valuta base. Al checkout, i clienti vedranno un avviso che mostra l'importo approssimativo convertito insieme all'importo effettivo in base alla tua valuta. |

**Solo visualizzazione** è utile quando il tuo provider di pagamento supporta solo la tua valuta base, o quando desideri evitare completamente i rischi dei tassi di cambio. I clienti vedranno comunque i prezzi localizzati durante la navigazione, dandogli un'idea dei costi nella loro valuta.

## Intervallo di sincronizzazione dei tassi di cambio

Controlla con quale frequenza il tuo negozio recupera i tassi aggiornati dal tuo provider connesso:

| Intervallo | Descrizione |
|----------|-------------|
| **In tempo reale** | Ogni 15 minuti. Ideale per negozi con vendite internazionali ad alto volume. |
| **Ogni ora** | Una volta all'ora. Buon equilibrio tra freschezza e utilizzo dell'API. |
| **Giornaliero** | Una volta al giorno. Adatto per la maggior parte dei negozi. Questo è il predefinito. |
| **Settimanale** | Una volta alla settimana. Per negozi con prezzi stabili. |
| **Mensile / Trimestrale** | Aggiornamenti meno frequenti per negozi che raramente modificano i tassi. |
| **Solo manuale** | I tassi non vengono mai recuperati automaticamente. Gestisci tutti i tassi manualmente. |

L'intervallo di sincronizzazione influisce su quanto spesso il compito in background recupera i tassi dal tuo provider. Tra le sincronizzazioni, vengono utilizzati i tassi memorizzati. Se devi forzare una sincronizzazione immediata, utilizza il pulsante **Sincronizza Ora** sulla Dashboard Tassi di Cambio o **Sincronizza dal Provider** sulla pagina Tassi di Cambio Manuali.

## Tassi di cambio manuali

I tassi di cambio manuali ti permettono di impostare tassi di conversione esatti per coppie specifiche di valute. Prendono il sopravvento sui tassi recuperati dal provider, dandoti il pieno controllo sui prezzi.

Vai a **Tassi di Cambio > Tassi di Cambio Manuali** per gestirli.

### Impostare i tassi manualmente

Clicca su **Aggiungi Tasso** per creare un tasso per una coppia di valute. Specifica la valuta base, la valuta target e il tasso. Ad esempio, impostare USD/EUR a 0,92 significa che 1 USD = 0,92 EUR.

### Sincronizzare da un provider

Clicca su **Sincronizza dal Provider** per popolare automaticamente i tassi manuali con i tassi più recenti del tuo provider connesso.

Questo crea tassi manuali per tutte le valute supportate, dandoti un punto di partenza per affinare i tassi.

I tassi bloccati vengono ignorati durante la sincronizzazione, quindi eventuali tassi che hai modificato manualmente non verranno sovrascritti.

### Blocco dei tassi

Fai clic sull'icona del lucchetto accanto a qualsiasi tasso per impedire che venga sovrascritto durante la sincronizzazione del fornitore. Questo è utile quando hai negoziato un tasso specifico o desideri mantenere un tasso fisso indipendentemente dai movimenti di mercato.

- I **tassi bloccati** mostrano un badge del lucchetto e vengono esclusi dalla sincronizzazione automatica.
- I **tassi non bloccati** possono essere aggiornati quando fai clic su **Sincronizza da Fornitore**.

### Confronto dei fornitori

Ogni tasso manuale mostra il tasso corrente del fornitore accanto a esso, con una differenza percentuale. Questo ti aiuta a vedere a colpo d'occhio come i tuoi tassi manuali si confrontano con i tassi di mercato:

- Una **percentuale verde** significa che il tuo tasso è più alto rispetto al tasso del fornitore.
- Una **percentuale rossa** significa che il tuo tasso è più basso rispetto al tasso del fornitore.

## Markup dei tassi di cambio

Puoi aggiungere un markup percentuale ai tassi di cambio per coprire le spese di conversione delle valute e proteggerti dalle fluttuazioni dei tassi tra il momento in cui un cliente effettua un ordine e quando ricevi il pagamento.

Ad esempio, un markup del 2% su un tasso USD/EUR di 1,18 lo aggiusterà a circa 1,20 USD/EUR. Questo piccolo buffer aiuta a garantire che non perda denaro nelle conversioni delle valute.

## Strategia di selezione dei tassi

Quando hai più fornitori di tassi di cambio connessi, puoi scegliere come vengono selezionati i tassi:

- **Fornitore Primario** - Utilizza sempre i tassi del tuo fornitore designato come primario. Questo garantisce prezzi coerenti in tutta la tua negozio. Se il fornitore primario non ha dati per una coppia di valute, si passa al tasso più recente disponibile da qualsiasi fornitore.
- **Più recente disponibile** - Utilizza il tasso più recentemente sincronizzato da qualsiasi fornitore attivo. Questo ti dà i dati più aggiornati, ma i tassi possono variare leggermente tra i fornitori.

Per la maggior parte dei negozi, **Fornitore Primario** è la scelta consigliata poiché fornisce il prezzo più prevedibile.

## Valute supportate

Utilizza il gestore delle valute a trascinamento per scegliere quali valute il tuo negozio supporta:

1. **Valute disponibili** (colonna di sinistra) mostra tutte le valute che puoi abilitare.
2. **Valute attive** (colonna di destra) mostra le valute attualmente abilitate nel tuo negozio.
3. Trascina le valute tra le colonne per abilitarle o disabilitarle.
4. Trascina all'interno della colonna Attive per riordinare l'aspetto in cui le valute appaiono nel commutatore.
5. Fai clic su **Salva Configurazione Valuta** per applicare le tue modifiche.

La tua valuta base è sempre attiva e non può essere rimossa.

## Come vengono risolti i tassi di cambio

Quando è necessario convertire un prezzo, il sistema controlla i tassi nell'ordine seguente:

1. **Tasso di cambio manuale** - Se esiste un tasso manuale attivo per la coppia di valute, viene sempre utilizzato per primo.
2. **Tasso del fornitore** - Se non esiste un tasso manuale, viene utilizzato il tasso più recente dal tuo fornitore connesso.

Questo significa che puoi utilizzare i fornitori per la maggior parte delle valute e sovrascrivere specifiche coppie con tassi manuali quando hai bisogno di un controllo preciso.

## Importante: Questa impostazione è permanente

Una volta abilitata la multi-valuta e i clienti hanno effettuato ordini in valute estere, questa impostazione **non può essere disattivata**. Questo è dovuto a:

- Gli ordini memorizzano permanentemente la valuta scelta dal cliente e il tasso di cambio utilizzato al momento dell'acquisto.
- I report finanziari e i calcoli dei rimborsi dipendono da questi dati storici sulle valute.
- Disattivare la multi-valuta lascerebbe gli ordini esistenti in una condizione inconsistente.

Se non sono stati effettuati ordini in valute estere, puoi comunque disattivare la multi-valuta.

## Consigli

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- **Prova con un ordine piccolo** - Piazza un ordine di prova in una valuta estera per verificare il flusso di checkout e assicurarti che siano applicate correttamente le quotazioni di cambio.
- **Monitora regolarmente le quotazioni di cambio** - Controlla periodicamente il pannello delle quotazioni di cambio per assicurarti che il tuo fornitore sincronizzi le quotazioni e che queste sembrino ragionevoli.
- **Considera un sovrapprezzo per valute volatili** - Se supporti valute con alta volatilità, un sovrapprezzo leggermente più elevato (2-3%) può proteggere i tuoi margini.
- **Inizia con le valute principali** - Inizia con valute ampiamente utilizzate (EUR, GBP, JPY, CAD, AUD) e espandi in base alla domanda dei clienti.
- **Verifica la compatibilità con i fornitori di pagamento** - Non tutti i fornitori di pagamento supportano tutte le valute.

Controlla la documentazione del tuo fornitore di pagamento per confermare quali valute gestiscono.
- **Utilizza la modalità Display Only se non sei sicuro** - Se non sei sicuro se il tuo fornitore di pagamento gestisce il checkout multivaluta, inizia con la modalità Display Only.

Puoi passare alla modalità Full Multi-Currency in un secondo momento.
- **Blocca le quotazioni prima dei periodi promozionali** - Se stai svolgendo una promozione, blocca le tue quotazioni di cambio in anticipo per assicurarti che i prezzi siano coerenti durante l'intera promozione.