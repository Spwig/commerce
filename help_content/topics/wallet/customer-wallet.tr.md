---
title: Müşteri Cüzdanı
---

Müşteri cüzdanı, müşterilere gelecekteki siparişlerde harcayabilecekleri bir bakiye sağlayan bir mağaza kredisi sistemidir. Mağaza kredisi, iade işlemleri, referans ödülleri, promosyon kampanyaları veya ekibiniz tarafından yapılan el ile ayarlamalar sonucu eklenebilir. Müşteriler, ödeme sırasında cüzdan bakiyelerini uygulayarak ödemelerini azaltabilirler.

**Müşteriler > Müşteri Cüzdanları** menüsüne giderek cüzdanları görüntüleyebilir ve yönetebilirsiniz.

## Cüzdan bakiyelerini anlama

Her müşteri cüzdanı dört bakiye rakamını gösterir:

| Bakiye | Açıklama |
|---|---|
| **Kullanılabilir Bakiye** | Müşterinin şu anda ödeme sırasında harcayabileceği miktar |
| **Bekleyen Bakiye** | Henüz harcayamayacağınız krediler — örneğin, onay penceresi içinde olan bir iade |
| **Toplam Kredili Bakiye** | Bu cüzdana asla kredili olan toplam miktar, geçmiş tüm krediler dahil |
| **Toplam Kullanılan** | Müşterinin tüm siparişlerden cüzdanından harcadığı toplam miktar |

Ödeme sırasında sadece kullanılabilir bakiye önemli olur. Bekleyen krediler, bekleyen dönem sona erdiğinde kullanıma açılır.

## Müşteri cüzdanını görüntüleme

1. **Müşteriler > Müşteri Cüzdanları** menüsüne gidin
2. Ad ya da e-posta ile müşteri aramak için arama alanını kullanın
3. Cüzdan girdisine tıklayarak detaylı görünümü açın

Detaylı görünüm, üstte mevcut bakiyeleri ve altta tam bir işlem geçmişini gösterir. **Son Kredili Bakiye** ve **Son Kullanılan Bakiye** zaman damgaları, cüzdanın son aktif olduğu zamanı gösterir.

### Cüzdan listesini filtreleme

**Aktif** filtresini kullanarak canlı cüzdanları donmuş olanlardan ayırabilirsiniz. Bir cüzdan, aktif olarak işaretlenmiş olsa bile pozitif bir bakiye varsa ödeme sırasında kullanılamaz.

## İşlem geçmişini okuma

Her cüzdan bakiyesindeki değişiklik, bireysel bir işlem olarak kaydedilir. İşlem geçmişi, tam ve kalıcı bir defterdir — işlemler hiçbir zaman düzenlenmez veya silinmez. Bir hata düzeltilmesi gerekiyorsa, bunun yerine yeni bir dengeleyici işlem eklenir.

Her işlem şu alanları gösterir:

| Alan | Açıklama |
|---|---|
| **Tip** | Kredi, Debit, Iade, Ayarlama veya Geri Alım |
| **Miktar** | Bu işlemin değeri (her zaman pozitif bir sayı olarak gösterilir) |
| **İşlem Sonrası Bakiye** | Bu işlem uygulandıktan hemen sonra cüzdan bakiyesi |
| **Kaynak** | Kredi veya debiti başlatan yer |
| **Durum** | Tamamlandı, Bekliyor veya Geri Alındı |
| **Açıklama** | İşlemin kısa açıklaması |
| **Referans Kimliği** | Kaynak kaydı (örneğin, bir sipariş numarası veya ödül kimliği) ile bağlantı kuran bir bağlantı |
| **Oluşturulma Zamanı** | İşlem kaydedildiğinde |

### İşlem türlerini anlama

- **Kredi** — cüzdana eklenen fonlar (iade, promosyon veya el ile ayarlama sonucu)
- **Debit** — ödeme sırasında harcanan fonlar
- **Iade** — iade veya iptal edilen bir sipariş sonucu olarak özel olarak eklenen kredi
- **Ayarlama** — ekibiniz tarafından yapılan el ile düzeltme
- **Geri Alım** — daha önceki bir girdiyi iptal eden bir işlem

### İşlem kaynaklarını anlama

- **Sipariş Iadesi** — bir sipariş iade edildiğinde cüzdana verilen kredi
- **Referans Ödülü** — referans programı aracılığıyla kazanılan kredi
- **Promosyon** — pazarlama kampanyası kapsamında verilen kredi
- **El ile Ayarlama** — bir personel tarafından doğrudan eklenebilen veya kaldırılabilecek kredi
- **Sipariş Ödemesi** — bir sipariş için ödeme sırasında harcanan fonlar

## El ile cüzdan ayarlamaları

Cüzdan detay görünümünden doğrudan fon ekleyemez veya kaldırılamaz — cüzdan işlemleri, ilgili süreçler aracılığıyla (iade, ödüller, promosyonlar) oluşturulur. Ancak, uygun izinlere sahip personel, **Cüzdan İşlemleri** bölümü üzerinden el ile ayarlama işlemleri oluşturabilir.

**Müşteriler > Cüzdan İşlemleri** menüsüne gidin ve bir cüzdan kredisi başka bir kaynakla uyuşmuyorsa (örneğin, hizmet şikayetinden sonra iyi niyet kredisi) bir cüzdan işlemi uygulamak istiyorsanız **+ Cüzdan İşlemi Ekle** kullanın.

El ile ayarlama oluştururken:

1.

Ayarlamak istediğiniz **Cüzdan**ı seçin (müşteri e-postası ile arama yapın)
2.


Set **Transaction Type** to `Adjustment`
3.

Set **Source** to `Manual Adjustment`
4.

Enter the **Amount** — always a positive number regardless of direction
5.

Set the **Status** to `Completed` for an immediate credit
6.

Add a clear **Description** explaining the reason — this is visible in the transaction history
7.

Click **Save**

> **Note:** Because wallet transactions are immutable, double-check the amount and wallet before saving. If you make a mistake, you will need to create a reversal transaction to correct it.

## Freezing a wallet

If you need to prevent a customer from using their wallet balance — for example, during a fraud investigation — you can deactivate it without deleting it or removing the balance.

1. Open the customer's wallet detail view
2. Uncheck the **Active** toggle
3. Click **Save**

The balance is preserved and the wallet can be reactivated at any time. While inactive, the customer cannot apply the wallet balance at checkout.

## Viewing all transactions

For a store-wide view of wallet activity, navigate to **Customers > Wallet Transactions**. This list shows every transaction across all customer wallets, with filters for:

- **Transaction Type** — filter by credit, debit, adjustment, etc.
- **Source** — filter by where transactions originated
- **Status** — filter by completed, pending, or reversed
- **Date** — use the date hierarchy at the top to drill into a specific day, month, or year

The transaction list is read-only — transactions cannot be edited or deleted from this view.

## Tips

- Check **Lifetime Credited** versus **Lifetime Used** to understand how actively a customer uses their store credit — a large unused balance may indicate the customer has forgotten it exists
- If a customer reports their balance looks wrong, review the full transaction history to trace exactly how the balance changed over time; the **Balance After** column on each entry makes this easy
- Use wallet credits as a customer retention tool — a goodwill credit after a difficult order experience can cost less than a refund while keeping the customer spending in your store
- Frozen wallets retain their balance permanently; there is no expiry — if you deactivate a wallet temporarily, remember to reactivate it when the issue is resolved
- The **Reference ID** on each transaction links back to the originating record, making it straightforward to verify why a credit or debit was applied without having to search elsewhere