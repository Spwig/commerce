---
title: Configurazione OAuth e Login Sociale
---

OAuth e login sociale permettono ai clienti di accedere al tuo negozio utilizzando i loro account esistenti di Google, Apple o Microsoft — non è necessario creare e ricordare un altro password.

![Impostazioni OAuth](/static/core/admin/img/help/oauth-social-login/oauth-settings.webp)

## Cosa è OAuth / Login Sociale?

OAuth è uno standard di autenticazione sicuro che permette ai clienti di accedere utilizzando credenziali da fornitori attendibili come Google, Apple o Microsoft.

### Vantaggi

- **Checkout più rapido** — I clienti saltano il modulo di registrazione e si accedono con un clic
- **Minore attrito** — Nessuna creazione di password, email di verifica o flussi per password dimenticate
- **Migliore conversione** — Studi mostrano che il login sociale può aumentare le tassi di conversione del 20-40%
- **Maggiore sicurezza** — Le credenziali non passano attraverso il tuo negozio; l'autenticazione è gestita dal fornitore
- **Fiducia del cliente** — I clienti si fidano dei fornitori stabiliti con le loro credenziali di accesso

### Funzionamento

1. Il cliente clicca su "Accedi con Google" (o Apple/Microsoft) sulla tua pagina di accesso
2. Vengono reindirizzati alla pagina di accesso sicura del fornitore
3. Il cliente si autentica con le credenziali del fornitore
4. Il fornitore invia le informazioni sull'identità verificata indietro al tuo negozio
5. Il cliente viene automaticamente accesso

Al primo accesso, un nuovo account cliente viene creato automaticamente utilizzando la loro email e informazioni del profilo dal fornitore.

## Fornitori Supportati

Spwig supporta tre principali fornitori OAuth:

| Fornitore | Caso d'uso | Requisiti delle credenziali |
|----------|----------|------------------------|
| **Google** | Più popolare, più facile da configurare | ID Client, Segreto Client |
| **Apple** | Richiesto per app iOS, orientato alla privacy | ID Client, ID Team, ID Chiave, Chiave Privata |
| **Microsoft** | Clienti aziendali, utenti Office 365 | ID Client, Segreto Client, ID Tenant |

Puoi abilitare uno, due o tutti e tre i fornitori. Ogni fornitore opera in modo indipendente.

## Configurazione OAuth di Google

L'OAuth di Google è l'opzione più popolare e la più facile da configurare.

### Requisiti preliminari

- Un account Google
- Accesso al Google Cloud Console

### Configurazione passo-passo

1. **Naviga verso le Impostazioni OAuth**
   - Vai a **Impostazioni > Impostazioni del negozio** nel tuo pannello di amministrazione
   - Scorri fino alla sezione **Fornitori OAuth**
   - Clicca su **Configura Google**

2. **Crea un Progetto Google Cloud**
   - Visita [Google Cloud Console](https://console.cloud.google.com/)
   - Clicca su **Crea Progetto**
   - Inserisci un nome del progetto (es. "My Store OAuth")
   - Clicca su **Crea**

3. **Abilita Google+ API**
   - Nel menu di sinistra, vai a **APIs & Services > Library**
   - Cerca "Google+ API"
   - Clicca su **Abilita**

4. **Crea le Credenziali OAuth**
   - Vai a **APIs & Services > Credentials**
   - Clicca su **Crea credenziali > ID client OAuth**
   - Seleziona il tipo di applicazione: **Web application**
   - Inserisci un nome (es. "Store Login")

5. **Configura l'URI di reindirizzamento**
   - Sotto **URI di reindirizzamento autorizzati**, aggiungi:
     ```
     https://yourdomain.com/accounts/google/login/callback/
     ```
   - Sostituisci `yourdomain.com` con il tuo dominio effettivo
   - Clicca su **Crea**

6. **Copia le Credenziali**
   - Copia l'**ID Client** e il **Segreto Client** dalla finestra di dialogo

7. **Inserisci le Credenziali in Spwig**
   - Torna alle impostazioni OAuth del tuo amministratore Spwig
   - Incolla l'ID Client e il Segreto Client
   - Clicca su **Salva**
   - Attiva **Abilita OAuth Google**

### Test

- Visita la pagina di accesso del tuo negozio
- Cerca il pulsante "Accedi con Google"
- Clicca e autentica con il tuo account Google
- Dovresti essere accesso e reindirizzato al tuo dashboard cliente

## Configurazione OAuth di Apple

L'OAuth di Apple è più complesso rispetto a Google a causa del sistema di autenticazione basato su chiavi.

### Requisiti preliminari

- Un account sviluppatore Apple (richiesto un abbonamento a pagamento)
- Accesso al portale sviluppatore Apple

### Configurazione passo-passo

1. **Naviga verso le Impostazioni OAuth**
   - Vai a **Impostazioni > Impostazioni del negozio > Fornitori OAuth**
   - Clicca su **Configura Apple**

2. **Crea un Service ID**
   - Accedi a [Apple Developer](https://developer.apple.com/account/)
   - Vai a **Certificati, Identificatori e Profili**
   - Clicca su **Identificatori** e poi sul pulsante **+**
   - Seleziona **Service IDs** e clicca su **Continua**
   - Inserisci una descrizione (es. "Store Login")
   - Inserisci un identificatore (es. `com.yourstore.login`)
   - Clicca su **Continua** e poi su **Registra**

3. **Configura il Service ID**
   - Clicca sul tuo nuovo Service ID creato
   - Seleziona **Accedi con Apple**
   - Clicca su **Configura**
   - Aggiungi il tuo dominio e l'URL di ritorno:
     - **Domini**: `yourdomain.com`
     - **URL di ritorno**: `https://yourdomain.com/accounts/apple/login/callback/`
   - Clicca su **Salva** e poi su **Continua** e **Salva** nuovamente

4. **Crea una Chiave**
   - Nel menu di sinistra, clicca su **Chiavi** e poi sul pulsante **+**
   - Inserisci un nome della chiave (es. "Store OAuth Key")
   - Seleziona **Accedi con Apple**
   - Clicca su **Configura** e seleziona il tuo ID App Primario
   - Clicca su **Salva**, quindi **Continua** e **Registra**
   - **Scarica il file della chiave** (.p8) — non puoi scaricarlo nuovamente

5. **Raccogli le informazioni necessarie**
   Hai bisogno di:
   - **ID Client** (Service ID): L'identificatore che hai creato (es. `com.yourstore.login`)
   - **ID Team**: Trovato in alto a destra nel portale sviluppatore Apple
   - **ID Chiave**: Mostrato quando hai creato la chiave
   - **Chiave Privata**: Il contenuto del file .p8 che hai scaricato

6. **Inserisci le Credenziali in Spwig**
   - Torna alle impostazioni OAuth di Spwig
   - Incolla l'ID Client, l'ID Team e l'ID Chiave
   - Apri il file .p8 in un editor di testo e copia il suo contenuto
   - Incolla l'intera chiave (inclusi gli header) nel campo Chiave Privata
   - Clicca su **Salva**
   - Attiva **Abilita OAuth Apple**

### Test

- Visita la pagina di accesso del tuo negozio su un dispositivo con un ID Apple
- Clicca su "Accedi con Apple"
- Autentica con il tuo ID Apple
- Dovresti essere accesso con successo

## Configurazione OAuth di Microsoft

L'OAuth di Microsoft è ideale per i negozi che si rivolgono a clienti aziendali che utilizzano Office 365 o Azure AD.

### Requisiti preliminari

- Un account Microsoft
- Accesso al portale Azure

### Configurazione passo-passo

1. **Naviga verso le Impostazioni OAuth**
   - Vai a **Impostazioni > Impostazioni del negozio > Fornitori OAuth**
   - Clicca su **Configura Microsoft**

2. **Registra un'applicazione in Azure**
   - Visita [Azure Portal](https://portal.azure.com/)
   - Vai a **Azure Active Directory > Registrazioni delle applicazioni**
   - Clicca su **Nuova registrazione**
   - Inserisci un nome (es. "Store OAuth")
   - Seleziona **Account in qualsiasi directory organizzativa e account personali Microsoft**
   - Sotto **URI di reindirizzamento**, seleziona **Web** e inserisci:
     ```
     https://yourdomain.com/accounts/microsoft/login/callback/
     ```
   - Clicca su **Registra**

3. **Copia l'ID dell'applicazione**
   - Nella pagina panoramica dell'app, copia l'**ID dell'applicazione (client)**

4. **Crea un Segreto Client**
   - Nel menu di sinistra, clicca su **Certificati e segreti**
   - Clicca su **Nuovo segreto client**
   - Inserisci una descrizione (es. "Segreto OAuth")
   - Seleziona un periodo di scadenza (consigliato: 24 mesi)
   - Clicca su **Aggiungi**
   - **Copia immediatamente il valore del segreto** — non sarà mostrato nuovamente

5. **Inserisci le Credenziali in Spwig**
   - Torna alle impostazioni OAuth di Spwig
   - Incolla l'ID dell'applicazione (client) come ID Client
   - Incolla il valore del segreto come Segreto Client
   - Opzionalmente inserisci un ID Tenant (per app a singolo tenant; lascia vuoto per app a multi-tenant)
   - Clicca su **Salva**
   - Attiva **Abilita OAuth Microsoft**

### Test

- Visita la pagina di accesso del tuo negozio
- Clicca su "Accedi con Microsoft"
- Autentica con il tuo account Microsoft
- Dovresti essere accesso con successo

## Gestione delle Connessioni OAuth

### Vista del Cliente

I clienti possono visualizzare e gestire le loro connessioni OAuth dal loro dashboard dell'account:

- Naviga a **Il mio account > Conti collegati**
- Vedi quali fornitori sono collegati (Google, Apple, Microsoft)
- Disconnetti un fornitore cliccando su **Disconnetti**
- Ricollega cliccando nuovamente per accedere con quel fornitore

### Fornitori Multipli

Un singolo account cliente può essere collegato a più fornitori OAuth. Ad esempio, un cliente può collegare sia Google che Apple allo stesso account.

Se un cliente tenta di accedere con un diverso fornitore OAuth utilizzando la stessa indirizzo email, Spwig collega automaticamente a loro account esistente.

### Gestione da Amministratore

Come amministratore, puoi visualizzare le connessioni OAuth dei clienti:

- Vai a **Clienti > Clienti**
- Apri un record cliente
- Scorri fino alla sezione **Conti collegati**
- Visualizza quali fornitori sono collegati e quando sono stati collegati

Non puoi disconnettere i fornitori al posto dei clienti — devono farlo da soli per motivi di sicurezza.

## Risoluzione dei Problemi

### Mismatch URI di Reindirizzamento

**Errore**: "Mismatch URI di reindirizzamento" o "redirect_uri non valido"

**Soluzione**:
- Assicurati che l'URI di reindirizzamento nelle impostazioni del fornitore corrisponda esattamente a quello in Spwig
- Controlla per slash finali — devono corrispondere
- Verifica che tu stia utilizzando `https://` (non `http://`)
- Pulisci la cache del browser e riprova

### Credenziali non valide

**Errore**: "ID client non valido" o "Autenticazione fallita"

**Soluzione**:
- Verifica che tu abbia copiato correttamente l'ID Client e il Segreto Client
- Assicurati che non ci siano spazi extra o interruzioni di riga
- Verifica che le credenziali provengano dal progetto/app corretto
- Per Apple, assicurati che la Chiave Privata includa l'intero contenuto del file .p8

### API del Fornitore non abilitata

**Errore**: "API non abilitata" o "Accesso non configurato"

**Soluzione**:
- Per Google: Assicurati di aver abilitato l'API Google+ nel tuo progetto Google Cloud
- Per Microsoft: Verifica che la registrazione dell'app sia approvata e attiva
- Per Apple: Controlla che "Accedi con Apple" sia abilitato per il tuo Service ID

### SSL Obbligatorio

**Errore**: "OAuth richiede HTTPS" o "URI di reindirizzamento non sicuro"

**Soluzione**:
- I fornitori OAuth richiedono SSL/TLS (HTTPS) per la sicurezza
- Assicurati che il tuo negozio abbia un certificato SSL valido installato
- Aggiorna i tuoi URI di reindirizzamento per utilizzare `https://` invece di `http://`
- Se stai testando localmente, utilizza un servizio come ngrok per creare un tunnel HTTPS

### Pulsante non visibile

**Problema**: Il pulsante "Accedi con Google/Apple/Microsoft" non appare sulla pagina di accesso

**Soluzione**:
- Verifica che il fornitore sia abilitato nelle impostazioni OAuth
- Pulisci la cache del browser e ricarica la pagina
- Controlla che il tema includa il modello di accesso sociale
- Controlla la console del browser per errori JavaScript

## Consigli e Buone Pratiche

### Sicurezza

- **Ruota i segreti regolarmente** — Aggiorna i segreti client ogni 12-24 mesi
- **Monitora gli accessi falliti** — Osserva per schemi di autenticazione insoliti
- **Utilizza credenziali separate per ogni ambiente** — Credenziali diverse per staging e produzione
- **Ristretti URI di reindirizzamento** — Aggiungi solo gli URI esatti di cui hai bisogno

### Esperienza Utente

- **Abilita tutti e tre i fornitori** — Dà ai clienti una scelta; diverse demografie preferiscono diversi fornitori
- **Posiziona i pulsanti in modo prominente** — I pulsanti di accesso sociale devono essere sopra il modulo email/password
- **Utilizza branding riconoscibile** — Mantieni lo stile standard dei pulsanti Google/Apple/Microsoft
- **Testa su mobile** — I flussi OAuth funzionano in modo diverso sui browser mobili

### Conformità

- **Informato sulla privacy** — Rivelare che utilizzi fornitori OAuth e i dati che ricevi
- **Termini di servizio** — Conformità ai termini dei fornitori (Google, Apple, Microsoft ciascuno ha requisiti)
- **Minimizzazione dei dati** — Richiedi solo le informazioni del profilo che effettivamente necessiti

### Elenco di controllo per i test

Prima di andare online, testa:

- [ ] Accedi con ciascun fornitore su desktop
- [ ] Accedi con ciascun fornitore su mobile
- [ ] Primo accesso (creazione account)
- [ ] Accessi successivi (collegamento account)
- [ ] Accedi con la stessa email attraverso diversi fornitori
- [ ] Disconnetti e ricollega un fornitore
- [ ] Il flusso di reimpostazione password funziona ancora per gli utenti non OAuth

Ricorda: Preserva tutti i formati markdown, percorsi delle immagini, blocchi di codice e termini tecnici esattamente come mostrato nelle regole di conservazione.