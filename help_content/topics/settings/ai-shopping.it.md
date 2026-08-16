---
title: Acquisto con l'AI
---

L'acquisto con l'AI consente agli assistenti di acquisto AI di trovare i tuoi prodotti e, quando lo permetti, di acquistare dai tuoi negozi a favore di un cliente. È **disattivato per impostazione predefinita** - attivarlo è una scelta deliberata, e finché non lo fai, il tuo negozio non espone nulla a questi assistenti.

## Attivarlo

Apri **Impostazioni → Acquisto con l'AI** e attiva **Agentic commerce**. Da quel momento in poi, gli assistenti che supportano il protocollo universale per gli acquisti possono scoprire il tuo negozio e leggere il tuo catalogo. Nulla del tuo normale negozio cambia.

## Il pannello di preparazione

La parte in alto della pagina Acquisto con l'AI risponde a una domanda in una frase: **gli assistenti AI possono acquistare dal tuo negozio adesso?**

- **"Gli assistenti AI possono acquistare dal tuo negozio"** - tutto ciò che serve per un acquisto è a posto.
- **"Gli assistenti AI possono sfogliare il tuo negozio, ma non possono ancora acquistare"** - il tuo negozio è individuabile, ma manca qualcosa prima che un acquisto possa completarsi (di solito un fornitore di pagamenti connesso).
- **"Emergency stop attivo"** o **"Agentic commerce disattivato"** - nulla viene fornito agli assistenti.

Sotto la valutazione vedrai un breve elenco di controllo - fornitore di pagamenti connesso, la consegna può essere preventivata, i prodotti sono visibili agli assistenti - con un suggerimento accanto a qualsiasi elemento che necessita ancora di attenzione. I contatori mostrano quanti prodotti gli assistenti possono vendere, quanti hai nascosti loro, quanti assistenti hanno visitato e quanti hai bloccato.

L'elenco di controllo riflette la tua configurazione **attiva**: connetti un fornitore di pagamenti o aggiungi un metodo di spedizione e la valutazione si aggiorna la prossima volta che apri la pagina.

## La funzione di emergenza

La **funzione di emergenza** è un interruttore separato da quello principale. Usalo per fermare immediatamente tutte le attività degli assistenti - ad esempio, se qualcosa sembra sbagliato - senza modificare la tua configurazione. Cancialo per riprendere. Immagina che l'interruttore principale sia "questa funzione è configurata" e la funzione di emergenza sia "ferma tutto adesso".

## Cosa possono fare gli assistenti

Due livelli di accesso, gestiti separatamente:

- **Lettura** (individuazione e navigazione) è a basso rischio. Un assistente può trovare il tuo negozio e leggere i dettagli del prodotto.
- **Acquisto** (acquistare veramente) è a maggiore rischio e rimane chiuso agli assistenti non verificati, a meno che non lo permetti tu.

Un negozio può essere individuabile senza essere acquistabile - un modo utile per iniziare.

## Nascondere prodotti specifici

Ogni prodotto ha un'impostazione **Visibile agli agenti di acquisto con l'AI** (attivato per impostazione predefinita). Spegnilo per mantenere un prodotto specifico lontano dagli assistenti mentre rimane nel tuo negozio - utile per gli articoli che preferisci vendere solo attraverso il tuo sito.

## Gestire singoli assistenti

Quando un assistente effettua un acquisto - o prova a farlo - Spwig lo registra sotto **Acquisto con l'AI → Identità degli agenti**. Ogni voce mostra la casa verificata dell'assistente (la directory con cui si firma), il suo livello di fiducia e il numero di richieste che ha effettuato. Il nome e il logo che l'assistente presenta vengono visualizzati solo come dettagli *asseriti* - trattali come un'etichetta, non come prova d'identità; la casa verificata è la parte che può essere fidata.

Ogni assistente si trova in uno dei tre livelli di fiducia:

| Livello di fiducia | Cosa significa |
|---|---|
| **Limitato (verificato, limitato)** | Il default per un nuovo assistente. Spwig ha registrato la sua identità, e ha i vincoli di importo massimo, di spesa giornaliera e di restrizioni sui pagamenti imposti sulla sua policy (vedi sotto). |
| **Verificato (vincoli rimossi)** | Una decisione deliberata da parte tua di fidarti completamente di questo assistente. I vincoli di importo massimo e di spesa giornaliera vengono rimossi. |
| **Bloccato** | L'assistente non può più acquistare dal tuo negozio. Le aperture di acquisto in sospeso vengono chiuse, anche se qualsiasi pagamento già effettuato rimane intatto. |

Per fermare un assistente, selezionalo nell'elenco e scegli **Blocca gli assistenti selezionati**. **Sblocca gli assistenti selezionati** li rimette sempre nel **Limitato** - mai direttamente nel **Verificato** - perché rimuovere i vincoli è un passo separato, deliberato.

Per rimuovere completamente i vincoli di un assistente, selezionalo e scegli **Promuovi a verificato (rimuovi i vincoli)**.

Questo elimina il valore massimo dell'ordine e il tetto giornaliero di spesa e passa lo stato dell'assistente a Verificato.

Un assistente bloccato viene saltato: sblocalo prima, poi promuovilo.

Trattalo come una decisione di fiducia reale: promuovi solo un assistente del quale sei sicuro, poiché la verifica rimuove i vincoli di sicurezza con cui un nuovo assistente inizia.

## Impostare i limiti di un assistente

Apri la pagina dettagliata di un assistente e usa la sezione **Policy (limiti e offerte accettate)** per impostare ciò che è autorizzato a fare:

| Campo | Cosa controlla |
|---|---|
| **Valore massimo dell'ordine** | Il massimo singolo ordine che questo assistente può effettuare. Lascia vuoto per nessun limite. |
| **Tetto giornaliero di spesa** | Il massimo che questo assistente può spendere su tutti gli ordini in un giorno. Lascia vuoto per nessun limite. |
| **Consenti codici sconto** | Se l'assistente può applicare codici sconto al checkout. |
| **Consenti carte regalo** | Se l'assistente può riscattare le carte regalo. |
| **Consenti prodotti digitali** | Se l'assistente può acquistare prodotti digitali. |
| **Limite di richieste (al minuto)** | Quante richieste l'assistente può effettuare al tuo negozio al minuto. |

Un nuovo assistente inizia con limiti fissi sul valore dell'ordine e sul tetto giornaliero di spesa, e con l'abilitazione di codici sconto, carte regalo e prodotti digitali disattivati - il default deliberatamente conservatore. Modifica uno di questi campi e salva; ogni modifica viene registrata in **Agent Events** con i valori prima e dopo, quindi hai sempre un registro di chi ha modificato cosa e quando. Promuovere un assistente a Verificato elimina il valore massimo dell'ordine e il tetto giornaliero di spesa per te - non devi cancellarli manualmente.

## Il registro delle attività

**AI Shopping → Agent Events** è un registro invariabile di ciò che hanno fatto gli assistenti - ogni richiesta verificata, ogni tentativo bloccato, ogni modifica che hai effettuato. È visibile solo e non può essere modificato o eliminato, quindi rappresenta la tua traccia di prove se un acquisto effettuato da un assistente dovesse mai essere contestato.

## Un avvertimento sui piattaforme degli assistenti

Le aziende che gestiscono questi assistenti (e le regole per apparire in essi) sono nuove e cambiano spesso. Alcuni richiedono di inviare una domanda o di soddisfare condizioni regionali prima che i tuoi prodotti possano essere acquistati attraverso di essi. Spwig rende il tuo negozio pronto; se un determinato assistente ti elenca dipende dall'assistente stesso.

Mantieni tutta la formattazione markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.