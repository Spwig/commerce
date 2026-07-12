---
title: Servizi ospitati di Spwig
---

Spwig include tre servizi cloud opzionali che il tuo negozio può utilizzare senza doverli configurare o ospitare da solo: **GeoIP** rileva dove si trovano i tuoi visitatori, **Geocoder** converte gli indirizzi dei clienti in coordinate mappa, e **Push** invia notifiche istantanee all'app mobile di amministrazione di Spwig. Nell'edizione Community (gratuita), ogni servizio include un limite mensile generoso. Quando qualsiasi servizio si avvicina al limite, Spwig ti avvisa nell'amministrazione in modo che tu possa decidere se effettuare l'aggiornamento prima che i tuoi clienti ne notino qualcosa.

## I tre servizi ospitati

### GeoIP — rilevamento del paese del visitatore

GeoIP cerca il paese di ogni visitatore in base al loro indirizzo IP. Il tuo negozio utilizza questa informazione per visualizzare automaticamente la valuta corretta quando un cliente arriva, e per compilare in anticipo il campo del paese durante il checkout. Ad esempio, un visitatore tedesco vedrà i prezzi in euro, e un visitatore giapponese vedrà i prezzi in yen — senza doverli selezionare manualmente.

Ogni caricamento di pagina in cui GeoIP esegue una ricerca conta sul tuo limite mensile. Le visite ripetute dallo stesso sessione del browser non consumano ciascuna una ricerca; il risultato è memorizzato per la sessione. Le ricerche di GeoIP avvengono solo sul negozio, non nel pannello di amministrazione.

### Geocoder — indirizzo a coordinate

Geocoder converte gli indirizzi digitati dai clienti in coordinate geografiche (latitudine e longitudine). Il tuo negozio utilizza queste coordinate per due scopi: calcolare i costi di spedizione basati sulla distanza quando hai punti di ritiro o regole di spedizione basate su raggio, e alimentare le suggerimenti di completamento automatico dell'indirizzo sulla pagina di checkout in modo che i clienti possano trovare rapidamente il loro indirizzo.

Una ricerca del geocoder viene attivata quando un cliente seleziona o conferma un indirizzo durante il checkout. Come GeoIP, i risultati vengono memorizzati in modo che lo stesso indirizzo venga cercato una volta per sessione.

### Push — notifiche nell'app di amministrazione

Push invia notifiche in tempo reale all'app mobile del commerciante di Spwig. Quando arriva un nuovo ordine, quando lo stock scende al di sotto di un limite, o quando un cliente invia un messaggio, Push invia una notifica istantanea al tuo dispositivo in modo che tu possa rispondere senza dover tenere aperto il pannello di amministrazione.

Ogni notifica inviata al tuo dispositivo conta come una richiesta di push contro il tuo limite mensile.

## La versione gratuita Community

Nell'edizione Community di Spwig, ogni servizio è incluso a costo zero fino a un limite mensile di richieste. I limiti esatti sono stabiliti da Spwig e possono variare; il tuo pannello di amministrazione mostra sempre le figure correnti per il tuo installazione. I piani a pagamento (Starter, Growth, Pro, Pro Plus) e le installazioni self-hosted con una licenza a pagamento hanno limiti più elevati per ogni servizio.

Quando un servizio raggiunge il 100% del limite della versione Community, le richieste a quel servizio si interrompono fino a quando il contatore non viene reimpostato nel mese successivo. L'impatto sul tuo negozio dipende da quale servizio è interessato:

| Servizio | Cosa accade al 100% |
|---------|----------------------|
| GeoIP | La rilevazione automatica della valuta torna alla valuta predefinita del tuo negozio. I clienti possono comunque cambiare manualmente la valuta. |
| Geocoder | Il completamento automatico dell'indirizzo smette di offrire suggerimenti. I clienti possono comunque digitare manualmente l'indirizzo. Il calcolo del costo di spedizione continua a utilizzare le ultime coordinate note. |
| Push | Le nuove notifiche dell'app di amministrazione vengono inserite in coda ma non vengono consegnate fino al mese successivo o all'aggiornamento. |

Il tuo negozio continua a funzionare normalmente in tutti i casi — non vengono persi ordini e i clienti possono comunque effettuare il checkout. Gli effetti sono limitati a funzionalità di comodità.

## Leggere il tile del dashboard

Il tile **Utilizzo dei servizi di Spwig** appare sulla pagina principale del dashboard di amministrazione. Mostra una barra di avanzamento per ciascuno dei tre servizi.

Ogni riga nel tile segue lo stesso layout:

- **Nome del servizio** (a sinistra) — GeoIP, Ricerca indirizzo (Geocoder), o Notifiche push.
- **Barra di avanzamento** (al centro) — si riempie da sinistra a destra man mano che l'utilizzo aumenta.

Il colore della barra cambia man mano che si avvicinano ai limiti:
  - **Verde** — l'utilizzo è inferiore all'80%.

Tutto funziona normalmente.
  - **Amber** — l'utilizzo è compreso tra l'80% e il 99%.

Il servizio è ancora attivo ma si sta avvicinando al limite.
  - **Red** — l'utilizzo ha raggiunto il 100%.

Il servizio è ora limitato per questo mese.
- **Conteggio dell'utilizzo** (a destra) — il numero esatto di richieste utilizzate rispetto al totale consentito, ad esempio `3.241 / 10.000`.

L'etichetta tra parentesi indica la finestra temporale, di solito `(questo mese)`.

Se il tile non riesce a raggiungere il server di aggiornamento Spwig per recuperare l'utilizzo corrente (ad esempio, se il tuo server non ha accesso in uscita a Internet), la colonna dei contatori mostra un trattino (`—`) per quel servizio. Questo non significa che il servizio sia rotto; significa che la visualizzazione dell'utilizzo è temporaneamente non disponibile.

### Il pulsante **Upgrade**

Quando qualsiasi servizio raggiunge l'80% o più, compare un pulsante **Upgrade** nell'angolo in alto a destra del tile. Cliccandolo si apre la pagina di aggiornamento Spwig dove puoi confrontare i piani e aumentare i limiti del tuo servizio. Il pulsante scompare una volta che l'utilizzo torna sotto l'80% all'inizio del mese successivo.

## La barra di avviso per la quota

Oltre al tile del dashboard, una barra compare in alto in ogni pagina di amministrazione ogni volta che qualsiasi servizio supera la soglia del 80%. La barra compare solo nelle installazioni Community.

**Barra Amber — vicino al limite (80–99%)**

> **Stai per raggiungere il limite dei servizi ospitati:** Uno dei tuoi servizi Spwig è sopra l'80% della quota del piano Community. Aggiorna per aumentare il limite prima che venga raggiunto.

Questa barra è un avviso anticipato. I tuoi servizi continuano a funzionare e hai tempo per decidere se aggiornare prima che il mese finisca.

**Barra Rosso — limite raggiunto (100%)**

> **Limite dei servizi Spwig raggiunto:** Uno dei tuoi servizi ospitati ha raggiunto la quota del piano Community. Aggiorna per mantenerli in funzione senza interruzioni.

Questa barra compare quando almeno un servizio ha raggiunto il 100% e ora è limitato. Cliccando su **Upgrade** su entrambe le barre si apre la stessa pagina di aggiornamento del pulsante del tile.

La barra scompare automaticamente all'inizio del mese successivo quando i contatori vengono resettati, o immediatamente dopo che hai aggiornato a un piano a pagamento.

## Avviso email al 90%

Quando qualsiasi servizio supera il 90% della sua quota, Spwig invia anche un avviso email una volta all'indirizzo configurato nelle impostazioni del tuo negozio (**Impostazioni > Impostazioni del negozio > Contatti > Email amministratore**). L'email viene inviata al massimo una volta per servizio per mese, quindi non sarai inondato di messaggi. Non viene inviata un'email al 100% perché in quel momento la barra all'interno dell'amministrazione già rende chiaro la situazione.

Se non ricevi l'email, controlla che l'indirizzo email dell'amministratore sia impostato correttamente sotto **Impostazioni > Impostazioni del negozio**.

## Aggiornamento del piano

Quando aggiorni da Community a qualsiasi piano a pagamento, i limiti più elevati entrano in vigore immediatamente — non è necessario riavviare il negozio o modificare le configurazioni. Il tile del dashboard mostrerà il nuovo, più alto limite la prossima volta che si aggiorna (entro cinque minuti).

Per aggiornare, clicca sul pulsante **Upgrade** sul tile del dashboard o sulla barra della quota, o visita direttamente la pagina di aggiornamento Spwig. I piani a pagamento includono gli stessi tre servizi ospitati (GeoIP, Geocoder, Push) con limiti mensili aumentati, più l'accesso alla consegna email ospitata da Spwig e al supporto prioritario.

## Self-hosting e licenze Pro

Se esegui un'installazione self-hosted di Spwig con una licenza a pagamento, il livello della tua licenza determina i limiti dei servizi, esattamente come il piano ospitato equivalente. Il tuo negozio ha comunque bisogno di un accesso in uscita a Internet per raggiungere `updates.spwig.com` in modo che la piattaforma possa recuperare e verificare la configurazione del tuo livello. I contatori dell'utilizzo visualizzati nel tile del dashboard vengono recuperati dagli endpoint dei servizi ospitati a `geoip.spwig.com`, `geocoder.spwig.com` e `push.spwig.com`.

Non esiste attualmente un'opzione per sostituire GeoIP, Geocoder o Push con alternative self-hosted — questi servizi vengono forniti esclusivamente dall'infrastruttura di Spwig e sono inclusi in tutte le edizioni.

## Consigli

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- **Controlla regolarmente il tile alla fine dei mesi occupati** — un evento di vendita o una promozione può aumentare significativamente le richieste di GeoIP e Geocoder.

Il tile ti dà un avviso in anticipo, prima che i clienti ne siano influenzati.
- **Il fallback della valuta è invisibile per la maggior parte dei clienti** — se GeoIP raggiunge il limite, i clienti vedranno la valuta predefinita del tuo negozio.

Questo è raramente un problema serio per i negozi che servono principalmente un mercato; è più rilevante per i negozi veramente internazionali.
- **L'autocompletamento dell'indirizzo è un'agevolezza, non un blocco** — quando Geocoder è limitato, i clienti possono comunque digitare e inviare il loro indirizzo normalmente.

Se conduci frequenti promozioni che generano un alto traffico al checkout, considera l'aggiornamento prima dei periodi occupati.
- **Il limitatore di push non perde permanentemente le notifiche** — le notifiche in coda dal periodo limitato non vengono consegnate retroattivamente quando il mese si reimposta o dopo un aggiornamento.

Se ti affidi pesantemente al push per allerte ordinate urgenti, aggiornare prima che venga raggiunto il limite ti assicura di non perdere nulla.
- **La cache di 5 minuti significa che il tile non è perfettamente in tempo reale** — le figure di utilizzo vengono aggiornate approssimativamente ogni cinque minuti in background.

Durante periodi di traffico insolitamente elevato, l'utilizzo effettivo potrebbe essere leggermente superiore rispetto a quanto mostra il tile.
- **Imposta l'indirizzo email dell'amministratore** — l'email del 90% di avviso funziona solo se **Settings > Store Settings > Admin Email** è compilato.

È utile verificare che sia impostato correttamente in modo da ricevere l'avviso prima che si verifichino problemi.