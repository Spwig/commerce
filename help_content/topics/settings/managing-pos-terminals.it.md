---
title: Gestione dei terminali POS
---

Gestire i terminali POS è la base delle tue operazioni retail. Ogni terminale rappresenta un dispositivo fisico (tablet, computer o hardware POS dedicato) dove lo staff elabora le vendite. Configura i terminali con assegnazioni del magazzino, autorizzazioni dello staff, integrazioni hardware e impostazioni di sincronizzazione offline. Monitora lo stato dei terminali con il tracciamento in tempo reale del 'heartbeat' e sblocca i terminali in modo remoto quando si verificano problemi. Una corretta gestione dei terminali garantisce operazioni fluide all'interno del negozio e previene conflitti di configurazione tra le diverse ubicazioni.

Accedi a **POS > Terminali** per registrare nuovi terminali, visualizzare lo stato online/offline e gestire tutte le impostazioni dei terminali.

![Elenco dei terminali](/static/core/admin/img/help/managing-pos-terminals/terminal-list.webp)

## Vista dell'elenco dei terminali

L'elenco dei terminali visualizza tutti i terminali registrati con informazioni di stato chiave:

**Nome del terminale** - Etichetta descrittiva per il terminale (es. "Checkout 1", "Main Register", "Mobile Terminal")

**UUID** - Identificatore univoco generato automaticamente al momento della creazione (usato internamente per l'identificazione del dispositivo)

**Magazzino** - Posizione fisica assegnata a questo terminale (determina la disponibilità di stock e l'attribuzione degli ordini)

**Stato online** - Indicatore in tempo reale che mostra se il terminale è attualmente connesso:
- **Punto verde** - Online (heartbeat ricevuto nell'ultimo 5 minuti)
- **Punto rosso** - Offline (nessun heartbeat per più di 5 minuti)
- **Punto grigio** - Mai accoppiato (terminale creato ma dispositivo mai connesso)

**Ultimo heartbeat** - Timestamp dell'ultimo ping ricevuto dal terminale (aggiornato ogni 5 minuti quando online)

**Codice di accoppiamento** - Codice alfanumerico di 8 caratteri utilizzato per l'accoppiamento iniziale del dispositivo (nascosto dopo il primo utilizzo)

**Utenti assegnati** - Numero di membri dello staff autorizzati ad utilizzare questo terminale

## Creare un nuovo terminale

Fai clic su **+ Aggiungi terminale** per registrare un nuovo dispositivo POS:

![Form per l'aggiunta di un terminale](/static/core/admin/img/help/managing-pos-terminals/terminal-add-form.webp)

### Configurazione di base

**Nome del terminale** - Scegli un nome descrittivo che indichi:
- Posizione fisica: "Register all'ingresso nord"
- Funzione: "Terminal per resi"
- Sequenza: "Checkout 1", "Checkout 2", "Checkout 3"

I nomi aiutano lo staff a identificare i terminali durante l'assegnazione delle shift e la risoluzione dei problemi. Utilizza convenzioni di denominazione coerenti in tutte le ubicazioni.

**Magazzino** - **OBIETTIVO** - Seleziona il magazzino da cui questo terminale opera:
- Determina quali stock sono disponibili per la vendita
- Gli ordini effettuati su questo terminale vengono attribuiti a questo magazzino
- Le prenotazioni di stock verificano la disponibilità nel magazzino assegnato
- **Non è possibile processare vendite senza l'assegnazione del magazzino**

Se hai più ubicazioni retail, crea un magazzino separato per ciascuna ubicazione e assegna i terminali di conseguenza.

**Attivo** - Toggle per abilitare/disabilitare il terminale senza eliminare la configurazione:
- I terminali non attivi non possono essere accoppiati
- Le sessioni esistenti sui terminali non attivi scadono immediatamente
- Utilizzare per disabilitare temporaneamente i terminali rubati o danneggiati

### Assegnazione dello staff

**Utenti assegnati** - Seleziona quali membri dello staff possono accedere a questo terminale:
- Solo gli utenti assegnati possono accedere al terminale
- Gli utenti devono anche avere i permessi POS nel loro ruolo di staff
- Assegnare zero utenti blocca effettivamente il terminale
- Modello comune: Assegnare tutti i membri dello staff a tutti i terminali del negozio

**Esempi di utilizzo**:
- **Negozio generico**: Assegna tutti i membri dello staff a tutti i terminali (qualsiasi cassiere può lavorare a qualsiasi cassa)
- **Negozio per dipartimenti**: Assegna membri dello staff specifici per i dipartimenti ai terminali dei dipartimenti
- **Multi-ubicazione**: Assegna membri dello staff specifici per le ubicazioni ai terminali delle ubicazioni
- **Gestione**: Assegna i manager a tutti i terminali per l'accesso di supervisione

Gli utenti senza assegnazione del terminale vedranno l'errore "Non autorizzato per questo terminale" quando cercheranno di accedere.

### Configurazione hardware

Il campo **Configurazione hardware** è una struttura JSON che definisce i dispositivi periferici:

**Stampante termica**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  }
}
```

**Scanner a codice a barre USB**:
```json
{
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  }
}
```

**Cassaforte** (connesso alla stampante):
```json
{
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

**Esempio completo**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  },
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  },
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

Lascia vuoto se il terminale non ha hardware periferico (adatto a terminali mobili o tablet senza stampante/scanner).

### Impostazioni del cache offline

Configura quanto dati il terminale memorizza per l'operazione offline:

**Giorni di sincronizzazione degli ordini** (7-30 giorni, predefinito: 14):
- Numero di giorni di ordini recenti da memorizzare localmente
- Valori più alti = più dati storici disponibili offline
- Valori più bassi = sincronizzazione più rapida, meno spazio di archiviazione utilizzato
- **Consiglio**: 7 giorni per terminali ad alto volume, 14 giorni per un uso normale, 30 giorni per operazioni di audit intensivo

**Limite di sincronizzazione degli ordini** (200-1000 ordini, predefinito: 500):
- Numero massimo di ordini da memorizzare indipendentemente dall'intervallo di date
- Impedisce l'uso eccessivo dello spazio di archiviazione sui terminali ad alto volume
- **Consiglio**: 200 per tablet con spazio di archiviazione limitato, 500 per terminali standard, 1000 per dispositivi POS dedicati

**Compromessi**:
- **Impostazioni più elevate**: Migliore accesso offline ai dati storici, sincronizzazione iniziale più lenta, maggiore utilizzo dello spazio di archiviazione
- **Impostazioni più basse**: Sincronizzazione più rapida, meno spazio di archiviazione, storia offline limitata

Il terminale scarica gli ultimi X ordini (entro Y giorni) in ogni ciclo di sincronizzazione. Se il terminale elabora 50 ordini/giorno e sync_days è 14, si prevede un totale di ~700 ordini memorizzati (potrebbe raggiungere il limite di sincronizzazione).

## Flusso di lavoro per l'accoppiamento del terminale

Dopo aver creato un terminale, accoppia il dispositivo fisico:

1. **Genera il codice di accoppiamento** - Creato automaticamente quando salvi il terminale (8 caratteri alfanumerici)

2. **Nota il codice** - Visualizzato nell'elenco dei terminali e nella vista dettagliata (scade dopo il primo accoppiamento riuscito)

3. **Naviga al terminale fisico** - Sul dispositivo fisico (tablet/computer), apri il browser e vai a: `https://yourstore.com/pos/`

4. **Inserisci il codice di accoppiamento** - Digita il codice di 8 caratteri quando richiesto

5. **Il terminale scarica la configurazione** - Il dispositivo riceve:
   - Assegnazione del magazzino
   - Configurazione hardware (stampa, scanner, cassetto)
   - Impostazioni del cache offline
   - Elenco degli utenti assegnati
   - Sincronizzazione iniziale del catalogo dei prodotti

6. **Schermo di accesso** - Il terminale mostra lo schermo di accesso per gli utenti assegnati

7. **Lo staff si accede** - Inserisci le credenziali dell'utente assegnato a questo terminale

8. **Sincronizzazione iniziale completata** - Il terminale scarica:
   - Ordini recenti (secondo sync_days e sync_limit)
   - Catalogo completo dei prodotti per il magazzino assegnato
   - Database dei clienti
   - Configurazioni promozionali

9. **Il terminale è pronto** - Appare lo schermo "Ready to Sell" con la barra di ricerca

10. **Codice di accoppiamento utilizzato** - Il codice viene rimosso dall'amministrazione; genera un nuovo codice se è necessario un nuovo accoppiamento

**Rigenerazione del codice di accoppiamento**: Se devi riacoppiare un terminale (reset del dispositivo, cache del browser pulita, nuovo hardware), utilizza l'azione amministrativa **Rigenera codice di accoppiamento**. Questo annulla il vecchio codice e ne crea uno nuovo.

## Monitoraggio dello stato del terminale

### Sistema di heartbeat

I terminali inviano un segnale di heartbeat al server ogni **5 minuti** che contiene:
- UUID del terminale
- Timestamp corrente
- Numero di utenti online
- Timestamp dell'ultima sincronizzazione
- Stato del Service Worker

**Indicatore di stato online**:
- **Verde** - Heartbeat ricevuto nell'ultimo 5 minuti (il terminale è online e operativo)
- **Rosso** - Nessun heartbeat per più di 5 minuti (il terminale è offline o disconnesso)
- **Grigio** - Il terminale mai accoppiato (nessun heartbeat mai ricevuto)

**Utilizzo**:
- **Apertura giornaliera**: Verifica che tutti i terminali siano online prima dell'apertura del negozio
- **Risoluzione dei problemi**: Identifica quali terminali stanno riscontrando problemi di connettività
- **Audit**: Verifica che i terminali siano attivi durante le ore di lavoro

### Timestamp dell'ultimo heartbeat

Mostra la data/ora esatta dell'ultimo heartbeat. Utilizza questo per:
- Determinare quanto tempo un terminale è stato offline
- Identificare i pattern (es. il terminale va offline ogni notte alla chiusura)
- Verificare la frequenza di sincronizzazione (dovrebbe aggiornarsi ogni ~5 minuti quando online)

## Funzione di sblocco remoto

Quando un terminale diventa non risponsivo o bloccato su uno schermo (crash del software, problemi di timeout della sessione, blocco del browser), utilizza l'azione amministrativa **Sblocco remoto**:

**Come funziona**:
1. Seleziona il terminale problematico nell'elenco amministrativo
2. Scegli **Sblocco remoto** dal menu delle azioni amministrative
3. Conferma l'azione
4. Il server invia un segnale di sblocco tramite la risposta del heartbeat
5. Il terminale riceve il segnale nel prossimo ciclo di heartbeat (<5 min)
6. Il terminale effettua automaticamente il logout dell'utente corrente e torna allo schermo di accesso

**Quando utilizzarlo**:
- Il terminale è bloccato sullo schermo della transazione
- Lo staff non riesce a disconnettersi (il pulsante di disconnessione non risponde)
- La sessione sembra attiva ma il terminale è non risponsivo
- Il browser è crashato ma il cookie di sessione persiste

**Importante**: Lo sblocco remoto **non** riavvia il dispositivo o il browser - forza solo il logout e la pulizia della sessione. Se il terminale è completamente bloccato, lo staff potrebbe dover riavviare manualmente il browser o il dispositivo.

## Modifica della configurazione del terminale

Fai clic su un terminale nell'elenco per modificare la sua configurazione:

![Form per la modifica del terminale](/static/core/admin/img/help/managing-pos-terminals/terminal-edit-form.webp)

**Modifiche sicure da effettuare mentre il terminale è online**:
- Nome del terminale
- Utenti assegnati
- Configurazione hardware (ha effetto dopo il riavvio dell'app del terminale)
- Impostazioni del cache offline (ha effetto sulla prossima sincronizzazione)

**Richiede un nuovo accoppiamento**:
- Assegnazione del magazzino (cambiare il magazzino richiede un nuovo accoppiamento per sincronizzare l'inventario nuovo)

**Non modificabile**:
- UUID (identificatore immutabile)

Le modifiche alla maggior parte delle impostazioni vengono applicate nel prossimo ciclo di heartbeat/sincronizzazione. I cambiamenti alla configurazione hardware richiedono che lo staff chiuda e riapra l'app POS (o aggiorni il browser).

## Risoluzione dei problemi comuni

**Il terminale mostra "Non autorizzato" durante l'accesso**:
- Verifica che l'utente sia nell'elenco **Utenti assegnati** per questo terminale
- Verifica che l'utente abbia i permessi POS in **Staff & Permissions > Roles**
- Controlla che il terminale sia contrassegnato come **Attivo**

**Il terminale non si accoppia (codice non valido)**:
- I codici di accoppiamento scadono dopo il primo utilizzo - rigenera se necessario
- I codici sono sensibili alle maiuscole/minuscole - verifica la capitalizzazione
- Controlla che il terminale sia contrassegnato come **Attivo**

**Il terminale mostra offline (punto rosso)**:
- Verifica che il dispositivo abbia la connessione internet
- Controlla che il terminale sia effettivamente in esecuzione (browser aperto sull'URL /pos/)
- Assicurati che il firewall non blocchi le richieste di heartbeat
- Aspetta 5 minuti per il prossimo ciclo di heartbeat

**Il terminale è lento nella sincronizzazione**:
- Riduci **Order Sync Days** da 30 a 7
- Riduci **Order Sync Limit** da 1000 a 200
- Controlla la velocità di rete nella posizione del terminale
- Verifica che il server non sia sotto carico elevato

**Stampante non funzionante**:
- Verifica l'indirizzo IP e la porta della stampante in **Hardware Config**
- Testa la connettività della stampante dal dispositivo terminale (ping dell'indirizzo IP)
- Controlla che la stampante sia compatibile ESC/POS
- Verifica che la stampante sia accesa e online

## Consigli

- **Le convenzioni di denominazione sono importanti** - Utilizza una denominazione coerente (ubicazione + numero) per semplificare la gestione su larga scala
- **Assegna sempre il magazzino prima dell'accoppiamento** - I terminali non possono processare vendite senza l'assegnazione del magazzino
- **Testa la configurazione hardware prima di distribuirla** - Stampa un ricevuta di test per verificare l'integrazione della stampante/cassetto
- **Monitora il heartbeat quotidianamente** - Imposta una routine per controllare che tutti i terminali siano online all'apertura del negozio
- **Riduci i limiti di sincronizzazione per i terminali mobili** - Tablet e smartphone beneficiano di sync_days: 7, sync_limit: 200
- **Utilizza lo sblocco remoto con moderazione** - Il logout forzato interrompe le transazioni attive; conferma che il terminale sia effettivamente bloccato prima di utilizzarlo
- **Documenta i codici di accoppiamento** - Scrivi giù il codice prima di distribuire il terminale al punto vendita (in caso l'installazione richieda più tempo del previsto)
- **Assegna un manager a tutti i terminali** - Garantisce che i supervisori possano accedere a qualsiasi cassa per annullamenti, rimborsi e risoluzione dei problemi