---
title: Esempi di Buoni
---

This guide provides concrete, field-by-field examples for the most common voucher types. Each example shows exactly what to enter when creating a voucher at **Marketing > Vouchers** → **+ Add Voucher**.

![Voucher Card](/static/core/admin/img/help/voucher-examples/voucher-card.webp)

## Example 1: Percentage Off with Discount Cap

**Scenario:** Offer 20% off the entire cart, but cap the discount at $50 so high-value orders stay profitable. No expiry date.

| Field | Value |
|-------|-------|
| Code | `SAVE20` |
| Name | 20% Off — Max $50 |
| Discount Type | Percentage |
| Discount Value | 20 |
| Max Discount Amount | 50 |
| Application Scope | Entire Cart |
| Max Uses Total | *(empty — unlimited)* |
| Max Uses Per Customer | 1 |
| Min Order Value | *(empty — no minimum)* |

**How the cap works:** On a $200 order the discount is $40. On a $300 order it would be $60, but the cap limits it to $50. On a $500 order the discount is still $50. This lets you run a generous-sounding promotion while keeping the actual discount predictable.

## Example 2: Fixed Amount Off with Minimum

**Scenario:** Give customers $10 off any order over $75 to encourage larger carts.

| Field | Value |
|-------|-------|
| Code | `TAKE10` |
| Name | $10 Off Orders Over $75 |
| Discount Type | Fixed Amount |
| Discount Value | 10 |
| Application Scope | Entire Cart |
| Min Order Value | 75 |
| Max Uses Per Customer | 0 *(unlimited)* |
| End Date | *(empty — no expiry)* |

> **Note:** Setting a minimum order value protects your margins. Without it, a customer could use this code on a $12 order and wipe out your profit. Always pair fixed-amount vouchers with a sensible minimum.

## Example 3: Free Shipping

**Scenario:** Offer free shipping on any order with no minimum spend.

| Field | Value |
|-------|-------|
| Code | `FREESHIP` |
| Name | Free Shipping |
| Discount Type | Free Shipping |
| Application Scope | Entire Cart |
| Max Uses Total | *(empty — unlimited)* |
| Max Uses Per Customer | 1 |
| Min Order Value | *(empty — no minimum)* |

> **Note:** Select the **Free Shipping** discount type, which removes shipping charges from the order automatically. This is the cleanest approach and works regardless of which shipping method the customer selects.

## Example 4: First-Time Customer Welcome Code

**Scenario:** Give new customers 15% off their first order to encourage conversion.

| Field | Value |
|-------|-------|
| Code | `WELCOME15` |
| Name | Welcome — 15% Off First Order |
| Discount Type | Percentage |
| Discount Value | 15 |
| Application Scope | Entire Cart |
| Max Uses Per Customer | 1 |
| First Time Customers Only | Checked |

The system validates first-time status by checking whether the customer has any previous completed orders. If a customer with order history tries to apply this code, they see a clear error message at checkout.

## Example 5: Product-Specific Voucher

**Scenario:** Offer $5 off selected products — for example, to move slow-selling inventory.

| Field | Value |
|-------|-------|
| Code | `PICK5` |
| Name | $5 Off Selected Items |
| Discount Type | Fixed Amount |
| Discount Value | 5 |
| Application Scope | Specific Products |
| Eligible Products | *(select the target products)* |
| Max Uses Per Customer | 1 |

> **Note:** Use product scope when you want to discount individual SKUs. Use category scope (next example) when you want to discount everything in a department. Product scope gives you precise control; category scope is easier to maintain when your catalog changes frequently.

## Example 6: Category Voucher

**Scenario:** Run a 25% off promotion on all items in the Electronics category.

| Field | Value |
|-------|-------|
| Code | `ELEC25` |
| Name | 25% Off Electronics |
| Discount Type | Percentage |
| Discount Value | 25 |
| Application Scope | Specific Categories |
| Eligible Categories | Electronics |
| Max Uses Total | *(empty — unlimited)* |
| Max Uses Per Customer | 1 |

Quando applicato a una categoria, lo sconto si applica solo agli articoli idonei nel carrello.

Gli articoli non elettronici vengono addebitati al prezzo pieno.

## Confronto dei tipi di sconto

| Tipo | Funzionamento | Migliore per | Esempio |
|------|-------------|----------|---------|
| **Percentuale** | Deduce una percentuale del totale idoneo | Sconti che crescono con la dimensione dell'ordine | 20% di sconto su tutto il carrello |
| **Importo fisso** | Deduce un importo fisso in dollari | Promozioni semplici e prevedibili | $10 di sconto su ordini superiori a $75 |
| **Spedizione gratuita** | Rimuove le spese di spedizione dall'ordine | Ridurre l'abbandono del carrello al checkout | Spedizione gratuita, senza minimo |

## Confronto delle porte

| Portata | Funzionamento | Migliore per |
|-------|-------------|----------|
| **Intero carrello** | Lo sconto si applica al totale completo dell'ordine | Promozioni a livello aziendale e codici di benvenuto |
| **Prodotti specifici** | Lo sconto si applica solo ai prodotti selezionati nel carrello | Smaltire inventario specifico o promozioni di prodotti in evidenza |
| **Categorie specifiche** | Lo sconto si applica solo agli articoli delle categorie selezionate | Vendite a livello di reparto e promozioni stagionali |

## Consigli

- **Utilizza codici memorabili** — `SUMMER20` si converte meglio rispetto a `COUPONX1600406498`. Riserva i codici generati automaticamente per le campagne di massa.
- **Testa prima di distribuire** — Effettua un ordine di test con il codice voucher per verificare che si applichi correttamente e rispetti tutti i limiti.
- **Monitora l'utilizzo** — Controlla il conteggio delle redemptions su ogni carta voucher per tracciare le prestazioni della campagna in tempo reale.
- **Combina con la barra di annuncio** — Promuovi il tuo codice voucher in un annuncio a livello del sito in modo che i clienti lo vedano prima di iniziare a fare shopping.