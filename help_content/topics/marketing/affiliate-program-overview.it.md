---
title: Panoramica del programma degli affiliati
---

La funzionalità del programma degli affiliati di Spwig ti permette di reclutare partner che promuovono i tuoi prodotti in cambio di commissioni. Questo canale di marketing estende il tuo raggio d'azione attraverso influencer, blogger, creatori di contenuti e ambasciatori di marca che condividono collegamenti di tracciamento unici con il loro pubblico. Quando qualcuno clicca su un collegamento di un affiliato e effettua un acquisto, l'affiliato guadagna una commissione e tu acquisisci un cliente.

Questa panoramica spiega cos'è il programma degli affiliati, a chi è rivolto e come i commercianti lo utilizzano per costruire una rete di partner che genera vendite.

![Pannello di controllo del commerciante](/static/core/admin/img/help/affiliate-program-overview/merchant-dashboard.webp)

## Concetti chiave

Comprendere questi termini fondamentali ti aiuterà a configurare e gestire il tuo programma degli affiliati:

| Termine | Definizione |
|---------|------------|
| **Affiliato** | Un partner che promuove i tuoi prodotti e guadagna commissioni sulle vendite riferite |
| **Programma** | Una struttura delle commissioni con tassi, regole e impostazioni (puoi creare più programmi) |
| **Collegamento di tracciamento** | Un URL unico che contiene il codice dell'affiliato (es. `yourstore.com/?ref=CODE`) |
| **Commissione** | Il pagamento che un affiliato riceve per una vendita riferita, calcolato in base alle regole del programma |
| **Durata del cookie** | Quanto tempo (in giorni) il cookie di tracciamento persiste dopo che un cliente clicca su un collegamento affiliato |
| **Pagamento** | Un pagamento di massa che regola diverse commissioni approvate contemporaneamente |
| **Pannello del commerciante** | La tua interfaccia amministrativa per gestire programmi, affiliati, commissioni e pagamenti |
| **Portale degli affiliati** | Il pannello pubblico dove gli affiliati visualizzano i guadagni, ottengono i collegamenti di tracciamento e richiedono i pagamenti |

## Funzionamento

Il flusso di lavoro degli affiliati segue quattro fasi principali:

### 1. Applica
Gli affiliati scoprono il tuo programma e inviano domande attraverso il portale degli affiliati pubblico a `/affiliate/` nel tuo negozio. Puoi abilitare l'**approvazione automatica** per i programmi aperti o la **revisione manuale** per le partnership a invito.

### 2. Approva
Esamina le domande in sospeso in **Marketing > Affiliati**. Verifica il sito web, la presenza su social media e la corrispondenza con l'audience di ogni candidato prima di approvare. Una volta approvato, l'affiliato riceve le credenziali di accesso e può accedere al proprio pannello.

### 3. Promuovi
Gli affiliati approvati ricevono collegamenti di riferimento unici dal loro portale. Condividono questi collegamenti in articoli di blog, social media, newsletter email o dove si connettono con il loro pubblico. Spwig imposta un cookie di tracciamento quando qualcuno clicca sul collegamento.

### 4. Guadagna
Quando un cliente riferito completa un acquisto entro la durata del cookie, Spwig crea un record di commissione. Esamina e approva le commissioni in **Marketing > Commissioni**, quindi elabora i pagamenti quando gli affiliati raggiungono il limite minimo di pagamento.

## Panoramica del flusso di lavoro del commerciante

Come commerciante, gestisci l'intero ciclo di vita del programma dal tuo pannello amministrativo:

### Creare Programmi
Inizia creando uno o più programmi degli affiliati in **Marketing > Programmi degli Affiliati**. Ogni programma ha la propria struttura delle commissioni, durata del cookie e impostazioni di approvazione. Potresti creare programmi separati per influencer (commissioni più elevate) rispetto ai partner generali (commissioni più basse).

### Verifica le domande
Le nuove domande degli affiliati appaiono in **Marketing > Affiliati** con lo stato **In attesa**. Verifica ogni domanda per verificare che il partner sia adatto alla tua marca. Approva per attivare il loro account o rifiuta con una ragione.

### Approva le commissioni
Quando gli affiliati generano vendite, le commissioni appaiono in **Marketing > Commissioni** con lo stato **In attesa**. Verifica l'ordine collegato per verificare che sia legittimo (non un'autoriferral, non un ordine restituito), quindi approva o rifiuta di conseguenza.

### Elabora i pagamenti
Una volta che gli affiliati accumulano commissioni approvate superiori al limite minimo di pagamento, elabora i pagamenti di massa in **Marketing > Pagamenti**. Spwig si integra con PayPal e Airwallex per i pagamenti automatici, o puoi registrare trasferimenti bancari manuali.

## Panoramica del flusso di lavoro degli affiliati

Comprendere come gli affiliati vivono il tuo programma ti aiuta a progettare un'adeguata onboarding e supporto:

### Applica
Gli affiliati visitano il tuo portale degli affiliati, leggono i dettagli del programma (tasso di commissione, durata del cookie, termini di pagamento) e inviano un'application con le loro informazioni di contatto e canali promozionali.

### Crea collegamenti
Dopo l'approvazione, gli affiliati accedono al loro pannello per generare collegamenti di tracciamento. Possono creare collegamenti generici al negozio o collegamenti a prodotti specifici/categorie che desiderano promuovere.

### Promuovi
Gli affiliati condividono i loro collegamenti di tracciamento ovunque si connettano con potenziali clienti — articoli di blog, video su YouTube, storie su Instagram, newsletter email o siti di confronto.

### Richiedi pagamenti
Gli affiliati monitorano i loro guadagni in tempo reale attraverso il pannello del portale degli affiliati. Quando il loro saldo approvato raggiunge il limite minimo di pagamento, possono richiedere un pagamento.

## Dove trovare ciascuna funzionalità

| Funzionalità | Posizione amministrativa | Descrizione |
|-------------|-------------------------|-------------|
| **Programmi** | Marketing > Programmi degli Affiliati | Crea e configura le strutture delle commissioni |
| **Affiliati** | Marketing > Affiliati | Verifica le domande, gestisci gli account degli affiliati |
| **Commissioni** | Marketing > Commissioni | Verifica e approva le commissioni in sospeso |
| **Pagamenti** | Marketing > Pagamenti | Elabora pagamenti di massa agli affiliati |
| **Impostazioni** | Marketing > Impostazioni degli Affiliati | Impostazioni globali, fornitori di pagamento, personalizzazione del portale |
| **Pannello** | Marketing > Pannello degli Affiliati | Panoramica analitica con clic, ordini e totali delle commissioni |

Il portale rivolto agli affiliati è automaticamente disponibile a `/affiliate/` sull'URL pubblico del tuo negozio.

## Caso d'uso comune

Ecco quattro modi provati per utilizzare il programma degli affiliati di Spwig per crescere il tuo business:

### Partnership con influencer
Collabora con influencer del social media che hanno un pubblico coinvolgente nel tuo settore. Offri tassi di commissione più elevati (15–20%) per attrarre influencer di qualità che possono generare traffico significativo. Utilizza i collegamenti di tracciamento per misurare il ROI per ogni partnership.

### Ambasciatori di marca
Costruisci una rete di clienti fedeli che diventano ambasciatori del brand. Offri a questi clienti ripetuti account degli affiliati in modo che possano guadagnare commissioni quando riferiscono amici e familiari. Questo funziona particolarmente bene per prodotti nicchia con comunità appassionate.

### Creatori di contenuti
Ricruita blogger, YouTuber e podcaster che creano guide all'acquisto, recensioni o contenuti di confronto. Gli affiliati con contenuti evergreen possono generare riferimenti costanti mese dopo mese.

### Reti di riferimento
Consenti ai clienti esistenti di unirsi al tuo programma e guadagnare commissioni condividendo prodotti che amano. Questo crea un loop virale dove i clienti soddisfatti diventano promotori, portando nuovi clienti che potrebbero diventare anche affiliati.

## Consigli

- **Inizia con un programma** — Crea un programma generale per partner con un tasso di commissione del 10% e una durata del cookie di 30 giorni. Puoi aggiungere programmi specializzati in seguito una volta che hai capito quali partner funzionano meglio.
- **Stabilisci aspettative chiare** — Documenta il tuo processo di approvazione, i tempi di pagamento delle commissioni e la programmazione dei pagamenti nel portale degli affiliati. La trasparenza costruisce fiducia e riduce le richieste di supporto.
- **Monitora per frodi** — Controlla attentamente le commissioni per segnali di allarme come autoriferral (affiliati che acquistano da loro stessi collegamenti), tassi di resi insolitamente elevati o pattern di clic sospetti. Rifiuta immediatamente le commissioni fraudolente.
- **Comunica regolarmente** — Invia aggiornamenti mensili ai tuoi affiliati con notizie sul programma, riepiloghi del calendario promozionale e riconoscimenti ai top performer. La comunicazione attiva mantiene gli affiliati impegnati e promotori.
- **Ottimizza per mobile** — La maggior parte degli affiliati condivide collegamenti su social media dove la maggior parte dei clic proviene da dispositivi mobili. Testa il flusso di checkout sui telefoni per garantire un'esperienza fluida per i clienti riferiti.
- **Fornisci asset creativi** — Facilita la promozione dei tuoi prodotti da parte degli affiliati fornendo immagini banner, foto dei prodotti e copia pre-redatta che possono utilizzare nel loro contenuto.