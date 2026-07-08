---
title: Configurazione CDN
---

Una rete di distribuzione del contenuto (CDN) memorizza copie delle immagini, degli stylesheet e degli script del tuo negozio su server in tutto il mondo. Quando un cliente visita il tuo negozio, questi file vengono serviti dal server più vicino a lui, invece che dal tuo server principale di hosting. Questo riduce i tempi di caricamento delle pagine, soprattutto per i clienti che si trovano lontano dal luogo in cui è ospitato il tuo negozio.

Spwig ottimizza già la consegna degli asset statici di default con la precompressione Brotli e gzip, il caching degli asset con fingerprint e intestazioni immutabili di 1 anno, e una corretta negoziazione del contenuto. L'aggiunta di un CDN è facoltativa, ma può migliorare ulteriormente la velocità per i negozi con una base di clienti internazionale.

## Il Tuo Negozio Ha Bisogno di un CDN?

Non tutti i negozi traggono lo stesso beneficio da un CDN. Usa queste linee guida per decidere:

**Un CDN è consigliato se**:
- I tuoi clienti si trovano in diversi paesi o continenti
- Il tuo negozio presenta molte immagini di prodotti o pagine pesanti da un punto di vista multimediale
- Vuoi i tempi di caricamento delle pagine più veloci possibili in tutto il mondo
- Vendetti in regioni lontane dal tuo server di hosting (es. server in Europa, clienti in Asia)

**Un CDN è probabilmente inutile se**:
- I tuoi clienti sono principalmente locali o nello stesso paese del tuo server
- Il tuo negozio ha un catalogo piccolo con poche immagini
- Il tuo fornitore di hosting include già un CDN integrato

Quando non sei sicuro, un CDN non danneggia le prestazioni. Servizi come Cloudflare offrono livelli gratuiti, quindi non c'è alcun costo per provarli.

## Come Spwig Funziona con i CDN

Spwig è pronto per il CDN di default. Non è necessario modificare alcun codice o impostazioni all'interno del pannello di amministrazione di Spwig. Ecco ciò che Spwig fa già per te:

- **File statici con fingerprint** -- Ogni file CSS, JavaScript e immagine include un hash unico di versione nel nome del file. Questo significa che i CDN possono memorizzare in modo sicuro questi file per molto tempo senza servire contenuti obsoleti.
- **Intestazioni di cache a lunga durata** -- Gli asset statici vengono serviti con intestazioni di cache immutabili di 1 anno, indicando ai CDN e ai browser di memorizzarli in modo aggressivo.
- **File precompressi** -- Spwig precomprime gli asset utilizzando Brotli e gzip, in modo che il tuo CDN possa consegnare file più piccoli senza un ulteriore elaborazione.
- **Negoziazione del contenuto corretta** -- Spwig invia le intestazioni di tipo di contenuto e codifica corrette su cui i CDN si basano per un corretto caching.

Tutto ciò che devi fare è puntare i DNS del tuo dominio al provider CDN, e tutto funziona automaticamente.

## Configurazione di Cloudflare

Cloudflare è il CDN più popolare e offre un livello gratuito che funziona bene per la maggior parte dei negozi. Segui questi passaggi:

**Passo 1: Crea un Account Cloudflare**
- Visita cloudflare.com e iscriviti a un account gratuito

**Passo 2: Aggiungi il Tuo Dominio**
- Clicca su **Add a Site** e inserisci il nome del dominio del tuo negozio
- Seleziona il piano **Free** (sufficiente per la maggior parte dei negozi)

**Passo 3: Aggiorna i Nameserver DNS**
- Cloudflare ti mostrerà due nameserver (es. `anna.ns.cloudflare.com`)
- Accedi al tuo registrar del dominio (dove hai acquistato il tuo dominio)
- Sostituisci i tuoi nameserver correnti con i nameserver di Cloudflare
- I cambiamenti DNS possono richiedere fino a 24 ore per prendere effetto

**Passo 4: Configura SSL/TLS**
- Nel dashboard di Cloudflare, vai a **SSL/TLS**
- Imposta la modalità di crittografia su **Full (strict)**
- Questo assicura che tutto il traffico tra Cloudflare e il tuo server rimanga crittografato

**Passo 5: Verifica che Funzioni**
- Una volta che i DNS si propagano, visita il tuo negozio e controlla l'intestazione `cf-cache-status` nel tuo browser (vedi Verifica il Tuo CDN di seguito)

## Configurazione di AWS CloudFront

Se utilizzi già Amazon Web Services, CloudFront si integra naturalmente con la tua infrastruttura:

1. Apri il console **CloudFront** nel tuo account AWS
2. Crea una nuova **Distribuzione** con il dominio del tuo negozio come origine
3. Imposta la **Policy del Protocollo di Origine** su "HTTPS Only"
4. Nella **Cache Behavior**, imposta la **Cache Policy** su "CachingOptimized" per gli asset statici
5. Aggiungi il dominio del tuo negozio come **Alternate Domain Name (CNAME)**
6. Collega un certificato SSL da AWS Certificate Manager
7. Aggiorna i DNS del tuo dominio per puntare all'URL della distribuzione CloudFront

Il prezzo di CloudFront è basato sull'utilizzo.

Per la maggior parte dei negozi, i costi sono minimi poiché gli asset fingerprintati di Spwig vengono memorizzati in cache per periodi lunghi.

## Impostazioni CDN Consigliate

Per ottenere i migliori risultati, configura il tuo CDN per memorizzare in cache il contenuto giusto e saltare il resto.

**Cosa memorizzare in cache** (asset statici):
- `/static/` -- Tutti gli stili, gli script, le font e gli asset del tema
- `/media/` -- Immagini dei prodotti e file multimediali caricati
- File immagine (`.jpg`, `.png`, `.webp`, `.svg`, `.gif`)
- File font (`.woff`, `.woff2`)

**Cosa non memorizzare in cache** (pagine dinamiche):
- `/admin/` -- Il pannello di amministrazione deve sempre servire contenuti freschi
- `/cart/` -- Le pagine del carrello contengono dati specifici per la sessione
- `/checkout/` -- Le pagine di checkout non devono mai essere memorizzate in cache per motivi di sicurezza
- `/accounts/` -- Le pagine del profilo cliente contengono dati privati
- Qualsiasi pagina che richiede l'autenticazione o mostra contenuti personalizzati

**Regole generali per la memorizzazione in cache**:
- **Rispetta gli header di cache dell'origine** -- Spwig invia gli header cache-control corretti per ogni tipo di contenuto. Configura il tuo CDN per rispettare questi header invece di sovrascriverli.
- **Abilita la compressione Brotli** -- Sia Cloudflare che CloudFront supportano Brotli. Abilitalo per sfruttare gli asset pre-compressi di Spwig.
- **Imposta il TTL del browser su "Rispetta gli header esistenti"** -- Questo permette alle politiche di cache integrate di Spwig di determinare il comportamento.

## Verifica il Tuo CDN

Dopo l'installazione, conferma che il CDN stia servendo correttamente il tuo contenuto:

**Passo 1: Apri gli strumenti per sviluppatori del browser**
- In Chrome o Firefox, premi **F12** per aprire gli strumenti per sviluppatori
- Clicca sulla scheda **Network**

**Passo 2: Carica il tuo negozio**
- Visita la homepage del tuo negozio con gli strumenti per sviluppatori aperti
- Clicca su una richiesta di file statico (es. un file `.css` o `.js`)

**Passo 3: Controlla gli header della risposta**
- **Cloudflare**: Cerca l'header `cf-cache-status`. Un valore di `HIT` significa che il file è stato servito dalla cache del CDN. `MISS` significa che è stato recuperato dal tuo server (solo la prima richiesta).
- **CloudFront**: Cerca l'header `x-cache`. Un valore di `Hit from cloudfront` conferma la consegna tramite CDN.

**Passo 4: Testa da un'altra posizione**
- Usa uno strumento gratuito come gtmetrix.com o webpagetest.org per testare il tuo negozio da diverse posizioni geografiche
- Confronta i tempi di caricamento prima e dopo l'installazione del CDN

## Problemi Comuni

### Contenuto Obsoleto Dopo Cambi al Tema

**Problema**: Dopo aver aggiornato il tema o aver apportato modifiche al design, i clienti vedono ancora la versione vecchia.

**Soluzione**: Pulisci la cache del tuo CDN. In Cloudflare, vai a **Caching > Configuration > Purge Everything**. In CloudFront, crea un'**Invalidation** per `/*`. Nota che gli asset fingerprintati di Spwig di solito impediscono questo problema poiché i file aggiornati ricevono automaticamente nuovi nomi di file. Questo problema colpisce principalmente gli asset non fingerprintati come caricamenti personalizzati.

---

### Avvisi di Contenuto Misto

**Problema**: Il tuo browser mostra un avviso di sicurezza riguardo al "contenuto misto" dopo aver abilitato il CDN.

**Soluzione**: Assicurati che la modalità SSL del tuo CDN sia impostata su **Full (strict)**, non su "Flexible". La modalità Flexible può causare al tuo server di ricevere richieste HTTP invece di HTTPS, portando a avvisi di contenuto misto. In Cloudflare, controlla **SSL/TLS > Overview** e verifica la modalità.

---

### Pannello di Amministrazione Lento

**Problema**: Il pannello di amministrazione sembra più lento dopo aver aggiunto un CDN.

**Soluzione**: I CDN non dovrebbero memorizzare in cache le pagine di amministrazione. Crea una **Page Rule** (Cloudflare) o un **Cache Behavior** (CloudFront) che imponga la memorizzazione in cache su "Bypass" per qualsiasi URL che corrisponde a `/admin/*`. Questo assicura che le richieste di amministrazione vengano inviate direttamente al tuo server senza sovraccarico del CDN.

---

### Immagini che non si caricano

**Problema**: Le immagini dei prodotti o i file multimediali restituiscono errori dopo l'installazione del CDN.

**Soluzione**: Verifica che l'origine del tuo CDN sia configurata con il protocollo corretto (HTTPS) e la porta. Controlla anche che il firewall del tuo server permetta connessioni provenienti dagli indirizzi IP del CDN.

## Consigli

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- **Inizia con il livello gratuito di Cloudflare** -- Copre le esigenze della maggior parte dei negozi e richiede solo pochi minuti per essere configurato
- **Utilizza sempre la modalità SSL completa (strict)** -- La modalità flessibile crea vulnerabilità di sicurezza e può compromettere i flussi di checkout
- **Pulisci il cache del CDN dopo importanti aggiornamenti del tema** -- Sebbene i file con fingerprint di Spwig gestiscano la maggior parte dei casi, un'eliminazione completa del cache assicura che non rimanga alcun contenuto obsoleto
- **Non cacheare le pagine di checkout o del carrello** -- Il caching di queste pagine può esporre i dati di un cliente ad un altro
- **Testa dalle ubicazioni dei tuoi clienti** -- Utilizza strumenti gratuiti come webpagetest.org per misurare le prestazioni reali dalle regioni in cui i tuoi clienti effettuano gli acquisti
- **Monitora le analisi del tuo CDN** -- Sia Cloudflare che CloudFront forniscono dashboard che mostrano i tassi di cache hit, la banda risparmiata e il traffico per paese
- **Mantieni il TTL DNS basso durante la configurazione** -- Imposta il TTL DNS a 300 secondi (5 minuti) durante il passaggio a un CDN, quindi aumentalo una volta che tutto è stato confermato funzionante
- **Un CDN non sostituisce un buon hosting** -- Il tuo server originale è comunque importante per le pagine dinamiche come checkout, carrello e amministrazione.

Scegli un hosting di qualità insieme a un CDN