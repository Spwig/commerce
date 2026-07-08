---
title: Modelli SMS
---

I modelli SMS controllano il testo di ogni notifica che il tuo negozio invia ai clienti tramite messaggio di testo. Ogni modello corrisponde a un evento specifico, ad esempio una conferma dell'ordine o un aggiornamento sulla spedizione, e utilizza variabili di sostituzione che Spwig sostituisce con i dettagli reali dell'ordine quando il messaggio viene inviato.

Naviga in **Sistema SMS > Modelli SMS** per visualizzare e modificare i tuoi modelli.

![Elenco dei modelli SMS](/static/core/admin/img/help/sms-templates/templates-list.webp)

## Tipi di modello disponibili

Spwig include i seguenti tipi di modello predefiniti:

| Tipo di modello | Quando viene inviato |
|----------------|---------------------|
| Conferma ordine | Quando un cliente effettua un ordine |
| Aggiornamento spedizione | Quando lo stato di tracciamento di un ordine cambia |
| Notifica di consegna | Quando un ordine viene contrassegnato come consegnato |
| Reimpostazione password | Quando un cliente richiede una reimpostazione della password |
| Codice di verifica | Quando è necessario un codice temporaneo per la verifica dell'account |
| Ricevuta POS | Quando viene elaborato un acquisto al terminale di cassa |
| Marketing | Per campagne promozionali (richiede un consenso separato) |
| Personalizzato | Per qualsiasi altra notifica che crei |

## Modifica di un modello

1. Naviga in **Sistema SMS > Modelli SMS**
2. Fai clic sul modello che desideri modificare
3. Aggiorna il campo **Messaggio** con il testo desiderato
4. Utilizza i segnaposti `{variabile}` per includere informazioni specifiche dell'ordine (vedi le variabili di seguito)
5. Verifica **Attivo** per abilitare il modello — i modelli non attivi non vengono inviati
6. Fai clic su **Salva**

![Modifica di un modello SMS](/static/core/admin/img/help/sms-templates/template-edit.webp)

## Utilizzo delle variabili

Le variabili sono segnaposti scritti tra parentesi graffe — ad esempio, `{name}` o `{order_number}`. Quando Spwig invia il messaggio, sostituisce ogni segnaposto con il valore reale per quel cliente o ordine.

### Variabili comuni

| Variabile | Sostituito con |
|----------|---------------|
| `{name}` | Il nome del cliente |
| `{order_number}` | Il numero di riferimento dell'ordine |
| `{total}` | L'importo totale dell'ordine |
| `{tracking_number}` | Il numero di tracciamento della spedizione |
| `{store_name}` | Il nome del tuo negozio |
| `{code}` | Un codice di verifica o reimpostazione |

**Esempio di messaggio:**

```
Hi {name}, your order #{order_number} has been confirmed. Total: {total}. We'll update you when it ships. - {store_name}
```

Quando viene inviato, diventa:

```
Hi Sarah, your order #10045 has been confirmed. Total: $89.00. We'll update you when it ships. - The Garden Shop
```

> Includi solo le variabili disponibili per un tipo di modello specifico. Ad esempio, `{tracking_number}` è disponibile in un modello di aggiornamento spedizione ma non in un modello di reimpostazione password. Se utilizzi una variabile non disponibile, apparirà così com'è (non sostituita) nel messaggio.

## Limiti di caratteri e lunghezza del messaggio

I messaggi SMS standard sono limitati a **160 caratteri** per un singolo segmento. I messaggi più lunghi vengono suddivisi in più segmenti e inviati come un unico messaggio (SMS concatenato), ma i carrier contano ogni segmento separatamente per scopi di fatturazione.

**Consigli per rimanere entro il limite:**
- Mantieni i messaggi brevi — un solo scopo per messaggio
- Abbrevia le frasi comuni dove naturale (ad esempio, "Ord" invece di "Order")
- Evita parole di riempimento non necessarie

Spwig non impone un limite di caratteri rigoroso nell'editor, quindi conta i caratteri (inclusi i valori delle variabili) prima di salvare.

## Attivazione e disattivazione dei modelli

L'interruttore **Attivo** su ogni modello controlla se quel tipo di notifica viene inviato. Se un modello non è attivo, Spwig salta completamente l'invio di quella notifica — il messaggio apparirà come **Saltato** nella casella di uscita SMS con la ragione `template_inactive`.

Per attivare un modello:
1. Apri il modello
2. Verifica la casella **Attivo**
3. Salva

Per disattivare (fermare l'invio di un tipo di notifica senza eliminare il modello):
1. Apri il modello
2. Deseleziona **Attivo**
3. Salva

## Consigli
Preserva tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- Scrivi messaggi nello stesso tono della tua marca — l'SMS è un canale diretto e personale, quindi un tono amichevole funziona bene
- Includi sempre il nome del tuo negozio nel messaggio in modo che i clienti sappiano chi li sta contattando
- Mantieni i messaggi di conferma dell'ordine brevi: il numero dell'ordine, il totale e una nota sulle prossime azioni sono sufficienti
- Testa i messaggi effettuando un ordine di prova sul tuo negozio (utilizzando un numero di telefono che controlli) per vedere esattamente ciò che ricevono i clienti
- Se una notifica genera confusione o reclami, disattivala e rivedila invece di eliminarla — in questo modo puoi riattivarla una volta aggiornata
- I modelli di marketing devono essere inviati solo ai clienti che hanno espresso esplicitamente il consenso per ricevere la comunicazione via SMS, come richiesto dalle normative delle telecomunicazioni in molti paesi