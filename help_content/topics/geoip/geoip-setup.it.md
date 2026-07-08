---
title: Configurazione GeoIP
---

GeoIP consente al tuo negozio di rilevare automaticamente da dove proviene ogni visitatore in base all'indirizzo IP. Questo abilita funzionalità basate sulla posizione in tutto il tuo negozio - dal visualizzare la valuta corretta di default, all'applicazione di regole aziendali geografiche, al visualizzare analisi a livello di paese.

Il tuo negozio è pre-configurato con il servizio GeoIP di Spwig, quindi la rilevazione geografica funziona subito. Puoi anche collegare fornitori aggiuntivi per una maggiore accuratezza, utilizzare un database che scarichi tu stesso, o affidarti agli header da un CDN per lookup senza latenza.

## Funzionamento dei fornitori

Naviga verso **Clienti > Fornitori GeoIP** per visualizzare i fornitori configurati per il tuo negozio. Ogni fornitore gestisce le lookup IP-to-location utilizzando un metodo diverso. Quando un visitatore arriva, il tuo negozio interroga i fornitori attivi nell'ordine di priorità e utilizza il primo risultato riuscito.

Possono essere attivi più fornitori contemporaneamente - vengono provati prima quelli con numero di priorità più basso. Se il fornitore con la priorità più alta fallisce o non restituisce dati, il successivo viene provato automaticamente.

### Tipi di fornitori disponibili

| Fornitore | Descrizione |
|----------|-------------|
| **Spwig GeoIP** | Lookup basato sul cloud predefinito tramite il servizio di Spwig. Non richiede alcuna configurazione. |
| **MaxMind GeoLite2** | Database offline da MaxMind. Alta accuratezza. Richiede una chiave di licenza gratuita. |
| **DB-IP Lite** | Database offline da DB-IP. Scarica dal loro sito web. |
| **IP2Location LITE** | Database offline da IP2Location. Richiede un'iscrizione gratuita. |
| **CDN Edge Headers** | Legge gli header di posizione inseriti dal tuo CDN (es. Cloudflare). Zero latenza. |
| **Browser Hints** | Utilizza il fuso orario/lingua fornito dal browser come segnale di posizione morbido. |
| **Fornitore Personalizzato** | Un componente fornitore installato dal mercato dei componenti Spwig. |

## Aggiungere un fornitore

### Utilizzando il servizio Spwig GeoIP (predefinito)

Il fornitore Spwig GeoIP viene aggiunto automaticamente su nuove installazioni. Verifica che appaia nell'elenco e che **Attivo** sia selezionato. Non è richiesta alcuna configurazione aggiuntiva.

### Aggiungere un database MaxMind GeoLite2

MaxMind offre un database gratuito offline che fornisce risultati accurati senza inviare lookup a un servizio esterno.

1. Registrati per un account gratuito su maxmind.com e genera una chiave di licenza
2. Naviga verso **Clienti > Fornitori GeoIP** e fai clic su **+ Aggiungi Fornitore GeoIP**
3. Compila il modulo:
   - **Nome**: `MaxMind GeoLite2` (o qualsiasi nome descrittivo)
   - **Tipo Fornitore**: MaxMind GeoLite2
   - **Attivo**: selezionato
   - **Priorità**: `1` (inferiore rispetto al predefinito di Spwig per provarlo per primo, o superiore per utilizzarlo come backup)
   - **Chiave di Licenza**: incolla la tua chiave di licenza MaxMind
   - **URL del Database**: l'URL di download dal tuo pannello di controllo account MaxMind
4. Fai clic su **Salva**

Dopo aver salvato, seleziona il fornitore nell'elenco e utilizza l'azione **Aggiorna database del fornitore selezionato** per verificare che l'URL del database sia raggiungibile.

### Aggiungere header edge CDN

Se il tuo negozio si trova dietro un CDN che inserisce header di geolocalizzazione (ad esempio, `CF-IPCountry` di Cloudflare), puoi utilizzare questi header per una rilevazione immediata del paese senza latenza.

1. Naviga verso **Clienti > Fornitori GeoIP** e fai clic su **+ Aggiungi Fornitore GeoIP**
2. Imposta **Tipo Fornitore** su **CDN Edge Headers**
3. Imposta **Priorità** su `0` (massima priorità, poiché gli header sono la fonte più veloce)
4. Nel campo **Config**, specifica quale header il tuo CDN utilizza:
   ```json
   {
     "header_name": "CF-IPCountry"
   }
   ```
5. Fai clic su **Salva**

## Testare un fornitore

Dopo aver aggiunto un fornitore, puoi verificare che funzioni correttamente:

1. Nell'elenco Fornitori GeoIP, seleziona il fornitore utilizzando la sua casella di controllo
2. Apri il menu a discesa **Azione** e scegli **Testa fornitori selezionati**
3. Fai clic su **Vai**

Spwig invierà un lookup di test per un indirizzo IP noto (il DNS pubblico di Google, `8.8.8.8`) e ti mostrerà il risultato. Un test riuscito visualizza il paese restituito e il tempo di risposta in millisecondi.

## Impostare la priorità del fornitore

Quando sono attivi più provider, il campo **Priorità** determina quale viene provato per primo.

Numeri inferiori indicano una priorità più alta.

Ad esempio, per utilizzare prima gli header del CDN (più veloci) e passare al GeoIP di Spwig in caso di fallimento:

| Provider | Priorità |
|----------|----------|
| CDN Edge Headers | 0 |
| Spwig GeoIP | 10 |

Puoi modificare direttamente la priorità nella vista elenco — la colonna **Priorità** è modificabile in linea.

## Monitoraggio delle prestazioni del provider

Ogni record del provider traccia le proprie statistiche di accuratezza:

- **Total Lookups** — numero totale di lookup IP tentati
- **Successful Lookups** — lookup che hanno restituito un risultato
- **Failed Lookups** — lookup che hanno restituito nessun dato o un errore
- **Average Response (ms)** — tempo medio di risposta in millisecondi
- **Accuracy** — percentuale di lookup riusciti

Se un provider mostra un tasso di accuratezza basso o tempi di risposta elevati, considera di modificare la sua priorità o di disattivarlo a favore di un'opzione con prestazioni migliori.

## Mappatura dei paesi

Vai a **Customers > Country Mappings** per configurare le impostazioni predefinite per paese relative alla valuta, alla lingua, all'imposta e alla spedizione. Ogni voce del paese controlla:

- **Default Currency** — valuta preselezionata per i visitatori provenienti da quel paese
- **Default Language** — lingua mostrata ai visitatori provenienti da quel paese
- **Tax Rate** — percentuale predefinita dell'imposta applicata per quel paese
- **Is EU Member** / **Requires VAT** — utilizzato per la logica di conformità fiscale UE
- **Shipping Zone** — collega il paese a una zona di spedizione
- **Supports COD** — abilita il pagamento in contanti per quel paese

Puoi modificare i campi **Is Active**, **Default Currency** e **Default Language** direttamente nell'elenco senza aprire ogni record.

## Consigli

- Il provider Spwig GeoIP funziona immediatamente senza configurazione — aggiungi solo provider aggiuntivi se hai bisogno di un'accuratezza maggiore o di un'operazione offline
- Se utilizzi Cloudflare, il provider CDN Edge Headers è la scelta migliore: non aggiunge latenza e non consuma quote API
- Mantieni attivi solo i provider di cui hai realmente bisogno — avere molti provider attivi non migliora l'accuratezza se il primo già riesce
- Controlla le statistiche di accuratezza settimanalmente e disattiva eventuali provider con un tasso di successo inferiore all'80%
- Le mappature dei paesi vengono utilizzate come impostazioni predefinite; i clienti possono sempre modificare manualmente la valuta e la lingua nel negozio online