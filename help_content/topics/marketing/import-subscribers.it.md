---
title: Importazione di iscritti da un file CSV
---

Se hai già un elenco di iscritti in un altro posto - un vecchio strumento email, un foglio di calcolo con le iscrizioni alla newsletter, una pila di scanner di biglietti da eventi - non devi aggiungere quei contatti uno per uno su Spwig. L'importazione di iscritti da parte di Campaign Studio legge un file CSV o Excel e aggiunge ogni contatto valido al tuo pubblico in un colpo solo, pronto per l'etichettatura, la segmentazione e l'email.

## Prima dell'importazione: consenso

Ogni importazione richiede di spuntare una casella per confermare: **"Questi contatti hanno acconsentito a ricevere email di marketing da parte mia."** Questo non è un formalismo - importa solo contatti che si sono veramente iscritti a ricevere email di marketing da te. Conta per due motivi:

- **È un obbligo legale in molti posti.** Inviare email di marketing a persone che non hanno mai acconsentito a riceverle viola le leggi sul consenso in molte giurisdizioni.
- **Protegge la tua consegna.** Inviare email a persone che non si sono iscritte genera reclami per spam e ritorni, che i fornitori di posta utilizzano per decidere se *tutte* le tue email - comprese quelle a persone che si sono iscritte - arrivino nella casella di posta in arrivo.

Se un elenco non proviene chiaramente da iscrizioni attive, non importarlo.

## Preparazione del file

L'importatore accetta un file `.csv` o `.xlsx` con un'intestazione. È necessaria una sola colonna:

| Colonna | Obbligatorio? | Note |
|--------|-----------|-------|
| **Email** | Sì | Deve essere un indirizzo email valido. |
| **Nome** | No | Utilizzato per personalizzare le email. |
| **Cognome** | No | Utilizzato per personalizzare le email. |
| **Linguaggio** | No | Il codice della lingua preferita dell'iscritto (es. `en`, `es`). |

Le colonne vengono collegate a questi campi automaticamente dal nome dell'intestazione, quindi non devi rinominare nulla prima - variazioni comuni come `E-mail`, `Indirizzo email`, `Nome`, `Nome di battesimo`, `Cognome`, o `Lingua` sono tutte riconosciute.

Ogni importazione è limitata a **5 MB** e **5.000 righe**. Se il tuo elenco è più grande, suddividilo in file più piccoli e importali uno dopo l'altro.

## Importazione dei contatti

1. Apri **Campaign Studio > Iscritti** e clicca **Importa CSV**.
2. Scegli il tuo file `.csv` o `.xlsx`.
3. Scegli cosa succede **per gli iscritti già presenti nel tuo elenco** - vedi [Gestione dei duplicati](#gestione-dei-duplicati) qui sotto.
4. Facoltativamente scegli un'etichetta sotto **Etichetta gli iscritti importati come** per etichettare tutti i contatti in questa importazione (es. `Evento 2026`) - vedi [Etichette per iscritti](/help/etichette-iscritti) per ulteriori informazioni sulle etichette.
5. Spunta **Questi contatti hanno acconsentito a ricevere email di marketing da me**.
6. Clicca **Continua**.

![Il modulo di caricamento per l'importazione con un file selezionato, un'etichetta scelta e il consenso confermato](/static/core/admin/img/help/import-subscribers/import-upload-form.webp)

Spwig mostra quindi un anteprima prima che venga effettivamente importato qualsiasi contatto:

![Anteprima dell'importazione che mostra i conteggi di nuovi, esistenti e saltati non validi con motivazioni](/static/core/admin/img/help/import-subscribers/import-preview.webp)

- **Nuovi contatti** - le righe che creeranno un nuovo iscritto.
- **Già presenti nel tuo elenco** - le righe i cui indirizzi email corrispondono a un iscritto esistente.
- **Saltati (non validi)** - le righe che non è stato possibile leggere, ciascuna elencata con il numero della riga e la motivazione (un formato email non valido, una cella email vuota o un duplicato di una riga precedente nello stesso file).

Controlla questi numeri, quindi clicca **Importa adesso** per eseguire l'importazione, oppure **Annulla** per tornare indietro senza modificare nulla.

## Gestione dei duplicati

Una riga viene considerata un duplicato quando l'indirizzo email corrisponde a un iscritto che hai già. Scegli come Spwig tratterà quelle righe nella schermata di caricamento:

| Opzione | Cosa accade |
|--------|--------------|
| **Lasciali invariati** *(predefinito)* | Il nome e la lingua dell'iscritto esistente vengono mantenuti come prima. |
| **Aggiorna il loro nome/lingua** | Il nome, cognome e lingua dell'iscritto esistente vengono aggiornati dal file (solo per i campi che il file fornisce effettivamente). |

L'etichetta che scegli per l'importazione viene applicata a **tutti i contatti nel file** - nuovi e contatti esistenti - indipendentemente dall'opzione per i duplicati scelta.

Mantieni tutta la formattazione markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

Così facendo, l'importazione della vostra "lista VIP" con il tag **VIP** contrassegna le persone che avete già, allo stesso modo.

L'opzione duplica controlla solo se il *nome e la lingua* di un contatto esistente vengono sovrascritti.

## Dopo l'importazione

Ogni contatto creato tramite l'importazione viene registrato con la fonte **Importa**, e contrassegnato come acconsentito al momento in cui avete eseguito l'importazione (non una data precedente in cui potrebbero aver optato altrove). Il loro nome e cognome — se il file li ha forniti — vengono memorizzati nel record del sottoscrittore, il che significa che i campi di fusione `[[first_name]]` e `[[last_name]]` nei vostri invii personalizzati funzioneranno correttamente anche per loro, anche se non hanno mai creato un account Spwig.

## Suggerimenti

- Esportate la vostra lista di origine in un unico foglio CSV o in un file `.xlsx` con un'intestazione pulita prima di caricare — fogli extra, celle unite o righe di sintesi possono rendere confusi i corrispondenti delle colonne.
- Usate **Tagga i contatti importati come** per creare immediatamente l'audience esatta che vorreste targettizzare in seguito — vedete [Subscriber Tags](/help/subscriber-tags) per costruire un segmento da esso.
- Leggete sempre le **ragioni di Salta (non valide)** prima di assumere che un'importazione sia andata male — un piccolo numero di righe saltate con motivi chiari è normale per la maggior parte delle liste del mondo reale.
- Eseguire nuovamente lo stesso file è sicuro: i contatti già importati vengono considerati duplicati la seconda volta, non vengono ricreati.
- Se state consolidando diverse piccole liste, contrassegna ciascuna importazione in modo diverso (es. `Importa: Evento Gennaio`, `Importa: Fiera`) in modo da poterle distinguere in seguito anche dopo che saranno tutte mescolate nella vostra audience principale.
- Per liste con più di 5.000 righe, suddividetele in base a un confine chiaro (alfabetico, per fonte o per data di raccolta) invece di un taglio arbitrario, in modo che ciascun batch rimanga facile da identificare in seguito.