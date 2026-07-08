---
title: Gestione del Blog
---

Il blog ti permette di pubblicare articoli, guide e notizie per generare traffico e coinvolgere il tuo pubblico. Il blog di Spwig include un editor di testo avanzato, la pubblicazione programmata, le notifiche ai sottoscrittori, la condivisione automatica su social media e strumenti SEO.

![Blog posts](/static/core/admin/img/help/blog-management/blog-post-list.webp)

## Creare un Post del Blog

Naviga verso **Marketing > Blog Posts** e fai clic su **Add Post**.

### Contenuto del Post

Scrivi il tuo post utilizzando l'editor di testo avanzato **CKEditor 5**, che supporta:
- Formattazione del testo (titoli, grassetto, corsivo, elenchi, citazioni)
- Immagini e media (caricati tramite la libreria media)
- Video incorporati (YouTube, Vimeo)
- Tabelle e blocchi di codice
- Link a prodotti, categorie e URL esterni

Per layout più complessi, attiva l'interruttore **Page Builder** per utilizzare l'editor di pagina a trascinamento invece dell'editor di testo.

### Impostazioni del Post

| Impostazione | Descrizione |
|---------|-------------|
| **Titolo** | Il titolo principale visualizzato nel blog e nei risultati di ricerca |
| **Slug** | Identificatore amico degli URL (generato automaticamente dal titolo, modificabile) |
| **Estratto** | Breve riassunto visualizzato nelle schede dell'elenco del blog e nei feed RSS |
| **Immagine in evidenza** | Immagine principale visualizzata in alto nel post e nelle schede dell'elenco |
| **Categoria** | Categoria principale per il post |
| **Tags** | Parole chiave per la filtratura e il contenuto correlato |
| **Autore** | Membro dello staff creditato come autore |
| **Stato** | Bozza, Pubblicato, Pubblicato o Archiviato |
| **In evidenza** | Fissa il post in alto nell'elenco del blog |

### Impostazioni SEO

Ogni post include campi SEO:
- **Meta Title** — Titolo personalizzato per i risultati dei motori di ricerca (predefinito come titolo del post)
- **Meta Description** — Riassunto visualizzato nei risultati dei motori di ricerca
- **Open Graph Image** — Immagine utilizzata quando il post viene condiviso su social media

## Stati dei Post

| Stato | Descrizione |
|--------|-------------|
| **Bozza** | Lavoro in corso, non visibile al pubblico |
| **Pubblicato** | Sarà pubblicato automaticamente in una data e ora specifiche |
| **Pubblicato** | Attivo e visibile ai visitatori |
| **Archiviato** | Nascosto dall'elenco del blog ma ancora accessibile tramite URL diretto |

### Pubblicazione Programmata

Per programmare la pubblicazione di un post in futuro:
1. Imposta lo stato su **Pubblicato**
2. Scegli la **data e l'ora di pubblicazione**
3. Salva il post

Un compito in background pubblica automaticamente il post all'ora programmata e attiva le notifiche ai sottoscrittori.

## Categorie

Naviga verso **Marketing > Blog Categories** per organizzare il tuo contenuto.

Le categorie supportano:
- **Gerarchia** — Crea categorie principali e secondarie (es. "Guides" > "Getting Started")
- **URL personalizzati** — Ogni categoria ha il proprio slug per URL puliti
- **Descrizioni** — Aggiungi descrizioni delle categorie visualizzate sulla pagina dell'archivio delle categorie
- **Ordinamento** — Controlla l'ordine di visualizzazione delle categorie nella navigazione

## Tags

I tag forniscono un secondo modo per classificare il contenuto. A differenza delle categorie (che sono gerarchiche), i tag sono etichette piatte. I visitatori possono cliccare su un tag per visualizzare tutti i post con quel tag.

## Sottoscrittori

Naviga verso **Marketing > Blog Subscribers** per gestire la tua lista dei sottoscrittori.

### Funzionamento delle Sottoscrizioni

1. I visitatori si iscrivono tramite un modulo sul blog (richiesto l'indirizzo email)
2. Viene inviata una **conferma a doppio opt-in**
3. Una volta confermata, il sottoscrittore riceve notifiche quando vengono pubblicati nuovi post

### Frequenza delle Notifiche

I sottoscrittori scelgono con che frequenza ricevono le notifiche:

| Frequenza | Descrizione |
|-----------|-------------|
| **Immediata** | Email inviata non appena un nuovo post viene pubblicato |
| **Riepilogo Settimanale** | Un riepilogo settimanale di tutti i nuovi post |
| **Riepilogo Mensile** | Un riepilogo mensile di tutti i nuovi post |

I compiti in background gestiscono automaticamente la compilazione e la consegna dei riepiloghi.

### Gestione dei Sottoscrittori

- Visualizza il numero di sottoscrittori, lo stato di conferma e la data di iscrizione
- Esporta le liste dei sottoscrittori per l'uso in strumenti esterni di marketing email
- Rimuovi o disiscriviti da singoli indirizzi
- Ogni email di notifica include un link per la disiscrizione con un solo clic

## Condivisione Automatica sui Social Media

Spwig può condividere automaticamente i nuovi post sui tuoi account di social media quando vengono pubblicati.

### Connessione degli Account Social

Naviga verso **Marketing > Social Connectors** per connettere i tuoi account:

| Piattaforma | Autenticazione |
|----------|---------------|
| **Facebook** | OAuth — connetti la tua pagina Facebook |
| **Instagram** | OAuth — connetti il tuo account aziendale |
| **LinkedIn** | OAuth — connetti la tua pagina aziendale |

### Funzionamento della Condivisione Automatica

1. Connetti uno o più account social
2. Quando crei un post, attiva **Auto Share** per ogni account connesso
3. Personalizza il messaggio di condivisione (predefinito come titolo del post e estratto)
4. Quando il post viene pubblicato (o raggiunge l'ora programmata), viene condiviso automaticamente

La condivisione automatica funziona anche con i post programmati — la condivisione sui social viene inviata nello stesso momento in cui il post va online.

## RSS Feed

Il blog genera automaticamente un feed RSS a `/blog/feed/`. Questo permette ai visitatori e agli aggregatori di iscriversi al tuo contenuto. Il feed include:
- Titolo del post e estratto
- Data di pubblicazione
- Informazioni sull'autore
- Link diretto all'articolo completo

## Impostazioni del Blog

Naviga verso **Marketing > Blog Settings** per configurare le opzioni globali del blog:

- **Posts Per Page** — Numero di post visualizzati per pagina nell'elenco
- **Allow Comments** — Abilita o disabilita i commenti sui post
- **Default Category** — Categoria di default per i post senza categoria assegnata
- **Social Sharing Buttons** — Mostra i pulsanti di condivisione sulle pagine dei singoli post

## Consigli

- Scrivi i post tenendo presente l'**SEO** — utilizza titoli descrittivi, compila le descrizioni meta e include parole chiave rilevanti in modo naturale nel contenuto.
- Utilizza la **pubblicazione programmata** per mantenere un ritmo di pubblicazione costante senza sforzo manuale.
- Abilita la **condivisione automatica** per massimizzare il raggiungimento — i post condivisi sui social media poco dopo la pubblicazione ottengono il maggior coinvolgimento.
- Incoraggia i visitatori a **iscriversi** posizionando il modulo di iscrizione in modo prominente sul tuo blog e utilizzando un call to action convincente.
- Utilizza le **categorie** per gruppi di contenuti ampi e i **tag** per argomenti specifici — questo aiuta i visitatori a trovare contenuti correlati.
- Aggiungi un'**immagine in evidenza** a ogni post — i post con immagini ottengono migliori risultati nei motori di ricerca e nelle condivisioni sui social media.
- Utilizza l'opzione **riepilogo settimanale o mensile** per i sottoscrittori che non desiderano ricevere email frequenti — riduce il tasso di disiscrizione.