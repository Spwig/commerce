---
title: Sincronizzazione Impostazioni
---

La sincronizzazione delle impostazioni ti permette di copiare la configurazione del negozio tra due installazioni di Spwig. Questo è ideale per mantenere ambienti di staging e produzione, dove configuri e testi i cambiamenti sull'ambiente di staging prima di deployarli nel tuo negozio live.

## Quando Usare la Sincronizzazione delle Impostazioni

- **Da Staging a Produzione**: Configura le impostazioni sul tuo negozio di staging, quindi spostale in produzione
- **Da Produzione a Staging**: Estrai le impostazioni di produzione nello staging per iniziare con un ambiente corrispondente
- **Backup della Configurazione**: Estrai le impostazioni da produzione a un'istanza di backup come misura di sicurezza

La sincronizzazione delle impostazioni gestisce solo i dati di configurazione -- non trasferisce prodotti, clienti, ordini o file multimediali. Per un trasferimento completo dei dati, usa invece la Migrazione Completa del Sistema.

## Cosa Può Essere Sincronizzato

La sincronizzazione delle impostazioni supporta le seguenti categorie:

| Gruppo | Categorie |
|-------|-----------|
| **Impostazioni** | Impostazioni del Sito, Tasse e Valuta, Tasse, Lingue, Impostazioni del Blog, Condivisione Sociale, Regioni di Vendita e Magazzini, Configurazione della Ricerca, Campi Personalizzati, Ruoli dello Staff, Analisi dei Clienti |
| **Design** | Design e Tema, Intestazioni/Piedi di Pagina/Menu |
| **Fornitori** | Email, SMS/WhatsApp, Fornitori di Pagamento, Spedizione, Fornitori SEO, Feed dei Prodotti, Connettori Social del Blog, Configurazione POS |
| **Contenuti** | Pagine e Template, Post del Blog, Annunci, Moduli, Collezioni di Prodotti |
| **Commercio** | Regole di Commercio (Buoni, Promozioni, Fedeltà, Abbonamenti), Programma di Affiliazione, Webhook e Integrazioni |

> **Nota:** Le categorie che contengono credenziali (fornitori di pagamento, account di spedizione, ecc.) sono contraddistinte da un'icona a forma di chiave. Le chiavi API e i segreti vengono trasferiti in modo sicuro, ma potrebbero dover essere reinseriti per le integrazioni basate su OAuth.

## Guida Passo Passo

### Passo 1: Configurare una Connessione

1. Naviga verso **Migrazione dei Dati > Sincronizzazione Spwig-Spwig** nel menu laterale di amministrazione
2. Clicca su **Avvia Sincronizzazione Impostazioni**
3. Seleziona una connessione salvata o crea una nuova connessione:
   - Inserisci l'URL del negozio remoto (es. `https://staging.yourstore.com`)
   - Incolla il token di sincronizzazione generato sul negozio remoto
   - Assegna alla connessione un nome descrittivo
   - Imposta il ruolo (Staging, Produzione, Backup o Altro)
4. Clicca su **Test Connessione** per verificare che funzioni
5. Clicca su **Avanti** per procedere

### Passo 2: Selezionare le Categorie e la Direzione

**Direzione:**
- **Estrai** -- Copia le impostazioni dal negozio connesso a questo negozio
- **Inserisci** -- Copia le impostazioni da questo negozio al negozio connesso

**Modalità di Sincronizzazione:**
- **Aggiungi e Aggiorna** -- Aggiunge nuovi elementi e aggiorna quelli esistenti, ma non elimina mai nulla. Questa è l'opzione più sicura.
- **Copia Esatta** -- Fa in modo che il target corrisponda esattamente alla sorgente, incluso l'eliminazione degli elementi presenti nel target ma non nella sorgente. Usa con cautela.

Seleziona le categorie che desideri includere, quindi clicca su **Avanti**.

### Passo 3: Anteprima dei Cambiamenti

Prima che vengano applicati qualsiasi cambiamento, vedrai un'anteprima dettagliata che mostra esattamente cosa verrà aggiunto, modificato o rimosso per ciascuna categoria. Controlla attentamente.

Se stai spostando su una connessione di produzione, dovrai confermare di comprendere che i cambiamenti influenzeranno il tuo negozio live.

Clicca su **Avvia Sincronizzazione** quando sei pronto.

### Passo 4: Monitorare i Progressi

La sincronizzazione viene eseguita in background. Puoi navigare liberamente lontano dalla pagina dei progressi -- la sincronizzazione continuerà comunque.

La pagina dei progressi mostra:
- Percentuale complessiva di completamento con tempo stimato rimanente
- Progresso per categoria con conteggio di successi/fallimenti
- Un registro di attività in tempo reale che puoi espandere per l'output dettagliato

## Rollback

Dopo che una sincronizzazione è completata, hai **24 ore** per eseguire un rollback. Un rollback ripristina lo stato precedente di tutte le impostazioni interessate.

Per eseguire un rollback:
1. Vai al **Pannello di Controllo della Sincronizzazione**
2. Trova il lavoro completato
3. Clicca su **Rollback** e conferma

Dopo 24 ore, l'opzione di rollback scade e i cambiamenti diventano permanenti.

## Consigli

Mantieni tutti i formati markdown, i percorsi delle immagini, i blocchi di codice e i termini tecnici.

- **Testa su staging prima**: Sincronizza sempre con un ambiente staging per verificare i risultati prima di spostare in produzione
- **Utilizza la modalità Aggiungi & Aggiorna**: Questa è la modalità più sicura poiché non elimina mai i dati esistenti
- **Controlla attentamente l'anteprima**: L'anteprima della differenza ti mostra esattamente cosa cambierà prima che venga applicato qualcosa
- **Le connessioni di produzione mostrano avvisi**: Quando si spinge a una connessione contrassegnata come Produzione, sono richieste conferme aggiuntive di sicurezza