---
title: Impostazioni dello schermo del cliente POS
---

Uno schermo per il cliente è un secondo schermo che si rivolge al vostro cliente durante un acquisto. Mentre gestite la transazione, il cliente vede ogni articolo man mano che viene scansionato, il totale parziale, la suddivisione dei prezzi e delle tasse, e - quando non c'è un acquisto in corso - uno slideshow rotante del vostro contenuto promozionale."
    },
    {
      "type": "paragraph",
      "content": "Questo documento copre l'hardware e l'aspetto del collegamento per impostare lo schermo del cliente: abilitare la funzione su un terminale, collegare un dispositivo separato come schermo e gestire scenari comuni di configurazione. Per informazioni sugli slideshow promozionali visualizzati durante i periodi di inattività, vedere [Customer Display Promo Slides](customer-display-promo-slides)."
    },
    {
      "type": "heading",
      "content": "Cosa mostra lo schermo del cliente"
    },
    {
      "type": "paragraph",
      "content": "Quando un acquisto è attivo, lo schermo del cliente mostra:"
    },
    {
      "type": "list",
      "content": [
        "Ogni articolo mentre viene aggiunto o rimosso, con quantità e prezzo",
        "Il sottototale del carrello, eventuali sconti applicati e la suddivisione delle tasse",
        "Il totale dovuto e, durante il pagamento, l'importo pagato e la restituzione"
      ]
    },
    {
      "type": "paragraph",
      "content": "Quando il terminale è inattivo (nessuna transazione attiva), lo schermo passa a uno slideshow promozionale. Controlli separatamente il contenuto di questo slideshow - vedere [Customer Display Promo Slides](customer-display-promo-slides)."
    },
    {
      "type": "heading",
      "content": "Configurazioni hardware comuni"
    },
    {
      "type": "paragraph",
      "content": "Esistono tre modi pratici per configurare uno schermo rivolto al cliente:"
    },
    {
      "type": "list",
      "content": [
        "**Tablet o monitor separato su un supporto** - la configurazione più comune per le vendite al banco. Un piccolo tablet appoggiato su un supporto rivolto al cliente mentre il vostro terminale principale rivolto a voi. Collegate i due dispositivi utilizzando un codice a breve termine (descritto di seguito).",
        "**Secondo monitor in modalità desktop esteso** - se il vostro terminale principale è un laptop o un desktop, collegare un secondo monitor, estendere il desktop su di esso, quindi trascinare la finestra dello schermo sul secondo monitor e massimizzarla. Entrambi gli schermi funzionano sullo stesso dispositivo; non è necessario un codice di collegamento.",
        "**Display dedicato su palo** - un'unità di display hardware montata su un palo, generalmente collegata al terminale del banco tramite USB o posizionata sul banco. Aprire `/pos/display/` nel browser del dispositivo sul palo e collegarlo utilizzando il codice dal terminale principale."
      ]
    },
    {
      "type": "heading",
      "content": "Abilitare lo schermo del cliente su un terminale"
    },
    {
      "type": "paragraph",
      "content": "La funzione dello schermo del cliente è abilitata per terminale tramite la configurazione hardware del terminale."
    },
    {
      "type": "list",
      "content": [
        "Navigare su **POS > Terminali** e aprire il terminale che si desidera configurare (o fare clic su **+ Aggiungi terminale POS** per un nuovo terminale).",
        "Fare clic sulla scheda **Dispositivo**.",
        "Scorrere fino alla scheda **Configurazione Hardware**. Si vedrà un campo JSON.",
        "Aggiungere `"customer_display": true` all'oggetto JSON. Ad esempio:"
      ]
    },
    {
      "type": "code-block",
      "content": "{'customer_display': true}"
    },
    {
      "type": "paragraph",
      "content": "Se il campo contiene già altre impostazioni hardware (ad esempio, la configurazione della stampante o dello scanner), aggiungere `"customer_display": true` insieme a esse:"
    },
    {
      "type": "code-block",
      "content": "{'printer': 'HP LaserJet', 'scanner': 'Datalogic', 'customer_display': true}"
    },
    {
      "type": "list",
      "content": [
        "Fare clic su **Salva**."
      ]
    },
    {
      "type": "image",
      "content": "![Configurazione hardware del terminale con customer_display abilitato](/static/core/admin/img/help/pos-customer-display-setup/terminal-capabilities-toggle.webp)"
    },
    {
      "type": "paragraph",
      "content": "Una volta abilitata, l'app POS su quel terminale aprirà la visualizzazione dello schermo del cliente in una seconda finestra o scheda del browser quando inizia una sessione."
    },
    {
      "type": "heading",
      "content": "Collegare un dispositivo separato come schermo"
    },
    {
      "type": "paragraph",
      "content": "Se si utilizza un dispositivo fisico separato per lo schermo del cliente (un tablet, un telefono o un secondo computer), si collega al terminale utilizzando un codice a 6 cifre a breve termine."
    },
    {
      "type": "heading",
      "content": "Passo 1: Generare un codice di collegamento sul terminale principale

Apri l'app POS sul tuo terminale principale e vai alle impostazioni del display o alla sezione di accoppiamento dell'interfaccia del terminale.

Richiedi un nuovo codice di accoppiamento per il display.

Il codice è un numero di 6 cifre e è valido per **5 minuti**.

Quando generi un nuovo codice, tutti i codici precedenti non utilizzati per questo terminale vengono automaticamente annullati.

### Passaggio 2: Apri l'URL del display sul dispositivo del cliente

Sul dispositivo rivolto al cliente, apri un browser web e vai a:

```
https://your-store-domain.com/pos/display/
```

Non è richiesto un login — la pagina del display è pubblicamente accessibile. Questo è intenzionale: il dispositivo del display non necessita di credenziali del personale, e il codice di accoppiamento fornisce il collegamento tra il display e il terminale corretto.

![Visualizzazione inattiva del display del cliente](/static/core/admin/img/help/pos-customer-display-setup/customer-display-view.webp)

### Passaggio 3: Inserisci il codice di accoppiamento

Sul dispositivo del cliente, inserisci il codice di 6 cifre proveniente dal terminale principale. Il display si accoppierà a quel terminale e inizierà a mostrare i dati del carrello in tempo reale.

Una volta utilizzato, il codice viene immediatamente invalidato e non può essere riutilizzato.

## Rigenerare un codice di accoppiamento

Se il codice di accoppiamento scade prima che tu possa inserirlo, o se devi riaccoppiare il dispositivo del display (ad esempio, se un dispositivo del display viene sostituito o resettato), genera un nuovo codice dall'app POS sul terminale principale.

La generazione di un nuovo codice annulla automaticamente qualsiasi codice esistente non utilizzato per quel terminale. Il nuovo codice è valido per 5 minuti.

Non è necessario modificare nulla nell'amministrazione per rigenerare un codice — tutto viene fatto interamente all'interno dell'app POS.

## Configurazione multi-monitor su un singolo dispositivo

Se il tuo terminale principale è un laptop o un desktop con due monitor:

1. Connetti il secondo monitor e impostalo in modalità **desktop esteso** nelle impostazioni del display del sistema operativo (non in modalità specchio).
2. Apri l'app POS sullo schermo principale come di consueto.
3. L'app POS aprirà il display del cliente in una seconda finestra. Trascina quella finestra verso il secondo monitor.
4. Massimizza o passa in modalità full screen sul secondo monitor.

Non è richiesto un codice di accoppiamento perché entrambe le finestre vengono eseguite sullo stesso dispositivo e comunicano direttamente.

## Comportamento inattivo

Quando non c'è un vendita attiva, il display del cliente mostra uno slideshow rotante di immagini promozionali. Crei e gestisci quegli slideshow separatamente sotto **POS > Promo Slides**.

Per dettagli sulla creazione degli slideshow, sull'indirizzamento a specifici negozi e sulla gestione del contenuto stagionale, vedi [Customer Display Promo Slides](customer-display-promo-slides).

Se non sono configurati slideshow, il display mostra un semplice schermo di benvenuto con il nome del tuo negozio.

## Risoluzione dei problemi

**Il display è diventato vuoto o ha smesso di aggiornarsi**

Il display comunica in tempo reale con il terminale principale. Se la connessione viene interrotta, il display potrebbe diventare vuoto o mostrare dati obsoleti. Aggiorna il browser sul dispositivo del cliente. Se non funziona, genera un nuovo codice di accoppiamento e riacoppia il display.

**Il display mostra il carrello del terminale sbagliato**

Ogni display è accoppiato a un terminale specifico. Se hai più terminali, assicurati di aver generato il codice di accoppiamento sul terminale corretto e di averlo inserito sul display. Per risolvere un mismatch, genera un nuovo codice sul terminale corretto e riacoppia il dispositivo del display.

**Il codice di accoppiamento è scaduto prima che potessi inserirlo**

I codici sono validi per 5 minuti. Genera un nuovo codice dall'app POS e inseriscilo immediatamente sul dispositivo del display. Mantieni i due dispositivi vicini durante il processo di accoppiamento.

**Il codice di accoppiamento è stato inserito ma il display non si è collegato**

Verifica che il dispositivo del cliente possa raggiungere il dominio del tuo negozio (ha bisogno di accesso alla rete). Verifica anche che `"customer_display": true` sia impostato nella configurazione hardware del terminale e che il terminale sia stato salvato.

**L'URL del display restituisce un errore**

Assicurati di navigare su `/pos/display/` nel dominio del tuo negozio, non sull'URL dell'amministrazione. La visualizzazione del display non richiede un login — se ti viene richiesto di effettuare il login, controlla nuovamente l'URL.

## Suggerimenti

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- **Mantieni breve la sessione di accoppiamento** — assicurati che il dispositivo del cliente sia pronto e il browser aperto su `/pos/display/` prima di generare il codice di accoppiamento.

Hai 5 minuti, ma completare l'operazione in meno di un minuto evita il timeout.
- **Testa prima di iniziare** — completa un test di vendita con il display collegato per verificare che i clienti vedranno gli articoli e i totali corretti prima della tua prima transazione reale.
- **Predisponi l'URL del display come segnalibro** — imposta il browser del dispositivo del cliente in modo da aprire automaticamente `/pos/display/` all'avvio, in modo che sia sempre pronto.
- **Utilizza lo schermo esteso per semplicità** — se il tuo terminale ha una porta HDMI disponibile e uno schermo a disposizione, l'approccio con lo schermo esteso non richiede un accoppiamento continuo e non scade mai.
- **Aggiungi diapositive promozionali prima di iniziare** — uno schermo vuoto che mostra solo una schermata di benvenuto è un'opportunità persa.

Configura almeno un paio di diapositive promozionali in modo che lo schermo sia utile anche quando non c'è una vendita in corso.

Vedi [Diapositive promozionali per lo schermo del cliente](customer-display-promo-slides).
- **Proteggi il dispositivo del display** — l'URL del display è accessibile pubblicamente per design, ma mostra i dati del carrello in tempo reale solo quando è accoppiato a un terminale attivo.

Tuttavia, considera di attivare la modalità browser kiosk sul dispositivo del cliente per impedire ai clienti di navigare altrove.