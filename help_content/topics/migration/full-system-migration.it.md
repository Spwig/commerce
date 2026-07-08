---
title: Migrazione Completa del Sistema
---

La Migrazione Completa del Sistema trasferisce l'intero negozio -- impostazioni, prodotti, clienti, ordini, file multimediali e tutti gli altri dati -- da un'installazione Spwig a un'altra. Utilizzala quando si passa a un nuovo server o si configura una copia completa del negozio.

## Quando Utilizzare la Migrazione Completa

- **Rilocazione del server**: Spostare il negozio verso un nuovo fornitore di hosting o server
- **Creare una copia di staging**: Configurare un ambiente di staging completo a partire da quello di produzione
- **Ripristino in caso di disastro**: Ripristinare un negozio completo da un'istanza di backup

La Migrazione Completa include tutto ciò che fa la Sincronizzazione delle Impostazioni, più tutti i dati transazionali (prodotti, clienti, ordini, recensioni, inventario, file multimediali, ecc.).

## Cosa Viene Migrato

La Migrazione Completa può trasferire tutte le categorie di impostazioni più queste categorie di dati:

| Categoria | Descrizione |
|----------|-------------|
| **Componenti Installati** | Temi, integrazioni dei fornitori e componenti utilitari con i loro file del pacchetto |
| **Prodotti, Categorie e Marchi** | Prodotti, varianti, immagini, categorie, marchi e attributi |
| **Libreria Multimediale** | Tutti i file multimediali e gli asset caricati |
| **Clienti e Indirizzi** | Account clienti, profili e indirizzi |
| **Storico Ordini** | Ordini, elementi degli ordini e registri delle transazioni |
| **Recensioni dei Prodotti** | Recensioni e valutazioni dei clienti |
| **Livelli di Scorta** | Quantità di inventario per magazzino e punti di rifornimento |
| **Prodotti Digitali e Licenze** | Asset digitali, modelli di licenza e pool di licenze |
| **Carte Regalo e Utilizzo dei Buoni** | Saldo delle carte regalo e registri dell'utilizzo dei buoni |
| **Credito del Negozio e Portafogli** | Saldo dei portafogli dei clienti e cronologia delle transazioni |
| **Membri del Programma di Fedelta** | Membri del programma di fedeltà, punti, transazioni e badge |
| **Abbonamenti Attivi** | Piani di abbonamento, abbonamenti attivi e cronologia dei pagamenti |
| **Spedizioni e Tracciamento** | Registri delle spedizioni e eventi di tracciamento |
| **Rimborsi, Resi e Note sugli Ordini** | Registri dei rimborsi, richieste di reso e note |
| **Membri Affiliati** | Account affiliati, codici di riferimento e cronologia delle commissioni |

## Guida Passo per Passo

### Passo 1: Connettersi all'istanza di origine

1. Naviga verso **Data Migration > Spwig-to-Spwig Sync** nel menu laterale di amministrazione
2. Clicca su **Start Full Migration**
3. Connettersi al negozio di origine (il negozio da cui si sta migrando):
   - Inserisci l'URL del negozio di origine
   - Incolla il token di sincronizzazione dal negozio di origine
   - Assegna un nome alla connessione (es. "Old Production Server")
4. Clicca su **Test Connection** per verificare
5. Clicca su **Next**

> **Importante:** La Migrazione Completa **preleva** sempre i dati dal negozio connesso in questo negozio. Esegui la procedura guidata sul **destinazione** (nuovo) negozio.

### Passo 2: Selezionare l'ambito

Seleziona quali categorie di dati includere nella migrazione. Le categorie sono organizzate in gruppi:

- **Impostazioni**: Configurazione del negozio, temi, fornitori, contenuti
- **Dati**: Prodotti, clienti, ordini, file multimediali e altri dati transazionali

Alcune categorie hanno dipendenze (es. gli Ordini dipendono dai Clienti e dai Prodotti). Le dipendenze vengono incluse automaticamente quando si seleziona una categoria.

Categorie con indicatori speciali:
- **Icona chiave**: Contiene credenziali che vengono trasferite in modo sicuro
- **Icona file**: Include file binari (immagini, file multimediali, pacchetti)
- **Icona avviso**: Considerazioni speciali per gli ambienti di produzione

### Passo 3: Controlli Pre-Migrazione

Prima che inizi la migrazione, i controlli automatici pre-migrazione verificano:

- **Salute della connessione**: Il negozio di origine è raggiungibile e autenticato
- **Compatibilità delle versioni**: Entrambi i negozi eseguono versioni compatibili di Spwig
- **Spazio su disco**: È disponibile un sufficiente spazio di archiviazione per i file multimediali
- **Prontezza del database**: Il database di destinazione può ricevere i dati

Se alcuni controlli falliscono, vedrai indicazioni specifiche su come risolvere il problema prima di procedere.

### Passo 4: Progresso della Migrazione

La migrazione viene eseguita in background. Puoi navigare liberamente -- il processo continuerà.


La pagina del progresso mostra:
- Percentuale complessiva con tempo stimato rimanente
- Stato di completamento per categoria
- Registro delle attività in tempo reale con dettagli del trasferimento
- Statistiche del trasferimento dei media (file e byte trasferiti) per la categoria media

Per negozi di grandi dimensioni con molti prodotti e file multimediali, la migrazione potrebbe richiedere del tempo. La fase di trasferimento dei media è generalmente la più lunga.

### Passaggio 5: Risultati

Dopo il completamento della migrazione, la pagina dei risultati mostra:

- Statistiche di riepilogo (elementi migrati, saltati, falliti)
- Analisi per categoria con stato
- Dettagli degli errori per gli elementi falliti

## Checklist post-migrazione

Dopo una migrazione riuscita, completa questi passaggi sul tuo nuovo negozio:

1. **Attiva il tuo licenziatario** sull'installazione nuova
2. **Riinserisci le credenziali del fornitore di pagamento** che sono state saltate durante la migrazione (le chiavi di sandbox/test non vengono trasferite in produzione)
3. **Configura il DNS** per puntare il tuo dominio al nuovo server
4. **Testa il flusso di checkout** con un ordine di test
5. **Verifica che l'invio delle email** funzioni correttamente
6. **Controlla i file multimediali** e verifica che le immagini si carichino correttamente

## Rollback

Dopo il completamento di una migrazione completa, hai **24 ore** per eseguire il rollback. Un rollback elimina tutti i dati migrati dal negozio di destinazione, ripristinandoli allo stato pre-migrazione.

Per eseguire il rollback:
1. Vai alla pagina dei risultati o al Dashboard di Sincronizzazione
2. Fai clic su **Rollback Migration** e conferma
3. Aspetta che il rollback venga completato

> **Avviso:** Il rollback rimuove definitivamente tutti i dati migrati. Qualsiasi modifica effettuata sul negozio di destinazione dopo la migrazione (nuovi ordini, iscrizioni dei clienti, ecc.) sarà influenzata.

Dopo 24 ore, l'opzione di rollback scade.

## Consigli

- **Esegui sul negozio di destinazione**: Il wizard di migrazione completa dovrebbe essere eseguito sul **nuovo** negozio, prelevando i dati dal vecchio
- **Migra su un'installazione pulita**: Per i migliori risultati, esegui la migrazione su un'installazione pulita di Spwig prima di andare in live
- **Verifica lo spazio su disco**: Assicurati che la destinazione abbia abbastanza spazio di archiviazione per tutti i file multimediali
- **Mantieni il negozio sorgente in esecuzione**: Non spegnere il negozio sorgente finché non hai verificato che tutto funziona correttamente sulla destinazione
- **Pianifica la transizione DNS**: Dopo aver verificato la migrazione, aggiorna i record DNS per puntare al nuovo server