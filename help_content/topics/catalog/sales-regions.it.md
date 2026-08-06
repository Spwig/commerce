---
title: Regioni di vendita
---

Le regioni di vendita ti consentono di definire mercati geografici per il tuo negozio e di controllare quali prodotti sono disponibili in ciascuna regione. Questo è utile quando vendi in più paesi o territori e hai bisogno di cataloghi prodotti diversi, valute regionali o disponibilità del magazzino per ogni località.

## Cos'è una regione di vendita?

Una regione di vendita è un'area geografica denominata composta da uno o più paesi. Ogni regione ha una valuta predefinita, una priorità e può essere collegata a uno o più magazzini. Quando un cliente esplora il tuo negozio, Spwig determina la sua regione in base alla sua posizione e applica la valuta e le regole di visibilità del prodotto appropriate.

Casi d'uso comuni:
- Mostrare solo i prodotti disponibili localmente ai clienti di ogni paese
- Assegnare valute predefinite specifiche per regione (es. NZD per i clienti della Nuova Zelanda)
- Controllare quali magazzini effettuano gli ordini per ciascuna regione
- Nascondere i prodotti che non sono ancora disponibili in alcuni mercati

## Creazione di una regione di vendita

1. Vai a **Inventario > Regioni di vendita**. Se non la vedi, attiva **Abilita più magazzini** sotto **Impostazioni > Impostazioni del negozio > E-commerce** per visualizzare l' voce del menu — non hai bisogno di utilizzare veramente più magazzini per questo, basta che sblocchi il collegamento. Puoi anche andare direttamente a `/admin/catalog/salesregion/`.
2. Fai clic su **+ Aggiungi regione di vendita**
3. Compila i dettagli della regione:

| Campo | Descrizione | Esempio |
|-------|-------------|---------|
| **Nome della regione** | Nome visualizzato per questa regione | `Asia-Pacifico` |
| **Codice della regione** | Identificatore univoco breve | `APAC` |
| **Paesi** | Codici ISO dei paesi inclusi in questa regione | `["NZ", "AU", "SG", "FJ"]` |
| **Valuta predefinita** | Codice ISO della valuta per questa regione | `NZD` |
| **Priorità** | Le regioni con priorità più alta vengono matchate per prime | `10` |
| **Attivo** | Se questa regione è attualmente in uso | Selezionato |

4. Fai clic su **Salva**

### Codici dei paesi

Inserisci i paesi come elenco JSON di codici ISO a due caratteri. Ad esempio:
- Nuova Zelanda e Australia: `["NZ", "AU"]`
- Solo Singapore: `["SG"]`
- Tutta l'Europa: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Priorità

Se il paese di un cliente corrisponde a più di una regione, viene utilizzata la regione con il numero di priorità più alto. Imposta una priorità più alta per le regioni più specifiche (es. assegna una priorità di 20 a `NZ` e una priorità di 10 a `APAC` in modo che i clienti della Nuova Zelanda vengano abbinati per primi alla regione NZ).

## Controllo della visibilità dei prodotti per regione

Per impostazione predefinita, ogni prodotto è visibile in tutte le regioni. Per limitare un prodotto, apri il prodotto su **Prodotti > Tutti i prodotti** e imposta il campo **Disponibilità per regione** (nella sezione Stato) per permetterne la visualizzazione solo in regioni specifiche o in tutte le regioni tranne quelle specifiche, quindi scegli le regioni nella tabella sotto tale campo.

Questo determina anche cosa vedono gli utenti esterni alle regioni disponibili per il prodotto — se il prodotto viene nascosto interamente dagli elenchi, o visualizzato con un avviso "Non viene spedito in [regione]". Consulta la guida **Disponibilità per regione** per il percorso completo, incluso il settaggio di visualizzazione e il Selettore per la consegna.

## Valuta regionale

Ogni regione ha una valuta predefinita. Se il tuo negozio supporta esplicitamente più di una valuta (**Impostazioni > Multi-valuta**), la valuta visualizzata dal cliente cambia nella valuta predefinita della sua regione ogni volta che la sua regione cambia — sia che ciò avvenga dal prompt automatico della regione o dal Selettore per la consegna. I negozi con una sola valuta, o che non hanno deliberatamente abilitato la multi-valuta, mostrano sempre quella singola valuta, indipendentemente dalla regione.

Per impostare i prezzi in più valute, configura i tassi di cambio sotto **Impostazioni > Tassi di cambio**. I prezzi possono essere convertiti automaticamente o impostati manualmente per ciascuna valuta.

## Collegamento dei magazzini alle regioni

I magazzini vengono collegati alle regioni quando crei o modifichi un magazzino su **Catalogo > Magazzini**. Ogni magazzino appartiene a una regione, che controlla quale stock della regione viene utilizzato per effettuare gli ordini.

Per ulterioriore dettagli sui magazzini, consulta l'argomento **Inventario e magazzini** nella guida.

## Suggerimenti

- Mantieni i codici di area brevi e descrittivi (NZ, APAC, EU, US) - vengono utilizzati internamente e nei registri.
- Assegna numeri di priorità più elevati per aree più piccole e specifiche, in modo che abbiano la precedenza rispetto alle aree più ampie di backup.
- Se vendi solo in un singolo paese, non hai bisogno di configurare le aree geografiche affatto - Spwig funziona correttamente con un unico catalogo globale.
- Imposta solo la **Disponibilità per regione** del prodotto lontano da **Disponibile in tutte le aree** quando hai bisogno effettivamente di limitarla - il predefinito mantiene i prodotti universalmente disponibili senza bisogno di manutenzione.
- Controlla le regole per ciascuna area geografica ogni volta che aggiungi una nuova area di vendita, in modo che i limiti siano ancora in linea con quanto desiderato.
- Aggiungi il Selettore per la consegna nel tuo header (vedi la guida **Disponibilità per regione**) in modo da poter cambiare le aree geografiche e verificare che i prodotti limitati si comportino come previsto.