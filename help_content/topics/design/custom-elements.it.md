---
title: Elementi personalizzati
---

Gli elementi personalizzati ti permettono di creare blocchi del costruttore di pagine riutilizzabili, adatti alle esigenze del tuo negozio. Progetti un elemento in modo visivo utilizzando gli strumenti esistenti del costruttore di pagine, quindi puoi collegarlo facoltativamente a dati live del negozio — come nomi dei prodotti, prezzi o immagini — in modo che l'elemento si popoli automaticamente con contenuti reali quando viene posizionato su una pagina. Una volta creato, i tuoi elementi personalizzati appaiono nella libreria degli elementi del costruttore di pagine insieme ai blocchi predefiniti.

![Libreria Elementi Personalizzati](/static/core/admin/img/help/custom-elements/custom-elements-list.webp)

## Quando utilizzare gli elementi personalizzati

Gli elementi personalizzati sono più utili quando ti trovi a costruire ripetutamente la stessa disposizione. Invece di ricreare una "scheda prodotto in evidenza" da zero su ogni pagina, puoi crearla una volta come elemento personalizzato e posizionarla ovunque ne hai bisogno. Se l'elemento è collegato ai dati, estrae automaticamente le informazioni sui prodotti attuali — non sono necessaggi aggiornamenti manuali quando i prezzi o i nomi cambiano.

Utilizzi comuni:

- Schede di prodotti in evidenza che mostrano nome, prezzo e immagine principale
- Blocchi promozionali di categoria con banner, titolo e link
- Pannelli di presentazione delle marche con logo e descrizione
- Anteprime dei post del blog con immagine in evidenza, titolo e estratto

## Creare un nuovo elemento personalizzato

1. Vai a **Design > Elementi personalizzati**
2. Clicca su **+ Aggiungi elemento personalizzato**
3. Spwig crea immediatamente un elemento bozza e apre il **Costruttore visivo** — non è necessario compilare un modulo prima
4. Nel Costruttore visivo, crea la disposizione del tuo elemento utilizzando gli strumenti disponibili del costruttore di pagine
5. Quando sei soddisfatto del design, configura le impostazioni dell'elemento (nome, collegamento ai dati, icona) nel pannello laterale
6. Imposta **Attivo** su attivo quando sei pronto a pubblicare l'elemento nella libreria
7. Salva l'elemento

L'elemento è ora disponibile nel pannello degli elementi del costruttore di pagine nella categoria che hai assegnato.

## Il costruttore visivo

Il Costruttore visivo è un canvas dedicato per progettare il tuo elemento. Funziona come il costruttore di pagine standard, ma si concentra su un singolo elemento invece che su tutta una pagina. Puoi:

- Aggiungere e disporre elementi figli (blocchi di testo, immagini, contenitori, ecc.)
- Impostare lo stile, lo spazio e la disposizione per ciascun elemento figlio
- Anteprima l'aspetto dell'elemento con dati di esempio

Le modifiche nel Costruttore visivo vengono salvate direttamente alla definizione dell'elemento. Non c'è un passo separato per pubblicare — salvare nel costruttore aggiorna immediatamente l'elemento per qualsiasi pagina che lo utilizza già.

## Configurare le impostazioni dell'elemento

Ogni elemento personalizzato ha queste impostazioni:

| Campo | Descrizione |
|-------|-------------|
| **Nome** | Nome visualizzato nella libreria degli elementi |
| **Slug** | Identificatore sicuro per URL, generato automaticamente dal nome |
| **Descrizione** | Nota opzionale su a cosa serve questo elemento |
| **Modello obiettivo** | Il modello del negozio da cui collegare i dati (vedi di seguito) |
| **Icona** | Icona visualizzata nella libreria degli elementi |
| **Categoria** | Raggruppa gli elementi correlati nella libreria |
| **Attivo** | Se l'elemento è disponibile nel costruttore di pagine |

## Collegamento ai dati

Il collegamento ai dati collega parti della tua disposizione dell'elemento ai dati live del negozio. Quando un editore di pagine posiziona un elemento collegato ai dati su una pagina, seleziona un record specifico (ad esempio, un prodotto), e tutti i campi collegati si popolano automaticamente da quel record.

### Scegliere un modello obiettivo

L'impostazione **Modello obiettivo** determina che tipo di dati del negozio l'elemento può visualizzare. I modelli disponibili sono:

| Modello | Cosa fornisce |
|-------|-----------------|
| **Prodotto** | Nome, prezzo, stato di disponibilità, immagini, descrizione, SKU, categoria, marca e altro |
| **Categoria** | Nome, descrizione, immagine, banner, numero di prodotti e URL |
| **Marca** | Nome, logo, descrizione, storia della marca e URL |
| **Post del blog** | Titolo, estratto, immagine in evidenza, autore, data di pubblicazione e URL |

Lascia **Modello obiettivo** vuoto per creare un elemento statico senza dati dinamici. Gli elementi statici sono utili per componenti di design fissi come banner decorativi o spaziatori di layout.

### Come funzionano i collegamenti


All'interno del Visual Builder, puoi contrassegnare singoli elementi figlio come dati associati selezionando il campo del modello che devono visualizzare.

Per esempio:
- Un elemento figlio **testo** può essere associato a **Product Name**, in modo da mostrare il nome del prodotto selezionato
- Un elemento figlio **immagine** può essere associato a **Main Image**, in modo da mostrare la foto principale del prodotto
- Un elemento figlio **testo** può essere associato a **Price**, in modo da riflettere sempre il prezzo corrente

Ogni associazione mappa un campo del contenuto di un elemento a un campo del modello. Puoi aggiungere più associazioni a un singolo elemento personalizzato — ad esempio, associare un blocco di testo a **Product Name** e un blocco immagine separato a **Main Image** nello stesso momento.

### Presetti per miniature di immagine

Per le associazioni delle immagini, puoi specificare opzionalmente un **Thumbnail Preset** (ad esempio `thumbnail` o `medium`). Questo controlla le dimensioni dell'immagine caricata, aiutando le pagine a caricarsi più velocemente servendo l'immagine di dimensioni appropriate per il layout dell'elemento.

## Disattivare e riattivare gli elementi

Disattivare un elemento lo rimuove dalla libreria degli elementi in modo che non possa essere aggiunto a nuove pagine. Le pagine esistenti che utilizzano già l'elemento non sono interessate — l'elemento continua a rendersi su quelle pagine.

Per disattivare:
1. Vai a **Design > Custom Elements**
2. Fai clic sul nome dell'elemento
3. Disattiva **Active**
4. Salva

Per riattivare, segui gli stessi passaggi e riattiva **Active**.

## Filtrare la libreria degli elementi

L'elenco degli elementi supporta il filtraggio per:
- **Active / Inactive** — mostra solo gli elementi pubblicati o solo gli elementi bozza
- **Target Model** — filtra per il modello a cui un elemento è associato
- **Category** — filtra per categoria dell'elemento
- **Search** — cerca per nome, slug o descrizione

Questo è utile quando hai molti elementi personalizzati e devi trovare uno specifico velocemente.

## Esempio: card di evidenziazione prodotto

**Obiettivo:** Una card elemento che mostra l'immagine principale, il nome e il prezzo di un prodotto.

| Impostazione | Valore |
|---------|-------|
| Nome | Product Highlight Card |
| Target Model | Product |
| Categoria | Products |
| Icon | fas fa-box |

Nel Visual Builder, aggiungi:
- Un elemento **Image** associato a **Main Image** con preset di miniature `medium`
- Un elemento **Text** associato a **Product Name**
- Un elemento **Text** associato a **Price**

Una volta salvato e attivato, l'elemento appare nel costruttore di pagine nella categoria Products. Quando un editore di pagine lo aggiunge a una pagina, seleziona quale prodotto evidenziare e la card si popola automaticamente.

## Consigli

- Assegna ai nomi degli elementi nomi descrittivi che includano lo scopo e il tipo di dati — ad esempio, "Product Highlight Card" invece di "Card 1" — in modo che la libreria rimanga facile da navigare man mano che cresce
- Utilizza il campo **Category** per raggruppare gli elementi correlati (Products, Blog, Promotions) — questo mantiene organizzata la libreria degli elementi per gli editor delle pagine
- Testa gli elementi associati ai dati aggiungendoli a una pagina bozza e selezionando un record reale prima di pubblicare, per confermare che l'associazione stia recuperando le informazioni corrette
- Disattiva gli elementi obsoleti invece di eliminarli — questo preserva eventuali pagine che li fanno ancora riferimento e ti dà l'opzione di riattivarli in un secondo momento
- Gli elementi statici (nessun modello target) sono ideali per i modelli di layout che si riutilizzano in tutto il sito, ad esempio separatori, pannelli CTA o spaziatori marchiati