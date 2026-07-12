---
title: Importo di massa dei codici voucher
---

L'assistente per l'importazione dei voucher ti permette di creare centinaia di codici voucher in una volta sola caricando un file CSV o XLSX. Questo è ideale quando hai codici già stampati, codici di un programma fedeltà da un sistema esterno o semplicemente hai bisogno di lanciare una campagna di grandi dimensioni senza aggiungere ogni codice a mano.

![Elenco dei voucher con pulsante Importa](/static/core/admin/img/help/voucher-import/voucher-list-import-button.webp)

## Iniziare un importo

Naviga verso **Marketing > Voucher** e fai clic sul pulsante **Importa** nell'area in alto a destra della pagina. Questo apre l'assistente per l'importazione a tre passaggi.

## Passaggio 1: Carica il tuo file e imposta le impostazioni del batch

![Form di caricamento dell'importo](/static/core/admin/img/help/voucher-import/import-upload.webp)

La prima pagina ha due parti: il caricamento del file e le impostazioni del sconto per il batch.

### Preparare il tuo file

Carica un file `.csv` o `.xlsx` di dimensioni massime di 5 MB. Il file deve avere una riga di intestazione come prima riga. Il requisito minimo è una singola colonna che contiene i codici voucher — ogni altra colonna è opzionale.

L'importatore riconosce automaticamente i nomi di colonna comuni. Se il tuo file utilizza uno dei nomi elencati di seguito, Spwig selezionerà automaticamente la mappatura corretta nella pagina successiva senza ulteriori clic:

| Nome della tua colonna | Mappa a |
|----------------------|--------|
| `code`, `voucher_code`, `coupon_code`, `promo_code` | Codice voucher |
| `name`, `title`, `campaign` | Nome interno |
| `description`, `details`, `note` | Descrizione rivolta al cliente |
| `external_id`, `member_id`, `reference` | ID esterno |

**Consiglio:** Scarica prima il modello XLSX (vedi [Esportare i voucher come modello](#exporting-vouchers-as-a-template) di seguito) — utilizza i nomi di colonna esatti che l'importatore aspetta, quindi la mappatura delle colonne è automatica.

### Limiti del file

- Dimensione massima del file: **5 MB**
- Righe massime per importo: **5.000 codici**

### Impostare le impostazioni del sconto del batch

Ogni voucher nel batch condividerà le stesse impostazioni di sconto che configurerai in questa pagina. Compila i campi come faresti quando crei un singolo voucher:

**Sezione sconto**

| Campo | Descrizione |
|-------|-------------|
| **Tipo di sconto** | Percentuale, Importo fisso o Spedizione gratuita |
| **Valore dello sconto** | La percentuale (0–100) o l'importo fisso da detrarre |
| **Importo massimo dello sconto** | Limite opzionale per gli sconti percentuali (es. limitare uno sconto del 20% a $50) |
| **Ambito di applicazione** | Carrello intero, Prodotti specifici o Categorie specifiche |

**Sezione validità**

| Campo | Descrizione |
|-------|-------------|
| **Data di inizio** | Quando i codici diventano attivi (predefinito come ora se lasciato vuoto) |
| **Data di fine** | Quando i codici scadono (lasciare vuoto per nessuna scadenza) |
| **Giorni di validità** | Alternativa alla data di fine — i codici scadono dopo questo numero di giorni dalla creazione |

**Sezione limiti di utilizzo**

| Campo | Descrizione |
|-------|-------------|
| **Utilizzo massimo totale** | Totale di redemptions consentiti per tutti i clienti (vuoto = illimitato) |
| **Utilizzo massimo per cliente** | Quante volte un cliente può utilizzare qualsiasi codice di questo batch |
| **Valore minimo dell'ordine** | Valore minimo del carrello richiesto prima che il codice venga applicato |

**Restrizioni**

Seleziona qualsiasi combinazione di:
- **Non applicabile a prodotti in offerta** — impedisce che il codice si sovrapponga a prodotti già scontati
- **Non combinabile con altri voucher** — impedisce ai clienti di utilizzare due codici nello stesso ordine
- **Non combinabile con prodotti in offerta** — simile al precedente ma mirato ai prodotti a prezzo di offerta
- **Solo per clienti nuovi** — limita il codice ai clienti senza ordini completati in precedenza
- **Attivo immediatamente** — lascia selezionato per rendere i codici attivi non appena vengono importati

Quando sei soddisfatto delle impostazioni, fai clic su **Continua per la prevista**.

## Passaggio 2: Mappare le colonne e rivedere

![Pagina di mappatura delle colonne e prevista](/static/core/admin/img/help/voucher-import/import-preview.webp)

La pagina di prevista mostra quattro contatori di sommario in alto:


- **Righe analizzate** — totale delle righe di dati trovate nel tuo file

- **Verranno importate** — nuovi codici che verranno creati

- **Duplicati** — codici che esistono già nel tuo catalogo

- **Verranno saltate (non valide)** — righe rifiutate a causa di errori di convalida (codice vuoto, codice troppo lungo, ecc.)

### Mappatura delle colonne

La tabella **Mappatura delle colonne** ti permette di indicare a Spwig quale colonna nel tuo file corrisponde a ogni campo del buono. Spwig rileva automaticamente i nomi degli header più comuni (vedi la tabella sopra), ma puoi modificare qualsiasi mappatura utilizzando il menu a discesa su ogni riga.

Solo la colonna **Codice del buono** è obbligatoria. Gli altri campi — **Nome interno**, **Descrizione rivolta al cliente** e **ID esterno** — sono opzionali. Se li salti, Spwig utilizza valori predefiniti sensati (il nome interno predefinito è "Buono importato {code}").

### Strategia per i codici duplicati

Se alcuni codici nel tuo file esistono già nel tuo catalogo, devi scegliere come gestirli:

| Strategia | Cosa accade |

|----------|-------------|

| **Salta i duplicati** | I codici esistenti vengono lasciati esattamente come sono. Vengono creati solo nuovi codici. |

| **Sovrascrivi le impostazioni** | I codici esistenti vengono aggiornati con le impostazioni di sconto di questo lotto. I loro codici, i contatori di utilizzo e le date di creazione vengono conservati. |

| **Annulla l'importazione** | L'intera importazione viene annullata se viene trovato anche un singolo duplicato. Utilizzalo quando hai bisogno di una garanzia che nessun codice esistente venga influenzato. |

Qualsiasi codice duplicato trovato viene elencato in un pannello espandibile in modo da poterli rivedere prima di decidere.

### Tabella anteprima dei dati

La parte inferiore della pagina mostra le prime 20 righe del tuo file in modo da poter confermare che la mappatura delle colonne sembra corretta prima di procedere. Le righe che corrispondono a codici esistenti sono evidenziate.

Quando tutto sembra corretto, fai clic su **Importa N buoni** per confermare il lotto.

## Passo 3: Rivedi il risultato

![Pagina del risultato dell'importazione](/static/core/admin/img/help/voucher-import/import-result.webp)

Dopo che l'importazione è completata, vedrai un riepilogo che mostra:

- **Importati** — codici creati con successo

- **Saltati** — codici che non sono stati creati (duplicati o righe non valide)

- **Righe elaborate** — totale delle righe del tuo file che sono state valutate

- **Falliti** — righe che hanno incontrato un errore inaspettato

Fai clic su **Visualizza buoni importati** per aprire l'elenco dei buoni filtrato solo sui codici di questo lotto, rendendo facile verificare il risultato o attivare di massa i nuovi codici.

Se qualcosa sembra sbagliato — ad esempio è stato applicato il tipo di sconto errato — puoi utilizzare la strategia **Sovrascrivi le impostazioni** su un'importazione di nuovo per correggere il lotto senza dover eliminare e ricreare i codici.

Fai clic su **Importa un altro lotto** per iniziare un nuovo caricamento, o su **Indietro all'elenco dei buoni** per tornare al tuo catalogo completo.

## Esportare i buoni come modello

L'elenco dei buoni supporta un'azione di esportazione XLSX che genera un file con lo stesso ordine di colonne che l'importatore aspetta. Questo è il modo più semplice per ottenere un modello correttamente formattato:

1. Vai a **Marketing > Buoni**

2. Seleziona i buoni che desideri esportare (o seleziona tutti)

3. Scegli **Esporta i buoni selezionati in XLSX** dal menu a discesa **Azione**

4. Fai clic su **Vai**

Il file scaricato contiene tutte e 21 le colonne che l'importatore comprende, tra cui i campi a livello di lotto nell'importatore (tipo di sconto, date, limiti di utilizzo, ecc.). Puoi utilizzare questo file come riferimento o far passare i tuoi codici esistenti attraverso un ciclo di modifica → rimportazione utilizzando la strategia **Sovrascrivi le impostazioni**.

## Suggerimenti

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- Scarica prima un'esportazione XLSX da utilizzare come modello — i nomi delle colonne sono già formattati in modo che l'auto-mappatura li riconosca senza dover apportare modifiche sulla pagina di anteprima.
- Esegui un piccolo batch di 5–10 codici prima di importarne centinaia per verificare che la mappatura delle colonne e le impostazioni del batch siano corrette.
- Usa **Giorni validi** invece di una data di fine fissa quando i codici saranno distribuiti nel tempo — la scadenza di ciascun codice verrà calcolata a partire dal momento in cui è stato importato, invece di una singola data del calendario.
- Se ricevi codici da un sistema di fedeltà di terze parti, mappa il riferimento membro o cliente del fornitore alla colonna **External ID** in modo da poter controllare le redemptions in seguito.
- Dopo un'importazione di grandi dimensioni, fai clic su **View imported vouchers** sulla pagina dei risultati per filtrare l'elenco solo per il nuovo batch — puoi quindi modificare di massa, attivare o disattivare i codici come gruppo.
- Un'importazione fallita (utilizzando la strategia di duplicato **Fail**) lascia il catalogo invariato, quindi è sicuro correggere il file e riprovare tante volte quante necessario.