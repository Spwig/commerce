---
title: Regole di visibilità
---

# Regole di visibilità

Le regole di visibilità ti consentono di mostrare o nascondere parti del tuo negozio in base a chi sta visitando e a dove si trova. Puoi bloccare **elementi della pagina**, **voci del menu** e **widget dell'header/footer** con le stesse condizioni: il mercato o la regione del cliente, la lingua o la valuta in cui sta visualizzando, l'ora del giorno, o segnali specifici per visitatore come se è autenticato.

Tutto è costruito da **gruppi di regole**: un insieme nominato e riusabile di una o più condizioni. Crei un gruppo di regole una volta (ad esempio, "mercato Nuova Zelanda" o "membri autenticati") e poi lo attacchi a qualsiasi elemento, voce del menu o widget che vuoi controllare. Un elemento senza gruppi di regole collegati è sempre visibile.

## Come viene decisa la visibilità

Quando a un elemento sono collegati più gruppi di regole, l'elemento viene visualizzato se **uno qualsiasi** dei gruppi collegati corrisponde (si combinano con OR). All'interno di un singolo gruppo scegli se **tutte** o **uno qualsiasi** delle sue condizioni devono corrispondere.

Le regole fanno parte di due famiglie e Spwig le gestisce in modo diverso per mantenere il tuo negozio veloce e friendly per i motori di ricerca:

- **Regole di mercato** — condizioni basate su regione/mercato, lingua, valuta e orario. Queste vengono decise sul server per ciascun URL di mercato, quindi la stessa pagina viene consegnata in modo identico a ogni visitatore (e a ogni motore di ricerca) a quel indirizzo. Questo mantiene le pagine memorizzabili e sicure per l'SEO.
- **Regole per visitatore** — stato di autenticazione, contenuto del carrello, dispositivo e posizione precisa. Queste dipendono dal singolo visitatore, quindi Spwig le risolve privatamente per ciascun utente dopo che la pagina è stata caricata. Non vengono mai cotte in una pagina condivisa e memorizzata.

Se disattivi un gruppo di regole, semplicemente smette di applicarsi - l'elemento a cui era collegato torna a essere visibile. Disattivare un gruppo non è un modo per nascondere qualcosa.

## Creare e collegare le regole

Esistono due modi per lavorare con i gruppi di regole.

### Collegarli dove li progetti

Ovunque tu possa bloccare il contenuto, vedrai un **controllo di visibilità** (l'icona dell'occhio):

- **Page Builder** - seleziona un elemento, apri le sue proprietà e usa il controllo di visibilità.
- **Menu Builder** - seleziona un elemento del menu e apri la scheda **Visibility**. Questo funziona su **qualsiasi** elemento, incluso un elemento di sottomenu (a tendina) annidato in un altro - una regola su un figlio nasconde solo quel figlio, lasciando intatto il resto del menu.
- **Header & Footer Builder** - seleziona un widget e apri la sezione **Visibility Rule Groups** delle sue impostazioni.

Le regole che dipendono dal singolo visitatore - se è autenticato, cosa c'è nel loro carrello o il loro dispositivo - vengono risolte per ciascun acquirente senza rallentare il tuo negozio o influenzare i motori di ricerca. Il tuo negozio rimane veloce e memorizzabile, e ogni visitatore vede solo la navigazione riservata a loro.

Nell'editor di visibilità puoi:

- **Collegare** qualsiasi gruppo di regole esistente selezionandoli.
- **Regola rapida** - crea un semplice gruppo di regole sul posto (ad esempio, "solo membri", un singolo mercato, una valuta, un dispositivo o un valore minimo del carrello) e collegarlo in un unico passaggio.
- **Gestisci i gruppi di regole** - vai al costruttore completo per regole avanzate.

Clicca su **Applica** e l'elemento viene bloccato immediatamente.

### Costruisci regole avanzate

Per qualsiasi cosa più complessa - combinare diverse condizioni, annidare gruppi o operatori specifici - vai a **Design → Visibility Rules** (gruppi di regole). Lì puoi assemblare le regole con logica AND/O e riutilizzarle in tutto il tuo negozio.

## Condizioni comuni

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

| Condition | Use it to… |
|-----------|------------|
| **Regione / mercato** | Mostra un blocco solo ai visitatori in un mercato specifico (es. Nuova Zelanda) |
| **Valuta selezionata** | Mostra note sui prezzi o offerte solo quando una certa valuta è attiva |
| **Lingua selezionata** | Mostra contenuti solo in una lingua specifica |
| **Data / orario / giorno / orari di apertura** | Esegui un banner durante una finestra di sconto o solo durante gli orari di apertura |
| **Stato accesso** | Mostra contenuti "riservati ai membri", o un invito alla registrazione per gli ospiti |
| **Tipo di dispositivo** | Mostra o nascondi qualcosa su dispositivi mobili, tablet o desktop |
| **Valore / articoli del carrello** | Mostra un suggerimento per la spedizione gratuita una volta superato un certo valore |

## Anteprima

Nell'anteprima del Page Builder puoi **anteprima come mercato** e **anteprima come visitatore** (accesso o ospite, con un carrello di esempio) per vedere esattamente cosa vedrebbe ogni pubblico — comprese le regole per visitatore che di solito vengono risolte in modo privato.

## Suggerimenti

- Costruisci un insieme piccolo di gruppi ben definiti ("mercato Nuova Zelanda", "Membri", "Solo mobile") e riusali ovunque — è più facile da gestire rispetto a regole singole.
- Le regole sul mercato sono la scelta sicura per qualsiasi cosa tu voglia indicizzata dai motori di ricerca, perché il risultato è lo stesso per tutti a un certo URL del mercato.
- Se un articolo scompare improvvisamente, controlla i gruppi di regole a cui è associato — un articolo viene nascosto solo quando ha un gruppo attivo e nessuno dei suoi gruppi corrisponde al visitatore corrente.