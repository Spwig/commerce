---
title: Personalizzazione del Modello di Ricevuta
---

I modelli di ricevuta controllano l'aspetto e il contenuto delle ricevute termiche stampate sui terminali POS. Personalizza il testo dell'intestazione e del piè di pagina, aggiungi il tuo logo, configura i campi obbligatori (numeri di identificazione fiscale, numeri di registrazione aziendale) e include codici QR promozionali. I modelli supportano la selezione per ambito - crea un modello predefinito per tutti i negozi, modelli specifici per gruppi per regioni o modelli specifici per negozi per singole ubicazioni. Il sistema utilizza le regole di precedenza per ambito per determinare quale modello si applica quando si stampa una ricevuta.

Utilizza i modelli di ricevuta per mantenere la coerenza del brand, soddisfare i requisiti normativi regionali e migliorare l'engagement dei clienti attraverso elementi promozionali.

![Elenco dei modelli di ricevuta](/static/core/admin/img/help/receipt-template-customization/receipt-list.webp)

## Nozioni di base sui modelli di ricevuta

I modelli di ricevuta definiscono la struttura e il contenuto delle ricevute stampate da stampanti termiche ESC/POS. Ogni modello specifica:

**Configurazione fisica**:
- Larghezza della carta (58mm o 80mm)
- Immagine del logo (in monocromatico per la stampa termica)
- Dimensioni e spaziatura dei caratteri

**Sezioni del contenuto**:
- Testo dell'intestazione (nome del negozio, indirizzo, informazioni di contatto)
- Dati dinamici della transazione (articoli, prezzi, totali, metodi di pagamento)
- Testo del piè di pagina (politica di resi, messaggio di ringraziamento, social media)
- Campi obbligatori (numeri di identificazione fiscale, numeri di registrazione aziendale)
- Codice QR promozionale con etichetta

**Selezione per ambito**:
- Modello predefinito (si applica a tutti i negozi a meno che non venga sovrascritto)
- Modello per gruppo (si applica a tutti i negozi in un gruppo)
- Modello per negozio (si applica a un negozio specifico/centro di magazzino)

## Regole di precedenza per ambito

Quando un terminale stampa una ricevuta, il sistema seleziona un modello utilizzando questa gerarchia (priorità più alta a priorità più bassa):

| Priorità | Ambito | Esempio | Caso d'uso |
|----------|-------|---------|----------|
| **1** | Specifico del negozio | Modello del negozio di Parigi | Requisiti normativi francesi unici |
| **2** | Specifico del gruppo | Modello per negozi europei | Visualizzazione IVA per tutte le ubicazioni dell'UE |
| **3** | Predefinito | Modello globale | Rientro di default per tutti i negozi non configurati |

**Come funziona**:
1. Verifica se il negozio ha un modello dedicato (specifico del magazzino)
2. Se non è presente, verifica se il gruppo del negozio ha un modello per gruppo
3. Se non è presente, utilizza il modello predefinito

**Esempio**:
- Modello predefinito: "Ricevuta Standard" (nessun assegnamento di ambito)
- Modello per gruppo: "Ricevuta UE" (assegnato al gruppo di negozi europei) - include la registrazione IVA
- Modello per negozio: "Ricevuta di Parigi" (assegnato al magazzino di Parigi) - include il numero SIRET francese

**Risultato**:
- Terminale del negozio di Parigi: Utilizza "Ricevuta di Parigi" (più specifico)
- Terminale del negozio di Berlino (nel gruppo di negozi europei, senza modello per negozio): Utilizza "Ricevuta UE" (livello di gruppo)
- Terminale del negozio di New York (nessun gruppo, nessun modello per negozio): Utilizza "Ricevuta Standard" (rientro predefinito)

## Configurazione della larghezza della carta

Le stampanti termiche per ricevute utilizzano una larghezza della carta di 58mm o 80mm. Scegli in base al tuo hardware della stampante:

| Larghezza carta | Caratteri per riga | Migliore per | Utilizzo tipico |
|----------------|------------------|-------------|----------------|
| **58mm** | ~32 caratteri | Piccolo ingombro, portatile | Tiratori di cibo, POS mobili, kioschi |
| **80mm** | ~48 caratteri | Retail standard | La maggior parte dei negozi al dettaglio, ristoranti |

**Non è possibile mescolare le larghezze**: Tutti i terminali che utilizzano lo stesso modello devono avere la stessa larghezza della carta. Se hai tipi di stampante misti, crea modelli separati per ogni larghezza.

**Limiti delle dimensioni del logo**:
- **58mm**: Larghezza massima 384 pixel (consigliato: 350px)
- **80mm**: Larghezza massima 576 pixel (consigliato: 550px)

I loghi che superano la larghezza massima vengono ridimensionati automaticamente, il che potrebbe ridurre la qualità.

## Configurazione del logo

I loghi delle ricevute devono essere **monocromatici** (solo nero e bianco) per la compatibilità con le stampanti termiche:

**Requisiti del logo**:
- Formato del file: PNG, JPG o WebP
- Modalità di colore: Monocromatico (pixel neri su sfondo bianco)
- Dimensioni consigliate:
  - Carta 58mm: 350px di larghezza × 100-150px di altezza
  - Carta 80mm: 550px di larghezza × 150-200px di altezza
- Dimensione del file: <100KB (le stampanti termiche hanno memoria limitata)

**Creazione di loghi monocromatici**:
1. Parti dal tuo logo regolare (a colori o in scala di grigi)
2. Utilizza un editor di immagini per convertirlo in nero e bianco puro (nessun grigio)
3. Aumenta il contrasto per assicurarti che gli elementi neri siano solidi
4. Esporta come PNG con sfondo trasparente o bianco

**Posizionamento del logo**:
- Sempre centrato orizzontalmente
- Stampa in alto sulla ricevuta (sopra il testo dell'intestazione)
- Seguito da uno spazio automatico (evita l'affollamento con il contenuto)

**Selezione del logo**:
- Fai clic su **Sfoglia la libreria media** nel modulo del modello
- Seleziona l'asset del logo monocromatico
- La previsione mostra come apparirà il logo sulla ricevuta

**Nessun logo**: Lascia il campo del logo vuoto se preferisci una branding basata solo sul testo (il testo dell'intestazione può includere il nome del negozio).

## Testo dell'intestazione

Il testo dell'intestazione appare immediatamente dopo il logo (o in alto se non c'è logo). Contenuto tipico:

**Nome del negozio e indirizzo**:
```
Your Store Name
123 Main Street
City, State 12345
Phone: (555) 123-4567
```

**Orari di apertura**:
```
Lunedì-Venerdì: 9am-9pm
Sabato-Domenica: 10am-6pm
```

**Slogan o tagline**:
```
Quality Products, Exceptional Service
```

**Formattazione**:
- Utilizza gli interruzioni di riga per separare le informazioni
- Allineamento centrale automatico
- Mantieni le righe sotto il limite di caratteri per la larghezza della carta (32 caratteri per 58mm, 48 per 80mm)

**Variabili disponibili** (opzionale):
- `{store_name}` - Sostituito con il nome del magazzino
- `{order_date}` - Sostituito con la data della transazione
- `{order_number}` - Sostituito con l'ID dell'ordine

La maggior parte dei commercianti utilizza il testo statico invece delle variabili per la coerenza dell'intestazione.

## Testo del piè di pagina

Il testo del piè di pagina appare dopo i dettagli della transazione (articoli, totali, pagamento). Contenuto tipico:

**Politica di resi**:
```
Resi entro 30 giorni con ricevuta
Solo credito per il negozio o scambio
```

**Messaggio di ringraziamento**:
```
Grazie per lo shopping con noi!
Seguici @yourstore
```

**Servizio clienti**:
```
Domande? Chiama (555) 123-4567
o invia un'e-mail a support@yourstore.com
```

**Consigli per la formattazione**:
- Mantieni le informazioni più importanti in alto (politica di resi, contatti)
- Utilizza gli interruzioni di riga per la leggibilità
- Considera l'aggiunta di una riga separatrice (`---`) tra le sezioni

## Campi obbligatori

Molti territori richiedono informazioni specifiche sulle ricevute:

**Etichetta del numero di identificazione fiscale** - Etichetta personalizzabile per il numero di identificazione fiscale:
- USA: "Tax ID" o "EIN"
- UE: "VAT Number" o "VAT Reg No"
- Canada: "GST/HST Number"
- Australia: "ABN"

**Valore del numero di identificazione fiscale** - Il numero di identificazione effettivo:
- Inserito una volta nel modello, appare su tutte le ricevute
- Esempio: "VAT Number: GB123456789"

**Etichetta del numero di registrazione aziendale** - Etichetta personalizzabile per la registrazione aziendale:
- Francia: "SIRET"
- Germania: "Handelsregister"
- Regno Unito: "Company Registration Number"

**Valore del numero di registrazione aziendale** - Il numero di registrazione effettivo:
- Esempio: "SIRET: 123 456 789 00010"

**Mostra Powered by Spwig** - Interruttore per visualizzare o nascondere il branding "Powered by Spwig" (supporta lo sviluppo della piattaforma):
- Abilitato per impostazione predefinita (supporta lo sviluppo della piattaforma)
- Disabilita per operazioni white-label

**Esempi di conformità per regione**:

**Unione Europea**:
- Etichetta del numero di identificazione fiscale: "VAT Number"
- Valore del numero di identificazione fiscale: "GB123456789"
- Visualizza il numero di registrazione aziendale se richiesto dal paese

**Stati Uniti**:
- Generalmente nessun requisito di numero di identificazione fiscale sulle ricevute (varia per stato)
- Potrebbe includere EIN per transazioni B2B

**Francia (specifico)**:
- SIRET obbligatorio su tutte le ricevute
- Etichetta del numero di registrazione aziendale: "SIRET"
- Valore del numero di registrazione aziendale: "123 456 789 00010"

**Australia**:
- ABN (Australian Business Number) raccomandato per aziende registrate per l'IVA
- Etichetta del numero di identificazione fiscale: "ABN"

Verifica i requisiti locali per le ricevute prima di andare online.

## Promozioni con codici QR

Includi un codice QR in fondo alle ricevute per stimolare l'engagement dei clienti:

**URL del codice QR** - Destinazione quando viene scansionato:
- Richiesta di recensione: `https://yourstore.com/reviews/leave-review`
- Programma fedeltà: `https://yourstore.com/loyalty/join`
- Sconto per prossimo acquisto: `https://yourstore.com/discount/THANKYOU`
- Social media: `https://instagram.com/yourstore`
- Homepage del sito web: `https://yourstore.com`

**Etichetta del codice QR** - Testo visualizzato sopra il codice QR:
- "Scansiona per lasciare una recensione e ottenere il 10% di sconto sul prossimo acquisto"
- "Unisciti al nostro programma fedeltà - Scansiona qui"
- "Seguici su Instagram - Scansiona per connetterti"
- "Valuta la tua esperienza"

**Linee guida per i codici QR**:
- Utilizza URL brevi (URL lunghi creano codici QR densi e difficili da scansionare)
- Testa il codice QR con diverse telecamere di smartphone prima del deployment
- Includi una chiara proposta di valore nell'etichetta (cosa riceve il cliente per la scansione)
- Traccia le scansioni del codice QR per misurare l'efficacia (utilizza un URL con un parametro di tracciamento)

**Codici QR dinamici** (avanzato):
- Utilizza un servizio di ridirezione QR (bit.ly, tinyurl) per creare un URL breve
- Punta la ridirezione a destinazioni diverse a seconda della stagione senza dover ristampare le ricevute
- Esempio: `https://bit.ly/yourstoreqr` → ridirige al promozione corrente

## Creare modelli per diversi ambiti

**Modello predefinito** (punto di partenza consigliato):
1. Naviga a **POS > Receipt Templates**
2. Clicca su **+ Aggiungi modello di ricevuta**
3. Lascia i campi **Warehouse** e **Store Group** vuoti (questo lo rende il modello predefinito)
4. Configura la larghezza della carta corrispondente al tipo di stampante più comune
5. Aggiungi logo, intestazione, piè di pagina
6. Configura i campi obbligatori per il tuo mercato principale
7. Salva

Questo modello si applica a tutti i negozi a meno che non venga sovrascritto.

**Modello per gruppo** (per variazioni regionali):
1. Crea un nuovo modello
2. Seleziona **Store Group** (es. "European Stores")
3. Lascia **Warehouse** vuoto
4. Modifica i campi obbligatori per la regione (es. formattazione IVA)
5. Modifica il testo dell'intestazione (es. indirizzo regionale)
6. Salva

Questo modello si applica a tutti i negozi nel gruppo.

**Modello per negozio** (per esigenze specifiche dell'ubicazione):
1. Crea un nuovo modello
2. Seleziona **Warehouse** (es. "Paris Store")
3. Modifica tutti i campi per questa ubicazione specifica
4. Salva

Questo modello si applica solo a questo singolo negozio.

**Test dei modelli**:
- Processa una transazione di test sul terminale
- Stampa la ricevuta
- Verifica la chiarezza del logo, l'allineamento del testo, i campi obbligatori, la scansionabilità del codice QR
- Modifica il modello e riprova se necessario

## Layout tipici delle ricevute

**Ricevuta minima** (tiratori di cibo, pop-up):
- Nessun logo (risparmio di spazio)
- Intestazione: solo nome del negozio e numero di telefono
- Piè di pagina: messaggio di ringraziamento
- Nessun codice QR

**Ricevuta standard per il retail**:
- Logo (marchio monocromatico)
- Intestazione: nome completo del negozio, indirizzo, orari
- Conformità: numero di identificazione fiscale
- Piè di pagina: politica di resi, messaggio di ringraziamento
- Codice QR: richiesta di recensione

**Ricevuta premium per il retail**:
- Logo (marchio completo del brand)
- Intestazione: slogan, indirizzo, contatti
- Conformità: numero di identificazione fiscale, numero di registrazione aziendale
- Piè di pagina: politica di resi, servizio clienti, social media
- Codice QR: iscrizione al programma fedeltà

**Catena multi-ubicazione**:
- Modello predefinito: branding aziendale, politiche standard
- Modelli per gruppo: conformità regionale (IVA per UE, GST per Canada)
- Modelli per negozio: indirizzo e numero di telefono specifici per l'ubicazione

## Gestione di più modelli

**Convenzione per il nome dei modelli**:
- Utilizza l'ambito nel nome: "Modello predefinito", "Modello del gruppo UE", "Modello del negozio di Parigi"
- Aiuta a identificare quale modello si applica dove quando si esamina l'elenco

**Modifiche al modello**:
- Le modifiche si applicano immediatamente alle ricevute future
- Le ricevute passate (già stampate) non sono influenzate
- Testa le modifiche su un terminale con poca affluenza prima di distribuirle a tutti i negozi

**Duplicazione dei modelli**:
- Quando si crea un nuovo modello simile a uno esistente, duplica il modello esistente e modifica
- Evita di iniziare da zero

**Cancellazione dei modelli**:
- Non è possibile cancellare il modello predefinito mentre esistono terminali (deve esserci un rientro)
- È possibile cancellare i modelli per gruppo/negozio (i terminali si rientrano al livello successivo nella gerarchia)
- Conferma che nessun terminale stia utilizzando attivamente il modello prima di cancellarlo

## Consigli

- **Inizia con 80mm se non sei sicuro** - La larghezza standard della carta funziona per la maggior parte del retail; 58mm è specializzato
- **Testa il logo sulla stampante reale** - Ciò che sembra buono a schermo potrebbe stampare male; testa presto
- **Mantieni aggiornati i campi obbligatori** - I numeri di registrazione fiscale scaduti sulle ricevute creano problemi legali
- **I codici QR con proposta di valore scansionano meglio** - "Scansiona per ottenere il 10% di sconto" supera "Scansiona qui" di 10 volte
- **Rivedi i limiti di caratteri** - Il wrapping del testo rovina la formattazione; conta i caratteri per riga prima di distribuire
- **Un modello per ogni larghezza della carta** - Non assegnare un modello per 80mm a un terminale con stampante 58mm (il logo non entrerà)
- **Stampa ricevute di test mensilmente** - Le stampanti degradano nel tempo; verifica che la qualità rimanga accettabile
- **Utilizza le variabili con parsimonia** - Il testo statico è più affidabile delle variabili dinamiche (punti di fallimento minori)
- **Fai backup della configurazione del modello** - Fai uno screenshot o esporta le impostazioni del modello prima di modifiche importanti (facile rollback)
- **La conformità regionale varia** - Ricerca i requisiti locali per le ricevute prima del deployment; le sanzioni per non conformità possono essere severe