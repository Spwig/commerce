---
title: Single Sign-On (SSO) per l'amministrazione
---

Single Sign-On (SSO) consente al tuo personale di accedere al pannello di amministrazione utilizzando il provider di identità dell'organizzazione invece di un nome utente e una password separati. Spwig supporta qualsiasi provider di identità che utilizza il protocollo OpenID Connect (OIDC), incluso Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak e altri.

## Cosa è l'Enterprise SSO?

L'Enterprise SSO è diverso dal login sociale (l'accesso con un account personale Google o Facebook). Con l'Enterprise SSO:

- Il personale si autentica tramite il **provider di identità dell'organizzazione** — lo stesso sistema che utilizzano per la posta elettronica, gli strumenti interni e altre applicazioni aziendali
- Il team IT controlla centralmente l'accesso — quando qualcuno lascia l'organizzazione, disattivare il loro account nel provider di identità revoca immediatamente l'accesso a Spwig
- L'autenticazione a due fattori (MFA) è obbligata dal provider di identità, fornendo una politica di sicurezza coerente in tutte le applicazioni
- Il personale non deve ricordare una password separata per Spwig

## Funzionamento

Quando l'SSO è abilitato, la pagina di accesso amministratore mostra un pulsante **Accedi con [Provider]**. Il flusso di autenticazione funziona così:

1. Il membro dello staff clicca il pulsante SSO sulla pagina di accesso a Spwig
2. Vengono reindirizzati alla pagina di accesso del provider di identità (es. accesso Microsoft)
3. Si autenticano con il provider di identità (inclusi eventuali MFA richiesti dal provider)
4. Il provider di identità li reindirizza nuovamente a Spwig con un codice di autorizzazione sicuro
5. Spwig scambia il codice per le informazioni utente e crea una sessione
6. Il membro dello staff arriva al dashboard di amministrazione, completamente autenticato

Questo utilizza il protocollo **OpenID Connect (OIDC)** standard dell'industria, supportato da quasi tutti i provider di identità aziendali.

## Abilitare l'SSO

L'SSO è configurato in due luoghi:

1. **Impostazioni del sito > scheda Sicurezza** — Abilitare o disabilitare l'SSO e controllare la visibilità del login con password
2. **Configurazione del provider SSO** — Inserire i dettagli OIDC del tuo provider di identità

### Passaggio 1: Configurare il provider di identità

Prima di abilitare l'SSO in Spwig, devi registrare Spwig come applicazione nel tuo provider di identità. Vedi le guide specifiche per il provider:

- **Microsoft Entra ID** — vedi la guida per la configurazione di Microsoft Entra ID
- **Google Workspace** — vedi la guida per la configurazione di Google Workspace
- **Okta** — vedi la guida per la configurazione di Okta
- **Altri provider** — qualsiasi provider conforme a OIDC funziona. Registra un'applicazione web con URI di reindirizzamento `https://your-store.com/oidc/callback/` e consulta la documentazione del tuo provider per l'URL di scoperta OIDC, l'ID client e il segreto client.

### Passaggio 2: Configurare il provider SSO in Spwig

Vai alla pagina **Configurazione del provider SSO** (collegata dalla scheda Sicurezza o accessibile tramite **Enterprise SSO > Configurazione del provider SSO** nel menu laterale dell'amministratore). Inserisci:

1. **Nome del provider** — visualizzato sul pulsante di accesso (es. "Microsoft Entra ID")
2. **URL di scoperta OIDC** — l'URL `.well-known/openid-configuration` del tuo provider. Clicca su **Auto-Discover** per popolare automaticamente i campi degli endpoint.
3. **ID client** e **segreto client** — ottenuti dalla registrazione dell'applicazione nel provider di identità

Il segreto client viene memorizzato crittografato e non viene mai visualizzato dopo il salvataggio.

### Passaggio 3: Abilitare l'SSO nelle impostazioni del sito

Vai a **Impostazioni del sito > scheda Sicurezza** e seleziona **Abilita SSO per il login amministratore**. Il pulsante SSO apparirà immediatamente sulla pagina di accesso amministratore.

## Impostazioni SSO

| Impostazione | Descrizione |
|---------|-------------|
| **Abilita SSO per il login amministratore** | Mostra il pulsante SSO sulla pagina di accesso amministratore. Non influisce sul login con password a meno che non lo disattivi anche tu. |
| **Consenti il login con password sulla pagina amministratore** | Quando non è selezionato, il modulo di password è nascosto dietro un interruttore collassabile. Il personale vede solo il pulsante SSO di default. Il modulo di password può comunque essere accessibile cliccando su "Accedi con account locale" o aggiungendo `?password=1` all'URL di accesso. |

### Comportamento della pagina di accesso

| SSO Abilitato | Login con Password | Risultato |
|-------------|---------------|--------|
| Off | On | Pagina di login standard con modulo username/password solo |
| On | On | Pulsante SSO in alto, divisore "o", quindi modulo password sotto |
| On | Off | Solo pulsante SSO. Il modulo password è dietro un interruttore "Accedi con account locale" |
| Off | Off | Non possibile — il login con password viene automaticamente riattivato se SSO è disabilitato o non configurato |

## Corrispondenza Utente

Quando un membro dello staff si accede tramite SSO, Spwig lo associa a un account utente esistente tramite **indirizzo email** (senza distinzione tra maiuscole e minuscole). L'email proveniente dalle attestazioni del provider di identità deve corrispondere all'email sull'account dello staff di Spwig.

Se non viene trovato un utente corrispondente:

- **Creazione automatica utenti disabilitata** (predefinito) — l'accesso è negato. Devi creare l'account dello staff in Spwig prima con un indirizzo email corrispondente.
- **Creazione automatica utenti abilitata** — viene creato automaticamente un nuovo account utente con il nome e l'email provenienti dalle attestazioni del provider di identità.

La configurazione **Limita a Staff** (abilitata per default) aggiunge un controllo aggiuntivo: anche se un account utente esiste, l'accesso è negato a meno che l'utente abbia lo status di staff. Questo impedisce agli account non di staff di accedere al pannello di amministrazione tramite SSO.

## Mappatura dei Ruoli

Se il tuo provider di identità invia informazioni sui gruppi di appartenenza nelle attestazioni OIDC, Spwig può automaticamente impostare lo status di staff e superutente in base all'appartenenza ai gruppi.

Per configurare la mappatura dei ruoli:

1. Nel **Configurazione Provider SSO**, imposta il campo **Attestazione Gruppi** sul nome dell'attestazione utilizzata dal tuo provider (predefinito: `groups`)
2. In **Gruppi Staff**, inserisci i nomi o gli ID dei gruppi separati da virgole. Gli utenti appartenenti a uno qualsiasi di questi gruppi vengono assegnati lo status di staff.
3. In **Gruppi Superutente**, inserisci i nomi o gli ID dei gruppi separati da virgole. Gli utenti appartenenti a uno qualsiasi di questi gruppi vengono assegnati lo status di superutente.

La mappatura dei ruoli viene valutata ogni volta che un utente si accede tramite SSO. Se un utente viene rimosso da un gruppo nel provider di identità, lo status di staff o superutente viene aggiornato al loro prossimo accesso tramite SSO.

**Importante:** Microsoft Entra ID invia per default gli **ID oggetto** (UUID) dei gruppi, non i nomi dei gruppi. Copia l'ID oggetto dal portale Azure quando configuri la mappatura dei ruoli. Altri provider come Okta inviano in genere i nomi dei gruppi.

## Mappatura delle Attestazioni

Spwig legge le informazioni sull'utente da attestazioni OIDC standard. I valori predefiniti funzionano con la maggior parte dei provider, ma puoi personalizzare i nomi dei campi delle attestazioni nella **Configurazione Provider SSO**:

| Impostazione | Predefinito | Descrizione |
|---------|---------|-------------|
| **Attestazione Email** | `email` | L'attestazione che contiene l'indirizzo email dell'utente |
| **Attestazione Nome** | `given_name` | L'attestazione che contiene il nome dell'utente |
| **Attestazione Cognome** | `family_name` | L'attestazione che contiene il cognome dell'utente |
| **Attestazione Gruppi** | `groups` | L'attestazione che contiene le appartenenze ai gruppi (lascia vuoto per disabilitare la mappatura dei ruoli) |

## Comportamento MFA

Quando un membro dello staff si accede tramite SSO, la richiesta di autenticazione a due fattori (2FA) integrata in Spwig viene automaticamente bypassata. Questo è dovuto al fatto che il provider di identità è responsabile dell'applicazione di MFA come parte del flusso di login SSO.

Se la tua organizzazione richiede MFA, configurala nelle politiche di accesso condizionale del tuo provider di identità, non nelle impostazioni di 2FA di Spwig. Questo ti permette di gestire centralmente l'MFA su tutte le tue applicazioni.

## Accesso di Recupero

Se il tuo provider di identità ha un'interruzione o una configurazione errata, puoi comunque accedere al modulo di login amministratore:

- **Clicca sull'interruttore** — Se il login con password è disabilitato, clicca su "Accedi con account locale" sulla pagina di login per visualizzare il modulo password
- **Parametro URL** — Aggiungi `?password=1` all'URL di login amministratore (es. `https://your-store.com/en/admin/login/?password=1`) per visualizzare direttamente il modulo password
- **Il login con password è sempre disponibile** — Anche quando è nascosto nell'interfaccia utente, il backend di autenticazione con password rimane attivo. Solo la visibilità del modulo è influenzata.

Spwig impedisce anche di disabilitare l'accesso con password a meno che l'SSO non sia abilitato e configurato correttamente — non puoi accidentalmente bloccarti da solo.

## Fornitori supportati

Spwig funziona con qualsiasi provider di identità che supporta il protocollo OpenID Connect (OIDC). Sono disponibili guide dettagliate per la configurazione di:

- **Microsoft Entra ID** (ex Azure Active Directory)
- **Google Workspace** (Google Cloud Identity)
- **Okta**

Per altri fornitori conformi a OIDC (Auth0, Keycloak, OneLogin, Ping Identity, JumpCloud, ecc.), i passaggi di configurazione di Spwig sono gli stessi — hai bisogno dell'URL di discovery OIDC del provider, dell'ID client e del segreto client. Consulta la documentazione del tuo provider per scoprire come registrare un'applicazione web e ottenere queste credenziali. L'URI di ridirezione da utilizzare è sempre `https://your-store.com/oidc/callback/`.

## Consigli

- **Inizia con l'accesso con password abilitato** — Abilita l'SSO insieme all'accesso con password. Una volta confermato che l'SSO funziona per il tuo team, puoi disabilitare opzionalmente l'accesso con password.
- **Testa in una finestra incognito** — Utilizza una finestra del browser privata/incognito per testare l'SSO senza essere influenzato dalla tua sessione amministratore corrente.
- **Crea gli account dello staff prima** — A meno che non abiliti la creazione automatica degli utenti, i membri dello staff devono già avere un account Spwig esistente con un indirizzo email corrispondente prima di poter accedere tramite SSO.
- **Utilizza il pulsante Auto-Discover** — Inserisci l'URL di discovery OIDC del tuo provider e fai clic su Auto-Discover per popolare automaticamente tutti i campi degli endpoint. Questo è più veloce e meno soggetto a errori rispetto all'inserimento manuale degli endpoint.
- **Mantieni un account amministratore locale** — Mantieni sempre almeno un account amministratore locale con una password come opzione di recupero in caso di problemi con il provider di identità.
- **Monitora l'expirazione del segreto client** — Alcuni fornitori (in particolare Microsoft Entra ID) emettono segreti client con date di scadenza. Imposta un promemoria nel calendario per ruotare il segreto prima che scada.