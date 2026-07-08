---
title: SMS Sağlayıcı Kurulumu
---

SMS bildirimleri, müşterilerin siparişlerinin her aşamasında bilgilendirilmesini sağlar — onaylamadan teslime kadar. Mağazanızdan SMS veya WhatsApp mesajı göndermek için, SMS sağlayıcısı hesabınızı kimlik bilgilerinizle bağlamalısınız. Bağlandıktan sonra Spwig, tüm giden metin mesajlarını göndermek için bu hesabı kullanır.

**SMS Sistemi > SMS Sağlayıcı Hesapları**'na giderek SMS sağlayıcılarınızı yönetin.

![SMS sağlayıcı hesapları listesi](/static/core/admin/img/help/sms-setup/provider-list.webp)

## Bir SMS sağlayıcısı ekleme

İlk kez kurulum yapmak için önerilen **Kurulum Sihirbazı**'nı veya el ile formu kullanarak bir sağlayıcı ekleyebilirsiniz.

### Kurulum sihirbazını kullanma

1. **SMS Sistemi > SMS Sağlayıcı Hesapları**'na gidin
2. Araç çubuğundaki **Kurulum Sihirbazı**'nı tıklayın
3. Rehberli adımları takip edin:
   - **Adım 1**: Kullanılabilir sağlayıcılar listesinden sağlayıcınızı seçin
   - **Adım 2**: Sağlayıcınızın kimlik bilgilerini girin (API anahtarları, Hesap SID, vb.)
   - **Adım 3**: Gösterim adını ve varsayılan ayarları belirleyin, ardından kaydedin
4. Sihirbaz, kaydetmeden önce otomatik olarak bağlantıyı test eder

### El ile sağlayıcı ekleme

1. **SMS Sistemi > SMS Sağlayıcı Hesapları**'na gidin
2. Kullanılabilir SMS sağlayıcılarını keşfetmek için **Sağlayıcıları Göster**'a tıklayın veya doğrudan **+ SMS Sağlayıcı Hesabı Ekle**'ye tıklayın
3. **Sağlayıcı** alanından, SMS sağlayıcınızı aşağı açılan listeden seçin
4. Bir sağlayıcı seçtikten sonra, bu sağlayıcının gereksinimlerine göre kimlik bilgi alanları otomatik olarak görünür
5. Gerekli kimlik bilgi alanlarını doldurun (bu alanlar sağlayıcıya göre değişebilir — aşağıda yer alan yaygın sağlayıcılar için bölümlere bakın)
6. Bu hesabı tanımlamak için bir **Gösterim Adı** girin (örneğin, `Twilio — Ana`)
7. **Varsayılan Ayarları** belirleyin (aşağıdaki bölüme bakın)
8. **Kaydet**'e tıklayın

## Sağlayıcı kimlik bilgileri

### Twilio

| Alan | Nerede bulunur |
|-----|---------------|
| Hesap SID | Twilio Konsolu → Dashboard |
| Auth Token | Twilio Konsolu → Dashboard |
| From Number | E.164 formatında Twilio telefon numaranız (örneğin, `+15551234567`) |

### Diğer sağlayıcılar

Seçildiğinde, diğer yüklenmiş SMS sağlayıcı bileşenleri kendi özel kimlik bilgi alanlarını gösterir. Gerekli tam değerleri belirlemek için sağlayıcınızın belgelerine bakın — genellikle bir API anahtarı veya erişim tokenı ve bir gönderen tanımlayıcısı gerekir.

## Varsayılan ayarlar

Kimlik bilgilerini girdikten sonra, bu hesabın nasıl kullanılacağını yapılandırın:

- **Aktif** — bu hesabı etkinleştirin veya devre dışı bırakın. Varsayılan olarak ayarlanmış olsalar bile, etkin olmayan hesaplar hiçbir mesaj göndermez
- **Varsayılan SMS Hesabı** — işaretlendiğinde, mağazanızdaki tüm SMS bildirimleri bu hesabı kullanır. Aynı anda yalnızca bir hesap varsayılan SMS hesabı olabilir
- **Varsayılan WhatsApp Hesabı** — bu sağlayıcı WhatsApp'ı destekliyorsa (örneğin, Twilio WhatsApp Business API aracılığıyla), bu alanı işaretleyerek WhatsApp mesajları için varsayılan olarak kullanabilirsiniz

## Bağlantıyı test etme

Bir sağlayıcı hesabı kaydettikten sonra, kimlik bilgilerinin işe yarayıp yaramadığını test edin:

1. **SMS Sistemi > SMS Sağlayıcı Hesapları**'na gidin
2. Sağlayıcı hesabınızı açmak için üzerine tıklayın
3. **Bağlantıyı Test Et** butonuna tıklayın
4. Spwig, sağlayıcıya bir test isteği gönderir ve **Bağlantı Durumu** alanını günceller

| Durum | Anlamı |
|------|--------|
| Bağlandı | Kimlik bilgileri geçerlidir ve sağlayıcı erişilebilir |
| Bağlantı Başarısız | Kimlik bilgileri yanlış veya sağlayıcı erişilebilir değil |
| Test Edilmemiş | Bağlantı henüz test edilmemiş |

Test başarısız olursa, kimlik bilgilerinizi kontrol edin ve sağlayıcının dashboard'ında gerekli izinlerin olduğundan emin olun.

## Bağlantı durumu sütunu

SMS Sağlayıcı Hesapları listesi, her hesap için renk kodlu bir **Bağlantı** etiketi gösterir:

- **Bağlandı** (yeşil) — hesap çalışıyor
- **Bağlantı Başarısız** (kırmızı) — kimlik bilgileri başarısız oldu — güncelleyin
- **Test Edilmemiş** (gri) — hesap henüz test edilmemiş

## İpuçları

- İlk sağlayıcınız için **Kurulum Sihirbazı**'nı kullanın — her alan için size rehberlik eder ve kaydetmeden önce bağlantıyı test eder
- Aynı anda yalnızca bir hesap **Varsayılan SMS Hesabı** olabilir.

İkinci bir hesap eklerseniz ve varsayılan olarak işaretlerseniz, önceki varsayılan otomatik olarak kaldırılır
- Sağladıcınızın API kimlik bilgilerini güvenli bir yerde not alın.

Kimlik bilgileri değişirse, burada hemen güncelleyin, aksi takdirde bildirimler başarısız olur
- Etkin olmayan hesaplar listede kalır ancak gönderimde kullanılmaz — bunlar etkinleştirmeden yedek kimlik bilgileri tutmak için faydalıdır
- Çoğu sağlayıcı gönderilen her mesaj için ücret alır — sağlayıcınızın paneline girerek kullanım durumunu izleyin, böylece beklenmedik faturalar kaçınılabilir