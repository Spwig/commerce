---
title: 3D Configuratore di prodotti
---

Il 3D Configuratore consente ai tuoi clienti di visualizzare i prodotti configurabili in un visualizzatore 3D interattivo direttamente sulla pagina del prodotto. Mentre i clienti selezionano le opzioni — come colori, materiali o variazioni dei componenti — il modello 3D si aggiorna in tempo reale per riflettere le loro scelte. Su dispositivi mobili supportati, i clienti possono anche visualizzare il prodotto in realtà aumentata (AR), posizionandolo virtualmente nello spazio in cui si trovano prima dell'acquisto.

Il 3D Configuratore funziona con prodotti configurabili. Ogni prodotto configurabile può avere una configurazione di scena 3D che collega un file modello GLB alle opzioni di configurazione del prodotto.

## Prima di iniziare

Per impostare una scena 3D, hai bisogno di:

- Un **prodotto configurabile** già creato nel tuo catalogo
- Un **modello 3D base** caricato nella tua Libreria Media come file GLB — questo è il modello assemblato che appare di default
- Opzionalmente, ulteriori file GLB per scambi di geometria (es. forme di collo diversi), e immagini di texture per variazioni dei materiali

Se non hai già creato il prodotto configurabile e le sue opzioni di configurazione, fallo prima di impostare la scena 3D.

## Creare una configurazione della scena

1. Vai a **Catalogo > Configurazioni Scene 3D**
2. Fai clic su **+ Aggiungi Configurazione Scene 3D**
3. Seleziona il **Prodotto** a cui appartiene questa scena — sono disponibili solo prodotti configurabili
4. Scegli il **Modello 3D Base** dalla tua Libreria Media — questo è il file GLB che si carica di default
5. Configura le impostazioni del visualizzatore (vedi di seguito)
6. Salva il record

Dopo aver salvato, il campo **Albero dei nodi** si popola automaticamente. Questo è il grafo della scena analizzato estratto dal tuo file GLB — elenca ogni nodo nominato all'interno del modello, che farai riferimento quando aggiungi le mappature dei nodi.

## Impostazioni del visualizzatore

Queste impostazioni controllano come appare il visualizzatore 3D sulla tua pagina del prodotto.

### Camera e illuminazione

| Campo | Descrizione | Default |
|-------|-------------|---------|
| **Orbita della Camera** | Posizione iniziale della camera nel formato `angolo elevazione distanza` (es. `0deg 75deg 2m`) | `0deg 75deg 2m` |
| **Punto di mira della Camera** | Il punto a cui la camera guarda, in metri dalla centro del modello (es. `0m 0m 0m`) | `0m 0m 0m` |
| **Immagine dell'ambiente** | Un'immagine HDR dalla tua Libreria Media utilizzata per l'illuminazione basata sull'immagine — fornisce riflessi e ombre più realistici | Nessuna |
| **Esposizione** | Luminosità complessiva della scena — valori più bassi sono più scuri, valori più alti sono più luminosi | `1.0` |

### Ombre

| Campo | Descrizione | Default |
|-------|-------------|---------|
| **Intensità dell'ombra** | Quanto forte appare l'ombra sotto il modello — `0` non c'è ombra, `1` è intensità massima | `0.5` |
| **Softness dell'ombra** | Quanto sfumata è l'edge dell'ombra — `0` è netto, `1` è molto morbido | `0.5` |

### Grading dei colori

| Campo | Descrizione |
|-------|-------------|
| **Mapping del tono** | L'algoritmo di grading dei colori applicato alla scena. **Commerce** produce colori vivaci e adatti ai prodotti. **Neutro** è accurato nei colori. **ACES** dà un aspetto cinematografico.
| **Forza del glow** | Aggiunge un effetto di glow alle parti emittenti (autoluminescenti) del modello. `0` disattiva il glow. I valori tra `1` e `5` producono un glow sottile a drammatico.

### Comportamento e background

| Campo | Descrizione | Default |
|-------|-------------|---------|
| **Ruota automaticamente** | Se il modello gira lentamente al caricamento per attirare l'attenzione del cliente | Attivo |
| **AR abilitata** | Se i clienti su dispositivi supportati vedono un pulsante **Visualizza in AR** | Attivo |
| **Background** | Il colore di sfondo del visualizzatore o il gradiente CSS — inserisci un colore esadecimale (es. `#f5f5f5`) o un valore di gradiente CSS | `#ffffff` |

### Miniatura

Il campo **Miniatura** contiene una screenshot anteprima del visualizzatore 3D, visualizzata prima del caricamento del visualizzatore. Puoi catturare una screenshot dalla pagina del prodotto live e caricarla nella tua Libreria Media, quindi collegarla qui per un'esperienza di caricamento della pagina più fluida.

## Abilitare e disabilitare il visualizzatore 3D

L'interruttore **Abilitato** controlla se il visualizzatore 3D viene mostrato sulla pagina del prodotto.

Quando disattivato, il prodotto torna al configuratore standard 2D.

Questo ti permette di preparare una configurazione della scena prima di renderla visibile ai clienti.

## Collegamento delle opzioni di configurazione alle azioni 3D

Una volta configurata la scena base, puoi collegare ogni opzione del slot di configurazione a un cambiamento visivo nel modello 3D. Questi collegamenti vengono chiamati **Node Mappings** e vengono aggiunti nella sezione **Node Mappings** in fondo al modulo di configurazione della scena.

### Campi di mapping dei nodi

| Campo | Descrizione |
|-------|-------------|
| **Opzione del Slot** | L'opzione di configurazione che attiva questo cambiamento (es. "Red Leather") |
| **Tipo di Azione** | Cosa accade visivamente (vedi i tipi di azione di seguito) |
| **Nodo Target** | Il nome del nodo del grafo della scena che cambia — scegli tra i nomi elencati nel tuo **Node Tree** |
| **Dati dell'Azione** | Dati specifici per l'azione, come un codice colore esadecimale, un URL di texture o un URL di file GLB |
| **Ordine di Sort** | Controlla l'ordine in cui vengono applicati diversi mapping per la stessa opzione |

### Tipi di azione

| Azione | Cosa fa |
|--------|-------------|
| **Colore del Materiale** | Cambia il colore di un materiale nel nodo target — fornisci un colore esadecimale in **Dati dell'Azione** |
| **Texture del Materiale** | Sostituisce la texture applicata a un materiale — collega un'immagine di texture nell'**Action Data** |
| **Sostituzione della Geometria** | Sostituisce una parte del modello con un diverso file GLB — utile per cambiamenti strutturali come una forma diversa di maniglia |
| **Visibilità** | Mostra o nasconde un nodo nella scena — imposta `visible: true` o `visible: false` in **Action Data** |

Possono essere aggiunti più mapping per una singola opzione del slot. Ad esempio, selezionando "Blue Denim" potrebbe cambiare il colore del materiale *e* nascondere un nodo di finitura in pelle allo stesso tempo.

## Asset geometrici

Se la tua configurazione include azioni **Geometry Swap**, devi registrare i file GLB di sostituzione come Asset Geometrici. Questi vengono aggiunti nella sezione **Geometry Assets** del modulo di configurazione della scena.

| Campo | Descrizione |
|-------|-------------|
| **Etichetta** | Nome descrittivo per questo asset geometrico, ad esempio "V-Neck Collar" |
| **File GLB** | Il file GLB di sostituzione dal tuo Media Library |
| **Nodo Target** | Quale nodo nel modello base questo asset geometrico sostituisce |

Dopo aver salvato un Asset Geometrico, i nomi dei nodi vengono analizzati dal GLB e archiviati in **Node Data**, rendendoli disponibili come nodi target nei tuoi mapping.

## Asset di texture

Le immagini di texture utilizzate nei mapping **Material Texture** possono essere registrate come Asset di Texture per un riferimento più semplice. Questi vengono aggiunti nella sezione **Texture Assets**.

| Campo | Descrizione |
|-------|-------------|
| **Etichetta** | Nome descrittivo, ad esempio "Red Leather" |
| **Immagine di Texture** | L'immagine di texture dal tuo Media Library |
| **Tipo di Texture** | Il canale PBR a cui questa texture si applica — Base Color, Normal Map, Roughness Map, Metalness Map, Ambient Occlusion o Emissive Map |

## Esempio: giacca configurabile con opzioni di colore

**Scenario:** Una giacca che può essere ordinata in Nero, Blu marino o Borgogna, con ciascun colore applicato alla mesh del corpo della giacca.

**Configurazione:**

1. Crea una configurazione della scena per il prodotto giacca con il file GLB della giacca assemblata come modello base
2. Imposta **Tone Mapping** su Commerce e **Auto Rotate** su attivo
3. In Node Mappings, aggiungi tre voci — una per ogni opzione di colore:

| Opzione del Slot | Tipo di Azione | Nodo Target | Dati dell'Azione |
|------------------|----------------|-------------|------------------|
| Nero | Colore del Materiale | JacketBody | `"{\"color\": \"#1a1a1a\"}"` |
| Blu marino | Colore del Materiale | JacketBody | `"{\"color\": \"#1b2a4a\"}"` |
| Borgogna | Colore del Materiale | JacketBody | `"{\"color\": \"#6b2737\"}"` |

Quando un cliente seleziona Blu marino sulla pagina del prodotto, il visualizzatore aggiorna immediatamente il materiale JacketBody al colore blu marino.

## Consigli

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- Assegna ai nodi GLB nomi chiari quando crei il tuo modello 3D — nomi dei nodi come "JacketBody" o "CollarMesh" sono molto più facili da utilizzare rispetto ai nomi generati automaticamente come "Mesh_023"
- Utilizza la mappatura del tono **Commerce** per la maggior parte dei prodotti — è ottimizzata per una presentazione del prodotto vivace e attraente
- Disattiva **Auto Rotate** per i prodotti in cui l'angolazione della fotocamera predefinita mostra già le caratteristiche più importanti, per evitare di disorientare il cliente all'avvio
- Testa il pulsante AR su un dispositivo mobile reale prima di promuoverlo — la disponibilità di AR dipende dal dispositivo e dal browser del cliente (iOS Safari e Android Chrome con supporto WebXR sono i più affidabili)
- Carica un'immagine **Thumbnail** per ogni configurazione della scena — questo evita che appaia una scatola bianca vuota mentre il visualizzatore 3D si carica
- Se il visualizzatore 3D non è ancora pronto, disattivalo tramite l'interruttore **Enabled** in modo che i clienti vedano invece il configuratore delle immagini standard