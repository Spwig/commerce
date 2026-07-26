---
title: Accesso dello staff POS & Accesso con riconoscimento biometrico
---

Ogni persona che serve i clienti al registratore di cassa deve disporre di un account dello staff con i permessi corretti. Questo argomento spiega come creare quell'account, assegnare lo staff a un terminale e configurare l'accesso con riconoscimento biometrico in modo che possano sbloccare il registratore con un'impronta digitale, uno scan facciale o una chiave hardware invece di digitare una password ogni volta.

Per i codici PIN, i limiti degli sconti e le impostazioni del blocco del terminale, vedere [Sconti dello staff POS & Sicurezza del terminale](pos-staff-discounts).

## Cosa serve a uno staff membro per utilizzare un terminale POS

Per accedere a un terminale POS, una persona ha bisogno di:

1. Un **account dello staff** — un utente Spwig con il flag **Stato dello staff** abilitato.
2. Un **ruolo che include l'accesso al POS** — i ruoli controllano cosa può fare uno staff membro all'interno dell'amministrazione. È richiesto un ruolo con i permessi POS per accedere al registratore.
3. **Assegnazione al terminale** — il terminale deve elencarlo come membro dello staff assegnato, oppure deve essere assegnato a livello di ubicazione del negozio.

## Creare un account dello staff idoneo al POS

Navigare a **Staff & Accounts > Staff Members** (o andare a `/admin/accounts/staffmember/`).

1. Fare clic su **+ Aggiungi membro dello staff**.
2. Compilare il **nome**, il **cognome** e l'**indirizzo email** del membro dello staff.
3. Impostare una password temporanea e chiedere al membro dello staff di cambiarla al primo accesso.
4. Assicurarsi che **Stato dello staff** sia selezionato — è ciò che gli permette di accedere all'amministrazione e all'applicazione POS.
5. Fare clic su **Salva**.

> **Nota:** Non selezionare **Stato superutente** per cassieri o supervisori normali. Lo stato superutente bypassa tutti i controlli dei permessi e deve essere riservato al proprietario del negozio.

### Assegnare un ruolo con accesso al POS

Gli account dello staff da soli non hanno permessi — i ruoli concedono capacità specifiche. Dopo aver creato l'account, aprire il record del membro dello staff e andare alla sezione **Ruoli**. Assegnare un ruolo che include l'accesso al POS.

Per una spiegazione completa su come funzionano i ruoli e quali permessi includere, vedere [Ruoli dello staff](staff-roles).

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: staff-user-list.webp
  description: Elenco dei membri dello staff che mostra un utente idoneo al POS con il badge del ruolo
-->

![Elenco dei membri dello staff](/static/core/admin/img/help/pos-staff-login/staff-user-list.webp)

## Assegnare lo staff a un terminale

Le impostazioni seguono una cascata: **Predefinito del sito → Gruppo di negozi → Ubicazione del negozio → Terminale individuale**. Per la maggior parte dei negozi, il posto giusto per assegnare lo staff è a livello di terminale.

1. Navigare a **POS > Terminali** (o andare a `/admin/pos_app/posterminal/`).
2. Aprire il terminale che si desidera configurare.
3. Andare alla scheda **Assegnamento dello staff**.
4. Nel campo **Staff assegnato**, cercare e aggiungere il membro dello staff.
5. Fare clic su **Salva**.

I membri dello staff che appaiono nell'elenco **Staff assegnato** per un terminale possono selezionare il loro nome sulla schermata di accesso di quel terminale. Lo staff non assegnato a nessun terminale può comunque accedere digitando direttamente la loro email.

> **Consiglio:** Se il negozio ha molti membri dello staff che si spostano tra i terminali, assegnarli a livello di ubicazione del negozio (magazzino) invece che terminale per terminale. Qualsiasi membro dello staff assegnato all'ubicazione ha automaticamente accesso a tutti i terminali in quella ubicazione.

## Accedere al registratore POS

Quando un cassiere apre l'applicazione POS (`/pos/`) su un terminale, vede uno schermo di selezione dello staff. Il flusso di accesso funziona come segue:

1. Il cassiere tocca o clicca il proprio nome nell'elenco (o digita la propria email se non è elencato).
2. Digita la propria password.
3. Viene accesso e il registratore si apre per il loro turno.

Per lo sblocco basato su PIN (dopo che il terminale si blocca durante un turno), vedere [Sconti dello staff POS & Sicurezza del terminale](pos-staff-discounts).

## Accesso biometrico

L'accesso biometrico permette a un cassiere di toccare un sensore di impronte digitali, guardare una telecamera per il riconoscimento facciale o premere una chiave hardware invece di digitare una password. Su un registratore occupato, questo risparmia diversi secondi per turno e evita errori durante gli orari di punta.

Spwig utilizza lo standard del browser **WebAuthn** per l'accesso biometrico.

Una "credenziale WebAuthn" è una coppia di chiavi legata al dispositivo: la chiave privata è memorizzata nell'hardware sicuro del dispositivo e non ne esce mai.

L'applicazione POS comunica con tale hardware tramite il browser.

### Dispositivi e browser che supportano l'accesso biometrico

WebAuthn è supportato da tutti i browser moderni — Chrome, Edge, Firefox e Safari — sui dispositivi che dispongono di hardware compatibile. Configurazioni comuni che funzionano bene:

| Dispositivo | Autenticatore |
|------------|---------------|
| iPad (Touch ID) | Impronta digitale tramite Safari o Chrome |
| Tablet Android | Impronta digitale o riconoscimento facciale tramite Chrome |
| Tablet o PC Windows | Windows Hello (impronta digitale, riconoscimento facciale o PIN) |
| Qualsiasi dispositivo + chiave di sicurezza | Chiave FIDO2 USB, NFC o Bluetooth (es. YubiKey) |
| iPhone (Face ID) | Riconoscimento facciale tramite Safari |

L'applicazione POS mostrerà l'opzione di accesso biometrico solo quando il browser avrà confermato che una credenziale è registrata per l'utente corrente su quel dispositivo.

### Funzionamento della registrazione

La registrazione avviene al terminale POS, non nell'amministrazione. Il membro dello staff deve completare prima un accesso normale con password, quindi scegliere di configurare l'accesso biometrico all'interno dell'applicazione POS. Il browser quindi lo invita a verificare la propria identità utilizzando il sensore biometrico del dispositivo (o una chiave di accesso salvata nel loro account su iOS/macOS/Windows). Una volta confermato, la credenziale viene memorizzata e l'accesso biometrico sarà disponibile per i prossimi turni su quel dispositivo.

Un singolo membro dello staff può registrarsi su più dispositivi — ad esempio, un tablet personale e un registratore condiviso — e ogni dispositivo conserva la propria credenziale.

> **Nota:** La descrizione esatta del prompt di registrazione ("Registra biometrico", "Configura l'accesso con impronta digitale", ecc.) proviene dall'applicazione POS e può variare in base al browser e al dispositivo.

### Accedere con un biometrico

Una volta registrato, il nome del cassiere sulla schermata di accesso mostrerà un pulsante per l'accesso biometrico (icona dell'impronta digitale o simile). Il cassiere:

1. Tocca il proprio nome sulla schermata di accesso del terminale.
2. Tocca **Accedi con impronta digitale** (o equivalente).
3. Tocca il sensore o guarda la telecamera.
4. Il terminale si sblocca immediatamente.

Se la verifica biometrica fallisce (impronta non riconosciuta, volto oscurato), il cassiere passa all'inserimento della password.

### Revoca di una credenziale

Se un dispositivo è perso, rubato o un membro dello staff lascia, dovresti rimuovere immediatamente le sue credenziali biometriche.

1. Vai a **Staff & Accounts > Staff Members**.
2. Apri il record del membro dello staff.
3. Scorri fino alla sezione **POS Settings**.
4. Nella riga **Biometric Unlock**, fai clic su **Remove All**.
5. Conferma l'azione.

Questo rimuove tutte le credenziali WebAuthn registrate per quel membro dello staff su ogni dispositivo. La prossima volta che proverà a utilizzare l'accesso biometrico su qualsiasi terminale, sarà richiesto di accedere con la propria password invece.

> **Importante:** Rimuovere le credenziali qui non blocca il membro dello staff dall'accedere con la propria password. Per revocare completamente l'accesso, disattiva anche il loro account dello staff o rimuovili dall'elenco dei membri dello staff assegnati al terminale.

<!-- screenshots-needed:
- url: /en/admin/accounts/staffmember/
  filename: webauthn-credential-list.webp
  description: Form di modifica del membro dello staff che mostra la sezione POS Settings con il conteggio delle credenziali biometriche e il pulsante Remove All
-->

## Note sulla sicurezza

- **Le credenziali sono legate all'hardware.** La chiave privata non lascia mai l'elemento sicuro del dispositivo.

Se un tablet viene rubato, un attaccante non può estrarre la chiave biometrica — dovrebbe comunque bypassare lo schermo di blocco del dispositivo prima che il browser rilasci la chiave.
- **Perdita di un dispositivo non comporta la perdita di una password.** WebAuthn sostituisce la password per quel dispositivo; la password dello staff è separata e non influenzata.
- **Revoca immediatamente quando lo staff lascia.** Rimuovi le credenziali biometriche e disattiva l'account dello staff nello stesso sessione quando si sta disattivando un membro dello staff.
- **La biometria stessa non viene mai trasmessa.** L'impronta digitale o lo scan facciale viene elaborato interamente dal hardware del dispositivo.

Spwig riceve solo una risposta firmata al challenge, non alcun dato biometrico.

## Risoluzione dei problemi

### Il pulsante "Accedi con impronta digitale" non viene visualizzato

L'opzione biometrica appare solo quando:
- Lo staff ha una credenziale registrata su questo dispositivo specifico.
- Il browser supporta WebAuthn (tutti i browser moderni lo supportano — aggiorna se stai utilizzando una versione più vecchia).

Se il pulsante non è presente, lo staff non ha ancora effettuato la registrazione su questo dispositivo. Dovrebbe accedere con la password e configurare l'autenticazione biometrica tramite l'applicazione POS.

### Registrazione fallita

Motivi comuni:
- **Permesso del browser negato.** Il browser ha richiesto il permesso per accedere all'autenticatore e lo staff ha rifiutato. Lo staff deve riprovare e toccare **Consenti** quando richiesto.
- **Nessun autenticatore compatibile trovato.** Il dispositivo non ha un sensore di impronte digitali, una fotocamera per il riconoscimento facciale o una chiave di sicurezza collegata. Controlla il hardware del dispositivo.
- **Credenziale duplicata.** Lo staff potrebbe già aver effettuato la registrazione su questo dispositivo. Le credenziali esistenti vengono escluse durante la reregistrazione per evitare duplicati.

### La biometria funziona su un dispositivo ma non su un altro

Ogni dispositivo memorizza le proprie credenziali. Registrarsi su un iPad non funziona automaticamente su un secondo iPad. Lo staff deve completare la registrazione separatamente su ciascun dispositivo che userà.

### Passkeys tra dispositivi

Alcuni sistemi operativi (iOS 16+, macOS Ventura+, Windows 11 con un account Microsoft) possono sincronizzare i passkeys tra dispositivi tramite iCloud Keychain o Windows Hello. Se lo staff si è registrato utilizzando un passkey sincronizzato, potrebbe funzionare automaticamente su diversi dispositivi. Il comportamento dipende dal sistema operativo e dal browser, non da Spwig.

## Consigli

- Configura l'autenticazione biometrica sui registri condivisi prima che lo staff arrivi per il turno — il processo di registrazione di due minuti è molto più fluido quando viene eseguito senza clienti in attesa.
- Assegna un ruolo con permessi POS limitati ai cassieri e un ruolo separato per i supervisori. Mantieni i loro account distinti dall'account del proprietario del negozio.
- Quando un membro dello staff cambia dispositivo (nuovo tablet, nuovo telefono), fagli registrare sul nuovo dispositivo prima e revoca la credenziale vecchia dall'amministratore se il dispositivo non è più in uso.
- Per i negozi con un alto turnover dello staff, controlla periodicamente l'elenco **Staff assegnato** su ciascun terminale e rimuovi lo staff che non lavora più in quella sede.
- Se utilizzi chiavi di sicurezza hardware (YubiKey o simili), una chiave può essere registrata su diversi terminali senza alcun cambiamento nell'amministratore — basta collegare la chiave e completare la registrazione su ciascun terminale.