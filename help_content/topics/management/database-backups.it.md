---
title: Backup del database
---

I backup regolari proteggono i dati del tuo negozio — ordini, clienti, prodotti e configurazioni — da guasti hardware, cancellazioni accidentali e altri eventi imprevisti. Il sistema di backup di Spwig ti permette di creare backup su richiesta, impostare orari automatici, scaricare i backup localmente, ripristinare da qualsiasi backup salvato e copiare i backup in destinazioni di archiviazione remote come Amazon S3 o Google Drive.

Naviga verso **Gestione > Metriche del sistema** e usa i collegamenti della barra degli strumenti per accedere agli strumenti di backup.

![Dashboard del sistema con strumenti di backup](/static/core/admin/img/help/database-backups/system-dashboard.webp)

## Creare un backup manuale

Esegui un backup in qualsiasi momento prima di apportare modifiche significative — ad esempio, un import di prodotti, un aggiornamento del tema o un aggiornamento della piattaforma.

1. Naviga verso **Gestione > Metriche del sistema**
2. Clicca su **Crea backup completo** dalla barra degli strumenti
3. Inserisci un **Nome** descrittivo per il backup (es. `before-july-import`)
4. Aggiungi opzionalmente una **Descrizione** per ricordarti il motivo per cui è stato creato questo backup
5. Scegli un **Tipo di backup**:
   - **Sistema completo** — esegue il backup del database e di tutti i file multimediali (consigliato)
   - **Solo database** — esegue il backup dei dati del negozio, escludendo le immagini e i file caricati
6. Scegli la **Compressione** (`gzip` è il valore predefinito e funziona bene per la maggior parte dei negozi)
7. Clicca su **Crea backup**

Spwig crea il backup in background. Un indicatore di avanzamento mostra la fase corrente. Quando è completato, il backup appare nell'elenco **Backup del database** con lo stato **Completato** e la sua dimensione del file.

## Scaricare un backup

Puoi scaricare qualsiasi backup completato per conservare una copia locale sul tuo computer.

1. Naviga verso **Gestione > Backup del database**
2. Trova il backup che desideri scaricare
3. Clicca sul pulsante **Scarica** accanto ad esso

Il file del backup viene scaricato come un archivio compresso. Conservalo in un luogo sicuro — su un dispositivo separato o su un'archiviazione cloud — in modo da avere una copia indipendente dal tuo server.

## Programmare backup automatici

I backup automatici vengono eseguiti in background senza alcun intervento da parte tua, quindi i tuoi dati sono protetti anche se dimentichi di creare backup manuali.

1. Naviga verso **Gestione > Metriche del sistema**
2. Clicca su **Programma backup**
3. Seleziona **Abilita backup automatici**
4. Imposta la **Frequenza**:
   - **Giornaliera** — esegue una volta al giorno all'ora specificata
   - **Settimanale** — esegue una volta alla settimana nel giorno scelto
   - **Mensile** — esegue in un giorno specifico del mese
5. Imposta l'**Ora** in cui deve essere eseguito il backup (ora del server, tipicamente UTC — 03:00 AM è un'ora con poca attività)
6. Scegli il **Tipo di backup** (Sistema completo o Solo database)
7. Imposta i **Giorni di conservazione** — i backup più vecchi di questo numero di giorni vengono eliminati automaticamente (predefinito: 30 giorni)
8. Seleziona opzionalmente **Cripta backup** per criptare il file del backup in stato di riposo
9. Se hai destinazioni di archiviazione remote configurate, selezionali sotto **Destinazioni remote** per caricare automaticamente i backup programmati
10. Clicca su **Salva programma**

Il timestamp **Prossima esecuzione** si aggiorna immediatamente e mostra quando avverrà il prossimo backup automatico.

## Ripristinare da un backup

Il ripristino sostituisce i dati correnti del tuo negozio con il contenuto di un backup. Usa questa funzione per recuperare da una perdita di dati o per annullare modifiche indesiderate.

> **Importante:** Il ripristino sostituirà tutti i dati correnti con i dati del backup. Il tuo negozio verrà messo in modalità manutenzione durante il ripristino. Informa il tuo team prima di eseguire un ripristino.

1. Naviga verso **Gestione > Metriche del sistema**
2. Clicca su **Ripristina** dalla barra degli strumenti
3. L'elenco del ripristino mostra tutti i backup disponibili con le loro date e dimensioni
4. Clicca su **Ripristina** accanto al backup che desideri utilizzare
5. Controlla lo schermo di conferma — elenca esattamente cosa verrà sostituito
6. Digita la frase di conferma se richiesto, quindi clicca su **Esegui ripristino**

Spwig mostra una barra di avanzamento mentre il ripristino procede attraverso le sue fasi (backup dello stato corrente, download del backup se remoto, ripristino del database, ripristino dei file multimediali). Quando è completato, il negozio esce automaticamente dalla modalità manutenzione.

## Configurazione del backup su archivio remoto

L'archivio remoto copia automaticamente i tuoi backup in una destinazione esterna — Amazon S3, Google Drive, Dropbox o un server SFTP. Questo ti protegge da guasti a livello di server.

1. Vai a **Gestione > Metriche del sistema**
2. Fai clic su **Archivio remoto**
3. Fai clic su **Aggiungi destinazione**
4. L'assistente di configurazione ti guiderà attraverso tre passaggi:
   - **Passaggio 1**: Scegli il tipo di archivio (S3, Google Drive, Dropbox o SFTP)
   - **Passaggio 2**: Inserisci le credenziali per il provider scelto (vedi i dettagli di seguito)
   - **Passaggio 3**: Assegna un nome alla destinazione e testa la connessione
5. Dopo che il test di connessione ha successo, fai clic su **Salva**

### Amazon S3 (e servizi compatibili con S3)

Hai bisogno di:
- **Access Key ID** e **Secret Access Key** dall'utente IAM di AWS
- **Nome del bucket** — il bucket S3 in cui caricare i backup
- **Regione** — la regione AWS in cui si trova il bucket (es. `us-east-1`)
- Opzionalmente un **Prefisso** (percorso della cartella all'interno del bucket, es. `spwig-backups/`)

I servizi compatibili con S3 (Backblaze B2, Wasabi, MinIO, ecc.) funzionano allo stesso modo — inserisci l'URL dell'endpoint personalizzato quando richiesto.

### Google Drive

Fai clic su **Connetti con Google** nel passaggio delle credenziali. Spwig apre una finestra OAuth di Google — accedi e concede il permesso per caricare i file. Non è necessario copiare manualmente le credenziali.

### Dropbox

Fai clic su **Connetti con Dropbox** nel passaggio delle credenziali. Accedi a Dropbox e approva l'accesso. I backup vengono caricati in una cartella `Apps/Spwig` nel tuo Dropbox.

### SFTP

Hai bisogno di:
- **Hostname** del server SFTP
- **Porta** (predefinito: 22)
- **Nome utente** e **Password** (o chiave privata SSH)
- **Percorso remoto** — la directory sul server in cui caricare i backup

### Impostare una destinazione come predefinita

Nella pagina **Archivio remoto**, fai clic sul pulsante di commutazione accanto a qualsiasi destinazione per renderla **predefinita**. La destinazione predefinita riceve automaticamente ogni backup — manuale e programmato — senza doverla selezionare ogni volta.

## Consigli

- Esegui un backup manuale prima di ogni cambiamento significativo: importi di prodotti, modifiche al tema, aggiornamenti della piattaforma o campagne di sconto
- Programma i backup giornalieri a un orario di bassa intensità (es. 03:00) per minimizzare l'impatto sulle prestazioni
- Configura almeno una destinazione di archivio remoto in modo che i backup sopravvivano anche se il server stesso ha un problema
- L'impostazione **Retention Days** controlla per quanto tempo vengono conservati i backup locali — 30 giorni è un valore predefinito ragionevole per la maggior parte dei negozi, ma aumentalo se lo spazio di archiviazione lo permette
- Dopo un ripristino, controlla alcune ordinazioni e prodotti per confermare che i dati siano corretti prima di uscire manualmente dalla modalità manutenzione
- I backup crittografati aggiungono un livello di sicurezza ma richiedono la chiave di decriptazione per il ripristino — non perderla