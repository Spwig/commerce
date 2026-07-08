---
title: Codici Buono
---

I codici buono ti permettono di creare codici sconto, coupon e carte regalo che i clienti possono inserire al momento del checkout per ottenere uno sconto. Naviga verso **Marketing > Buoni** nel menu laterale dell'amministratore.

![Elenco dei buoni](/static/core/admin/img/help/voucher-codes/voucher-list.webp)

## Dashboard dei Buoni

La pagina dei buoni mostra un riepilogo con:

- **Cartelle Statistiche** — Conteggio dei buoni attivi, non attivi, riscossioni e totali
- **Filtri** — Cerca per codice o nome, filtra per Tipo, Stato e Ambito
- **Cartelle dei Buoni** — Ogni buono visualizzato con dettagli sull'utilizzo e lo stato

## Creare un Buono

1. Clicca su **+ Aggiungi Buono** in alto a destra
2. Compila i dettagli del buono:
   - **Codice** — Il codice che i clienti inseriscono al momento del checkout (es. "SAVE20", "FREESHIP")
   - **Nome/Descrizione** — Descrizione interna per il tuo riferimento
   - **Tipo di Sconto** — Scegli come applicare lo sconto
   - **Valore dello Sconto** — L'importo o la percentuale di sconto
3. Configura le regole di utilizzo:
   - **Limite di Utilizzo** — Massimo totale di riscossioni (0 = illimitato)
   - **Limite per Cliente** — Massimo utilizzo per cliente
   - **Valore Minimo dell'Ordine** — Valore minimo totale del carrello richiesto
4. Imposta l'**ambito**:
   - **Intero Carrello** — Lo sconto si applica all'intero ordine
   - **Prodotti Specifici** — Si applica solo agli elementi selezionati
   - **Categorie Specifiche** — Si applica solo agli elementi delle categorie selezionate
5. Imposta eventualmente la scadenza:
   - **Data di Scadenza** — Quando il buono smette di funzionare
6. Clicca su **Salva**

## Tipi di Buoni

| Tipo | Descrizione | Esempio |
|------|-------------|---------|
| **Importo Fisso** | Deduce un importo fisso in dollari | $20 di sconto sull'ordine |
| **Percentuale** | Deduce una percentuale del totale | 15% di sconto sull'ordine |
| **Spedizione Gratuita** | Rimuove le spese di spedizione | Spedizione gratuita per qualsiasi ordine |

## Gestione dei Buoni

### Cartelle dei Buoni

Ogni cartella del buono mostra:
- **Codice** — Il codice del buono in grassetto
- **Descrizione** — Cosa fa il buono
- **Etichetta di Stato** — Attivo o Non attivo
- **Dettagli dello Sconto** — Tipo e valore (es. "$ 20.00" o "15.00%")
- **Ambito** — Se si applica all'intero carrello o a elementi specifici
- **Conteggio dell'Utilizzo** — Quante volte il buono è stato riscosso
- **Data di Creazione** — Quando è stato creato il buono
- **Scadenza** — Data di scadenza o "Nessuna scadenza"

### Azioni sui Buoni

Ogni cartella ha pulsanti per le azioni:
- **Modifica** — Modifica le impostazioni del buono
- **Visualizza Storico** — Vedi l'history delle riscossioni
- **Elimina** — Rimuovi il buono

### Filtrare i Buoni

Utilizza la barra di filtro per trovare buoni specifici:
- **Cerca** — Trova per codice, nome o descrizione
- **Tipo** — Importo Fisso, Percentuale o Spedizione Gratuita
- **Stato** — Attivo o Non attivo
- **Ambito** — Intero Carrello o specifico per prodotti

## Generazione di Buoni in Blocco

Per campagne di grandi dimensioni, puoi generare buoni in blocco:
1. Il sistema genera automaticamente codici unici (es. "COUPONX1600406498")
2. Imposta parametri comuni per tutti i buoni generati
3. Distribuisci i codici tramite e-mail, social media o stampa

## Esperienza del Cliente

Quando un cliente ha un codice buono:
1. Procede al **checkout**
2. Inserisce il codice nel campo **codice sconto**
3. Lo sconto viene applicato immediatamente se il buono è valido
4. Il riepilogo dell'ordine viene aggiornato per mostrare lo sconto

Se un buono non è valido (scaduto, limite di utilizzo raggiunto, valore minimo non soddisfatto), il cliente vede un messaggio di errore chiaro.

## Consigli

- Utilizza codici memorabili per le campagne di marketing (es. "SUMMER20" invece di stringhe casuali).
- Imposta limiti per cliente per prevenire l'abuso di sconti di valore.
- Utilizza valori minimi dell'ordine per mantenere la redditività (es. "$10 di sconto su ordini superiori a $50").
- Monitora il conteggio delle riscossioni sulla dashboard per tracciare l'efficacia delle campagne.
- Crea buoni con scadenza per creare urgenza (es. "Valido solo questo fine settimana").
- Utilizza lo stato Attivo/Non attivo per sospendere i buoni senza eliminarli.
