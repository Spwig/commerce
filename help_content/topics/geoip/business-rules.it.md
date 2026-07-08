---
title: Regole basate sulla posizione
---

Le regole basate sulla posizione ti permettono di eseguire automaticamente azioni quando un visitatore arriva da un paese, una regione o un tipo di dispositivo specifico. Puoi utilizzare le regole per impostare una valuta per i clienti di una regione specifica, ridirigere i visitatori a una pagina localizzata, mostrare un banner promozionale o limitare l'accesso a determinati contenuti.

Le regole vengono valutate nell'ordine di priorità ogni volta che viene stabilita una sessione di visita. Quando una regola corrisponde, le azioni configurate vengono eseguite immediatamente.

## Come funzionano le regole aziendali

Ogni regola è composta da due parti:

- **Condizioni** — i criteri che devono essere soddisfatti affinché la regola venga attivata (es. "il visitatore è della Germania")
- **Azioni** — ciò che accade quando tutte le condizioni corrispondono (es. "imposta la valuta su EUR")

Le condizioni e le azioni vengono salvate come oggetti JSON nel modulo della regola. Spwig valuta tutte le regole attive nell'ordine di priorità (a partire dal numero più basso) e applica quelle che corrispondono.

## Navigare verso le regole aziendali

Naviga verso **Customers > Business Rules** per visualizzare tutte le tue regole configurate. L'elenco mostra il nome di ogni regola, lo stato, la priorità, quante volte è stata attivata e quando è stata attivata per l'ultima volta.

Fai clic su qualsiasi regola per visualizzarla o modificarla, o fai clic su **+ Add Business Rule** per crearne una nuova.

## Creare una regola aziendale

### Passo 1: informazioni di base

Compila i dettagli di identificazione della regola:

- **Name** — un nome chiaro e descrittivo (es. `Set EUR for Eurozone`)
- **Description** — note opzionali che spiegano lo scopo della regola
- **Is Active** — seleziona questa opzione per abilitare la regola; deseleziona per sospendere la regola senza eliminarla
- **Priority** — i numeri più bassi vengono eseguiti per primi; utilizza `10`, `20`, `30` per lasciare spazio a regole future

### Passo 2: definire le condizioni

Nel campo **Conditions**, inserisci un oggetto JSON che descrive quando la regola deve essere attivata. Tutte le condizioni nell'oggetto devono essere vere affinché la regola corrisponda.

#### Chiavi di condizione disponibili

| Condizione | Formato | Esempio |
|-----------|--------|---------|
| `country_in` | Array di codici paese ISO | `["DE", "FR", "IT"]` |
| `country_not_in` | Array di codici paese ISO | `["US", "CA"]` |
| `region_in` | Array di nomi di regioni | `["Bavaria", "Catalonia"]` |
| `region_not_in` | Array di nomi di regioni | `["Quebec"]` |
| `is_mobile` | Booleano | `true` |
| `is_vpn` | Booleano | `false` |

#### Esempi di condizioni

Visitatori da Germania, Francia o Italia:
```json
{
  "country_in": ["DE", "FR", "IT"]
}
```

Visitatori da Stati Uniti che utilizzano un dispositivo mobile:
```json
{
  "country_in": ["US"],
  "is_mobile": true
}
```

Visitatori fuori dall'Unione Europea:
```json
{
  "country_not_in": ["AT","BE","BG","CY","CZ","DE","DK","EE","ES","FI","FR","GR","HR","HU","IE","IT","LT","LU","LV","MT","NL","PL","PT","RO","SE","SI","SK"]
}
```

### Passo 3: definire le azioni

Nel campo **Actions**, inserisci un oggetto JSON che descrive cosa deve accadere quando la regola viene attivata.

#### Chiavi di azione disponibili

| Azione | Formato | Descrizione |
|--------|--------|-------------|
| `set_currency` | Stringa del codice valuta | Imposta una valuta preselezionata per il visitatore |
| `set_language` | Stringa del codice lingua | Imposta la lingua di visualizzazione |
| `show_banner` | Booleano | Attiva un banner promozionale |
| `redirect_to` | Stringa del percorso URL | Ridirige il visitatore a un URL diverso |

#### Esempi di azioni

Imposta la valuta su Euro:
```json
{
  "set_currency": "EUR"
}
```

Ridirige a una pagina di atterraggio localizzata:
```json
{
  "redirect_to": "/de/"
}
```

Imposta sia la valuta che la lingua:
```json
{
  "set_currency": "GBP",
  "set_language": "en"
}
```

## Esempi pratici

### Esempio: regola di valuta per l'area dell'euro

**Scenario:** Mostra automaticamente i prezzi in euro ai visitatori provenienti da paesi dell'area dell'euro.

| Campo | Valore |
|-------|-------|
| Name | `Eurozone — Set EUR` |
| Priority | `10` |
| Is Active | Checked |
| Conditions | `{"country_in": ["AT","BE","DE","ES","FI","FR","GR","IE","IT","LU","NL","PT"]}` |
| Actions | `{"set_currency": "EUR"}` |

### Esempio: regola di prezzo per il Regno Unito

**Scenario:** Mostra i prezzi in GBP ai visitatori provenienti dal Regno Unito.

| Campo | Valore |
|-------|-------|
| Nome | `UK — Set GBP` |
| Priorità | `20` |
| Attivo | Contrassegnato |
| Condizioni | `"{\"country_in\": [\"GB\"]}"` |
| Azioni | `"{\"set_currency\": \"GBP\"}"` |

### Esempio: reindirizzare a una sezione del negozio localizzato

**Scenario:** Inviare i visitatori dall'Australia a una pagina dedicata australiana.

| Campo | Valore |
|-------|-------|
| Nome | `Australia — Redirect` |
| Priorità | `30` |
| Attivo | Contrassegnato |
| Condizioni | `"{\"country_in\": [\"AU\"]}"` |
| Azioni | `"{\"redirect_to\": \/au\/}"` |

## Test delle regole

Puoi verificare che una regola corrisponda al profilo del visitatore previsto senza dover aspettare il traffico reale:

1. Nella lista delle regole di Business Rules, seleziona la regola utilizzando la casella di controllo
2. Apri il menu a discesa **Azioni** e seleziona **Testa le regole selezionate**
3. Clicca su **Vai**

Spwig valuterà la regola rispetto a un profilo di visitatore basato negli Stati Uniti e riferirà se è corrisposta e quali azioni sarebbero state attivate.

## Monitoraggio dell'attività delle regole

La colonna **Triggered** nella lista delle regole mostra quante volte ogni regola è stata attivata. Clicca su una regola per visualizzare l'orario **Last Triggered** nella sezione Statistiche.

Utilizza l'azione **Reset statistics** per azzerare i conteggi delle attivazioni se desideri iniziare a misurare da una data specifica dopo aver apportato modifiche a una regola.

## Consigli

- Imposta le priorità con spazi (10, 20, 30) invece di numeri sequenziali (1, 2, 3) in modo da poter inserire nuove regole in seguito senza dover riassegnare tutti i numeri
- Le regole vengono attivate nell'ordine di priorità e vengono applicate tutte le regole corrispondenti — se due regole impostano entrambe la valuta, l'azione della regola con priorità inferiore (numero più alto) verrà applicata per ultima
- Utilizza l'interruttore **Is Active** per sospendere temporaneamente una regola durante le promozioni senza eliminare la configurazione
- Testa sempre una nuova regola prima di attivarla in un ambiente live per assicurarti che le condizioni siano corrette
- La rilevazione del VPN (`"is_vpn": true`) è disponibile se desideri applicare un trattamento diverso ai visitatori che nascondono la loro posizione, ma tieni presente che alcuni clienti legittimi utilizzano i VPN per la privacy