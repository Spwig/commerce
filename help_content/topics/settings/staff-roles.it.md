---
title: Staff Roles & Permissions
---

I ruoli del personale ti permettono di controllare esattamente cosa può vedere e fare ogni membro del team — sia nel pannello di amministrazione che nel terminale POS. Definisci ruoli con permessi specifici, quindi assegnali ai membri del personale. Un utente può avere più ruoli, e i suoi permessi effettivi sono la combinazione di tutti i ruoli assegnati.

![Staff roles](/static/core/admin/img/help/staff-roles/role-list.webp)

## How It Works

1. Crei **ruoli** che definiscono un insieme di permessi (es. "Order Manager", "Cashier")
2. Ogni ruolo controlla due tipi di accesso: **permessi del pannello di amministrazione** e **permessi POS**
3. **Assegnerai i ruoli** ai membri del personale dalla loro pagina del profilo
4. I permessi effettivi di un membro del personale sono l'**unione** di tutti i loro ruoli — se qualsiasi ruolo concede l'accesso, l'utente lo ha
5. I permessi sono **cachati** per prestazioni e vengono automaticamente aggiornati quando cambiano i ruoli

## Predefined Roles

Spwig include 7 ruoli predefiniti che coprono le strutture di team più comuni. Questi non possono essere eliminati, ma puoi creare ruoli personalizzati per esigenze più specifiche.

| Ruolo | Accesso | Descrizione |
|------|--------|-------------|
| **Store Owner** | Amministrazione + POS | Accesso completo a tutto. Per l'amministratore principale del negozio. |
| **Store Manager** | Amministrazione + POS | Operazioni quotidiane — accesso completo a prodotti, ordini, clienti, marketing e ricerca. Solo visualizzazione per design, email, pagamenti e impostazioni. |
| **Content Editor** | Amministrazione | Gestisce pagine, post del blog, design e media. Solo visualizzazione per i prodotti. |
| **Order Manager** | Amministrazione | Gestisce ordini, spedizioni, resi e servizio clienti. Solo visualizzazione per i prodotti. |
| **Marketing Manager** | Amministrazione | Gestisce promozioni, buoni, affiliati, fedeltà e programmi di referenza. Solo visualizzazione per prodotti, clienti e media. |
| **Cashier** | Solo POS | Personale POS di prima linea. Può processare vendite e controllare i saldi delle carte regalo. Nessun sconto, rimborso o gestione del denaro. |
| **Senior Cashier** | Solo POS | Personale POS esperto. Può processare rimborser, applicare sconti (fino al 25%), gestire il denaro e chiudere i turni. |

## Creating a Custom Role

Naviga verso **Settings > Staff Roles** e clicca **Add Role**.

### General Settings

| Impostazione | Descrizione |
|---------|-------------|
| **Display Name** | Il nome del ruolo visualizzato nell'amministrazione (es. "Warehouse Staff") |
| **Description** | Una breve spiegazione di a cosa serve questo ruolo |
| **Sort Order** | Controlla l'ordine di visualizzazione nell'elenco dei ruoli |
| **Icon** | Scegli tra 20 icone per identificare visivamente il ruolo |
| **Badge Color** | Colore utilizzato per i badge dei ruoli (Blu, Verde, Arancione, Rosso, Turchese, Grigio) |
| **Admin Panel** | Attiva/disattiva se questo ruolo concede l'accesso al pannello di amministrazione |
| **POS Terminals** | Attiva/disattiva se questo ruolo concede l'accesso ai terminali POS |

### Admin Permission Categories

La scheda dei permessi amministrativi organizza tutte le funzionalità della piattaforma in 13 categorie. Per ciascuna categoria, puoi impostare uno dei tre livelli di accesso:

- **None** — Nessun accesso a questa area (gli elementi del menu sono nascosti)
- **View** — Accesso in sola lettura (puoi vedere i dati ma non modificarli)
- **Full** — Accesso completo (puoi visualizzare, creare, modificare e eliminare)

![Permission categories](/static/core/admin/img/help/staff-roles/permission-categories.webp)

| Categoria | Cosa Controlla |
|----------|-----------------|
| **Product Catalog** | Prodotti, categorie, marchi, attributi, stock, magazzini, asset digitali |
| **Orders & Fulfillment** | Ordini, rimborser, resi, spedizioni, configurazione della spedizione |
| **Customers** | Profili clienti, segmenti, analisi |
| **Content & Pages** | Pagine, post del blog, annunce, moduli |
| **Design & Theme** | Temi, modelli di header/footer, menù, token di design, CSS personalizzato |
| **Marketing & Promotions** | Promozioni, buoni, affiliati, fedeltà, referenze, feed dei prodotti |
| **Media Library** | Immagini, video, cartelle, tag |
| **Email System** | Conti email, modelli, coda di consegna |
| **Payments & Billing** | Fornitori di pagamento, transazioni, webhooks, abbonamenti, tassi di cambio |
| **Search** | Impostazioni di ricerca, sinonimi, reindirizzamenti, analisi |
| **Store Settings** | Impostazioni del sito, geolocalizzazione, mappature dei paesi, regole aziendali |
| **POS Management** | Terminali POS, turni, movimenti di denaro, modelli di ricevute |
| **Users & Roles** | Account utenti del personale, ruoli, token API |

Quando un utente ha più ruoli, il **livello di accesso più alto** vince. Per esempio, se il Ruolo A concede "View" per Prodotti e il Ruolo B concede "Full", l'utente ha accesso "Full".

### POS Permission Flags

Se il ruolo concede l'accesso POS, la scheda dei permessi POS ti permette di regolare esattamente cosa un operatore POS può fare. Questi sono separati dai permessi amministrativi e vengono controllati direttamente nel terminale POS.

![POS permissions](/static/core/admin/img/help/staff-roles/pos-permissions.webp)

| Gruppo | Permesso | Descrizione |
|-------|-----------|-------------|
| **General** | Accesso POS | Può utilizzare il sistema POS in generale |
| **Sales & Discounts** | Sconti Manuali | Può applicare sconti su singoli articoli o a livello di carrello |
| | Percentuale Massima di Sconto | La percentuale massima di sconto consentita (0–100) |
| | Override Prezzo | Può sovrascrivere i prezzi dei prodotti al registratore di cassa |
| **Refunds & Voids** | Processa Rimborser | Può processare rimborser sugli ordini POS |
| | Annulla Ordini | Può annullare ordini POS dal turno corrente |
| **Gift Cards** | Emetti Carte Regalo | Può emettere nuove carte regalo al registratore di cassa |
| | Controlla Saldo Carta Regalo | Può controllare i saldi delle carte regalo |
| **Cash Management** | Gestione del Denaro | Può eseguire operazioni di deposito e prelievo di denaro |
| | Apri Cassa | Può aprire la cassa senza un acquisto |
| | Chiudi Turni | Può chiudere i turni e eseguire la conciliazione del denaro |
| **Reporting** | Visualizza Report POS | Può visualizzare i report dei turni e le sommari delle vendite |
| **Inventory** | Regolamento del Stock | Può regolare i livelli di stock (ricezione, danni, riconte, resi) |

Per i permessi booleani, se **qualsiasi** dei ruoli dell'utente lo abilita, l'utente lo ha. Per la Percentuale Massima di Sconto, il **valore più alto** tra tutti i ruoli si applica.

## Managing Staff Members

Naviga verso **Settings > Staff Management** per visualizzare e gestire il tuo team.

### Staff List

L'elenco del personale mostra tutti gli utenti con accesso al personale. Per ciascun membro, puoi vedere:
- **Nome e email**
- **Ruoli assegnati** (mostrati come badge colorati)
- **Tipo di accesso** — Solo Amministrazione, Solo POS o Entrambi
- **Stato 2FA** — Se l'autenticazione a due fattori è abilitata
- **Stato Attivo/Inattivo**

Utilizza i filtri per restringere per ruolo, tipo di accesso o stato 2FA.

### Assigning Roles to Staff

1. Clicca su un membro del personale per aprire il suo profilo
2. Nella sezione **Ruoli**, vedrai le schede per ogni ruolo disponibile
3. Clicca sul toggle di qualsiasi scheda di ruolo per assegnare o rimuovere il ruolo
4. Le modifiche hanno effetto immediatamente — non è necessario un pulsante di salvataggio
5. Il riepilogo **Effective Permissions** qui sotto mostra il risultato combinato di tutti i ruoli assegnati

### Adding a New Staff Member

1. Naviga verso **Settings > Staff Management** e clicca **Add Staff Member**
2. Inserisci l'email, il nome e il cognome dell'utente
3. Imposta una password temporanea
4. Assegna uno o più ruoli
5. L'utente può ora accedere con l'accesso fornito dai suoi ruoli

## Cloning Roles

Per creare un nuovo ruolo basato su uno esistente:

1. Apri il ruolo che desideri copiare
2. Clicca **Clone Role** in fondo alla pagina
3. Viene creato un nuovo ruolo con tutti i permessi identici
4. Rinominalo e modifica i permessi come necessario
5. Salva il nuovo ruolo

Questo è utile quando hai bisogno di un ruolo simile a uno esistente con piccole differenze — ad esempio, un "Junior Manager" basato su "Store Manager" ma con meno permessi.

## How Permissions Are Applied

### Admin Panel

- **Visibilità del menu** — Le sezioni del sidebar sono nascoste per le categorie in cui l'utente ha accesso "None"
- **Accesso alle pagine** — Provare a visitare una pagina restrittiva mostra un errore di permesso
- **Limitazioni alle azioni** — Con l'accesso "View", i pulsanti di modifica e cancellazione sono nascosti e le azioni di salvataggio sono bloccate
- **Bypass superuser** — Gli account superuser hanno sempre accesso completo indipendentemente dall'assegnazione dei ruoli

### POS Terminal

- **Gate di accesso** — Solo gli utenti con almeno un ruolo che ha "POS Terminals" abilitato possono accedere al POS
- **Toggle delle funzionalità** — I pulsanti e le azioni POS (rimborser, sconti, annullamenti, ecc.) vengono mostrati o nascosti in base ai permessi POS combinati dell'utente
- **Limite di sconto** — La Percentuale Massima di Sconto impone un limite fisso su quanto grande uno sconto un operatore POS può applicare
- **Enforcement API** — Tutti i permessi POS vengono controllati a livello server nell'API, non solo nell'interfaccia utente

## Tips

- **Inizia con i ruoli predefiniti** — I 7 ruoli predefiniti coprono la maggior parte delle strutture di team. Crea ruoli personalizzati solo quando hai bisogno di controlli di accesso più specifici.
- **Utilizza la funzione di clonazione** — Quando hai bisogno di un ruolo simile a uno esistente, clonalolo e modificalo invece di crearlo da zero.
- **Assegna più ruoli quando necessario** — Un membro del personale che gestisce sia ordini che marketing può essere assegnato sia al ruolo "Order Manager" che al ruolo "Marketing Manager". I permessi si combinano automaticamente.
- **Separa l'accesso amministrativo e POS** — I cassieri di solito non necessitano dell'accesso amministrativo, e il personale d'ufficio non necessita dell'accesso POS. Utilizza i toggle di accesso per mantenere le cose pulite.
- **Imposta limiti di sconto per il personale POS** — La Percentuale Massima di Sconto impedisce ai cassieri di applicare sconti eccessivi. Impostala a 0 per disabilitare i sconti, o un limite ragionevole come 10–25% per il personale senior.
- **Rivedi i ruoli periodicamente** — Man mano che il tuo team cresce, ispeziona le assegnazioni dei ruoli per assicurarti che il personale abbia l'accesso minimo necessario per il loro lavoro. Rimuovi i ruoli quando le persone cambiano posizione.
- **Abilita 2FA per i ruoli sensibili** — Il personale con accesso ai pagamenti, alle impostazioni o alla gestione degli utenti dovrebbe avere l'autenticazione a due fattori abilitata per la sicurezza.