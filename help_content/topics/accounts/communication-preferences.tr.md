---
title: İletişim Tercihleri
---

İletişim tercihleri, müşterilerin mağazanızdan hangi e-posta ve SMS mesajlarını alacaklarını kontrol etmelerine olanak tanır. Bu sistem, GDPR uyumluluğunu sağlar ve tüm kanallarda müşteri iletişim tercihlerine saygı göstermenize yardımcı olur.

Müşteri iletişim tercihlerini yönetmek için yönetim paneli kenar çubuğunda **Müşteriler > İletişim Tercihleri** bölümüne gidin.

## İletişim Tercihlerini Anlama

İletişim tercihleri sistemi, müşterilerin aldıkları mesajlar üzerinde ince ayar kontrolü sağlar. Bu şunları içerir:

- **İşlem e-postaları** — Temel sipariş onayları, kargo güncellemeleri, hesap güvenliği e-postaları (her zaman açık)
- **Pazarlama e-postaları** — Bültenler, promosyonlar, ürün önerileri (opt-in gerektirir)
- **Uygulama özel bildirimleri** — Blog yazıları, sadakat puanları, referans ödülleri, komisyonlar
- **SMS bildirimleri** — Metin mesajı bildirimleri (TCPA'ya göre açık opt-in gerektirir)

Tüm pazarlama iletişimleri, GDPR uyumluluğunu sağlamak için müşteri onayı ve e-posta doğrulaması gerektirir.

## Tercih Türleri Açıklaması

### İşlem İletişimleri (Her Zaman Etkin)

İşlem mesajları, müşterinizin hesabı ve siparişleri için temel öneme sahiptir. Bunları müşteriler **kapatamaz**:

| Tür | Açıklama | Örnekler |
|------|-------------|----------|
| **Sipariş Onayları** | Sipariş verildiğinde onay | Sipariş #12345 alındı |
| **Kargo Güncellemeleri** | Sipariş durumu değiştiğinde bildirimler | Siparişiniz kargoya verildi |
| **Ödeme Onayları** | Ödeme alındı, iade işlendi | 49,99 $ tutarındaki ödeme onaylandı |
| **Hesap Güvenliği** | Şifre sıfırlama, e-posta doğrulama | Şifrenizi sıfırlayın |

### Pazarlama İletişimleri (Opt-In Gerektirir)

Pazarlama mesajları müşteri onayı ve e-posta doğrulaması gerektirir:

| Tür | Açıklama | Varsayılan |
|------|-------------|---------|
| **Bülten** | Genel bültenler ve güncellemeler | Opt-out |
| **Promosyonel Fırsatlar** | İndirimler, kampanyalar, özel teklifler | Opt-out |
| **Ürün Önerileri** | Kişiselleştirilmiş ürün önerileri | Opt-out |
| **Stokta Var** | Ürünler geri geldiğinde bildirimler | Opt-out |

Müşteriler, herhangi bir pazarlama e-postası almadan önce **e-posta adreslerini doğrulamalıdır** (GDPR çift opt-in gereksinimi).

### Uygulama Özel Tercihleri

Müşteriler, belirli özelliklerden gelen bildirimleri kontrol edebilir:

**Blog Bildirimleri**
- Yeni blog yazısı yayımlandı (anında, haftalık özet veya aylık özet)
- Kategori bazlı abonelikler
- Sıklık tercihleri

**Sadakat Programı**
- Kazanılan puan bildirimleri
- Seviye yükseltmeleri
- Açılan ödüller
- Yakında sona erecek puanlar
- Doğum günü bonusları
- Kampanya teklifleri

**Referans Programı**
- Ödül verildi (referans veren ve referans edilen)
- Başarılı referans kaydı
- Yakında sona erecek ödül
- Referans davetleri

**Ortaklık Programı**
- Kazanılan komisyon
- Onaylanan veya reddedilen komisyon
- İşlenen, tamamlanan veya başarısız olan ödeme
- Aylık performans raporları

### SMS Bildirimleri (Açık Opt-In Gerektirir)

Tüm SMS bildirimleri, TCPA düzenlemelerine göre **açık opt-in** gerektirir. Müşteriler, SMS opt-in kutusunu aktif olarak işaretlemelidir:

- **İşlem SMS** — Kargoya verildi, teslim edildi (opt-in gerektirir)
- **Pazarlama SMS** — Promosyonlar, özel teklifler (ayrı opt-in gerektirir)

İstenmeyen metin mesajlarının gönderilmesinin e-postadan daha sıkı düzenlenmesi nedeniyle, işlem SMS'leri bile opt-in gerektirir.

## Yönetim Panelinde Müşteri Tercihlerini Yönetme

### Tüm Tercihleri Görüntüleme

Tüm müşteri tercihlerini görmek için **Müşteriler > İletişim Tercihleri** bölümüne gidin:

{
  "Column": "Açıklama",
  "--------": "-------------",
  "**Kullanıcı E-posta Adresi**": "Müşterinin e-posta adresi (kullanıcı admin'ine bağlantı)",
  "**E-posta Durumu**": "E-posta etkinse yeşil ✓, devre dışıysa gri ○",
  "**SMS Durumu**": "SMS etkinse yeşil ✓, devre dışıysa gri ○",
  "**Pazarlama Durumu**": "'Katıldı' ya da 'Katılmadı' etiketi",
  "**Doğrulama Durumu**": "E-posta doğrulanmışsa 📧✓, SMS doğrulanmışsa 📱✓",
  "**Rıza Kaynağı**": "Müşterinin rıza gösterdiği yer (kayıt, ödeme, tercih merkezi)",
  "**Güncelleme Zamanı**": "Tercihlerin değiştirildiği son zaman"
}

### Tercihleri Filtreleme

Filtre kenar çubuğunu kullanarak müşteri bulun:

- **E-posta Etkin** — Evet/Hayır
- **SMS Etkin** — Evet/Hayır
- **E-posta Pazarlama** — Evet/Hayır (pazarlamaya katıldı)
- **SMS Pazarlama** — Evet/Hayır (SMS pazarlamasına katıldı)
- **E-posta Doğrulandı** — Evet/Hayır (e-posta adresini doğruladı)
- **SMS Doğrulandı** — Evet/Hayır (telefon numarasını doğruladı)
- **Rıza Kaynağı** — Kayıt, Ödeme, Tercih Merkezi, API, Taşıma
- **Dil Kodu** — İletişim için tercih edilen dil

### Tercihleri Ara

Aşağıdakileri kullanarak müşteri ara:
- Kullanıcı e-posta adresi
- Kullanıcı adı
- Ad
- Soyad
- İptal token'ı

### Toplu Eylemler

Çoklu müşteri seçip toplu eylemleri uygula:

**✓ E-postayı Doğrula**
- Kullanıcı e-posta adreslerini manuel olarak doğrula
- Başka bir sistemden müşteri aktarıldığında yararlıdır
- Tercih önbelleğini geçersiz kılarak değişiklikleri hemen uygula

**🚫 Tüm Pazarlamadan İptal Et**
- Tüm pazarlama iletilerini (e-posta, SMS, tüm uygulamalar) devre dışı bırakır
- İşlemli e-postaları devre dışı bırakmaz
- İstekleri olan müşteriler için kullanılır
- GDPR'e göre rızanın geri alınmasına saygı gösterir

**📥 Tercihleri CSV'ye Aktar**
- Müşteri tercihlerini tablo belgesine aktar
- Tüm tercih alanlarını ve uygulama özel ayarlarını içerir
- Uyumluluk denetimleri ve analizleri için yararlıdır
- Biçim: Başlıklarla birlikte CSV

## Müşteri Kendi Tercih Merkezini Yönetme

Kullanıcı girişi yaparken /accounts/preferences/ adresinde kendi tercihlerini yönetebilir.

### Tercih Merkezi Özellikleri

**Hızlı Eylemler**
- **Tüm Pazarlamaya Abone Ol** — Tek tıkla tüm pazarlama iletilerini etkinleştir
- **Tümünden İptal Et** — Tüm pazarlama iletilerini devre dışı bırak (işlemli e-postalar devam eder)

**Tercih Kartları**
- **İşlemli E-Postalar** — Okunur (her zaman etkin, "Gerekli" olarak işaretlenir)
- **Pazarlama İletileri** — Doğrulama etiketi ile aç/kapat
- **Blog Tercihleri** — Etkin/etkisiz, sıklığı seç (anında, haftalık, aylık)
- **Loyalty Programı** — Bireysel bildirim türlerini etkin/etkisiz
- **İlan Programı** — Ödül bildirimlerini etkin/etkisiz
- **Cari Programı** — Komisyon ve ödeme bildirimlerini etkin/etkisiz
- **SMS Bildirimleri** — SMS'e katılmak/etmemek (doğrulama durumunu gösterir)

**Ani Güncellemeler**
- AJAX ile anında kaydeder
- Sayfa yeniden yüklenebilir gerekmez
- Kaydolduğunda görsel geri bildirim

### E-posta Doğrulama Süreci

Bir müşteri pazarlama e-postalarını etkinleştirirse:

1. Müşteri, "Pazarlama E-Postaları" nı AÇIKA ALIR
2. Sistem, benzersiz bir bağlantı ile doğrulama e-postası gönderir
3. Müşteri doğrulama bağlantısına tıklar
4. E-posta doğrulanmış olarak işaretlenir (📧✓ etiketi görünür)
5. Pazarlama e-postaları şimdiden gönderilmeye başlar

**Doğrulanmamış müşteriler**, ayarlar açık olsa bile pazarlama e-postalarını almayacaktır. Bu, GDPR çift onay uygulamasına uygunluk sağlar.

## Tek Tıkla İptal Etme

Tüm pazarlama e-postaları, alt kısmında bir iptal bağlantısı içerir. Bu bağlantıyı tıklayarak:

1. /accounts/unsubscribe/<token>/ adresine gider (oturum gerekmez)
2. Neye iptal ettiğinizi gösterir
3. Opsiyonel geri bildirim (iptal nedeni)
4. Pazarlama iletilerini devre dışı bırakır
5. İşlemli e-postaları devre dışı bırakmaz
6. Tam tercih merkezine link sağlar

Müşteriler, tercih merkezinden herhangi bir zaman tekrar abone olabilir.

## Uyumluluk ve Hukuki Gereklilikler

### GDPR 7. Maddesi Uygunluğu

Sistem, tam olarak GDPR 7. maddesi uygunluğunu sağlar:

Tüm markdown formatlamasını, resim yollarını, kod bloklarını ve teknik terimleri koruyun.

**✅ Onam Kanıtı**
- Onamın verildiği zaman damgası
- Onam kaynağı (kayıt, ödeme, tercih merkezi)
- Onamın IP adresi
- Kullanıcı ajanı (tarayıcı bilgisi)

**✅ Ayrı Onam**
- Pazarlama ve işlem e-postaları ayrı anahtarlar olarak yönetilir
- Her uygulama (blog, sadakat vb.) için ayrı onam gereklidir

**✅ Kolay Çekilme**
- Tüm pazarlama e-postalarında tek tıkla abonelikten çıkma
- Tüm oturum açan müşteriler için tercih merkezi mevcut
- Abonelikten çıkma anında geçerli olur

**✅ Serbestçe Verilen Onam**
- Pazarlama için varsayılan ayar opt-out'tur (GDPR en iyi uygulama)
- Ön işaretli kutular yok (müşteriler aktif olarak opt-in yapmalıdır)

**✅ Spesifik ve Bilgilendirilmiş Onam**
- Her tercihin neyi kontrol ettiğine dair açık açıklamalar
- İnce ayarlı uygulama düzeyinde tercihler (hepsi veya hiç değil)

**✅ Doğrulanabilir Onam**
- Pazarlama e-postaları için çift opt-in
- EmailOutbox durum takibi ile denetim izi

### TCPA Uyumluluğu (ABD SMS Düzenlemeleri)

Tüm SMS bildirimleri **açık opt-in** gerektirir:

- Müşteriler SMS opt-in kutusunu aktif olarak işaretlemelidir
- Ön işaretli kutulara izin verilmez
- Ne için opt-in yaptıklarına dair açık açıklama
- Tercih merkezi üzerinden kolay opt-out
- Uyumluluk denetimi için tüm SMS gönderimleri kaydedilir

### CAN-SPAM Uyumluluğu (ABD E-posta Düzenlemeleri)

Sistem CAN-SPAM uyumluluğunu sağlar:

- Her pazarlama e-postasında abonelikten çıkma bağlantısı
- Abonelikten çıkma anında işlenir (10 iş günü içinde yapılması gerekir, biz anında yapıyoruz)
- Açık "From" adı (mağazanızın adı)
- E-posta altbilgisinde fiziksel adres
- Yanıltıcı konu satırları yok

## EmailOutbox'ta E-posta Durumunu Anlama

**E-posta Sistemi > E-posta Gönderi Kutusu**'nu görüntülerken, tercihlerin e-posta teslimatını nasıl etkilediğini görebilirsiniz:

| Durum | Anlam | Neden |
|--------|---------|--------|
| **Beklemede** | Gönderim için kuyruğa alındı | Tercihler bu e-postaya izin veriyor |
| **Kuyrukta** | Gönderim kuyruğunda | Tercihler bu e-postaya izin veriyor |
| **Atlandı** | E-posta gönderilmedi | Müşteri tercihi devre dışı |
| **Gönderildi** | Başarıyla teslim edildi | E-posta normal şekilde gönderildi |

Bir e-posta **atlandığında**, `skip_reason` alanı nedenini gösterir:

- **user_preference_disabled** — Müşteri bu e-posta türünü tercihlerde devre dışı bıraktı
- **email_not_verified** — Müşteri e-posta adresini doğrulamadı
- **email_disabled** — Müşteri tüm e-postaları devre dışı bıraktı (ana anahtar)

Bu denetim izi GDPR uyumluluğu için önemlidir — müşteri tercihlerine saygı gösterdiğinizi kanıtlayabilirsiniz.

## Tercihler İçin Site Ayarları

Küresel tercih varsayılanlarını yapılandırmak için **Ayarlar > Site Ayarları**'na gidin:

**Pazarlama E-postaları İçin Çift Opt-In'i Etkinleştir** (Varsayılan: Evet)
- Pazarlama e-postaları göndermeden önce e-posta doğrulaması gerektirir
- GDPR en iyi uygulama
- Önerilen: Etkin bırakın

**Varsayılan Pazarlama Opt-In Durumu** (Varsayılan: Hayır - Opt-Out)
- Yeni müşteriler kayıt olduğunda varsayılan durum
- GDPR varsayılan olarak opt-out gerektirir
- Önerilen: Opt-out olarak bırakın (False)

**Tercih Merkezi Etkin** (Varsayılan: Evet)
- Müşterilerin kendi tercihlerini yönetmesine izin verir
- GDPR'deki onamı geri çekme hakkı için gereklidir
- Önerilen: Etkin bırakın

**SMS Doğrulaması Gerektir** (Varsayılan: Hayır)
- SMS bildirimleri için telefon numarası doğrulaması gerektirir
- İsteğe bağlıdır ancak yüksek hacimli SMS göndericileri için önerilir
- SMS için çift opt-in istiyorsanız etkinleştirilebilir

**Abonelikten Çıkma Nedenlerini Göster** (Varsayılan: Evet)
- Müşteriler abonelikten çıktığında isteğe bağlı geri bildirim toplanır
- Müşterilerin neden opt-out yaptığını anlamaya yardımcı olur
- Önerilen: İçgörü için etkin bırakın

## En İyi Uygulamalar

### 1. Pazarlama İçin Varsayılan Olarak Opt-Out

Pazarlama iletişimini her zaman varsayılan olarak **opt-out** (işaretlenmemiş) yapın:
- GDPR'a uyumlu
- Müşterilerle güven inşa eder
- Spam şikayetlerini azaltır
- Yalnızca etkileşimde bulunan müşterilere gönderin

### 2. E-posta Doğrulaması Gerektirin

**Çift Opt-In**'i etkin tutun:
- E-posta adreslerinin geçerli olduğunu sağlar
- Müşterinin gerçekten pazarlama e-postaları istediğini doğrular
- Dönme oranını azaltır
- GDPR uyumluluğu için gereklidir

### 3. Tercihlere Anında Saygı Gösterin

Tüm markdown biçimlendirmesini, görsel yollarını, kod bloklarını ve teknik terimleri koruyun. /no_think

Müşteri tercihlerini değiştirdiğinde:
- Değişiklikler anında geçerli olur
- Tercih önbelleği geçersiz hale gelir
- Bir sonraki e-posta gönderimi güncellenmiş tercihleri kontrol eder
- İptal isteklerinin hiçbir gecikme olmadan yerine getirilmesi gerekir

### 4. E-Posta Atlamalarını İzle

Düzenli olarak **E-Posta Gelen Kutusu**'nda atlanan e-postaları kontrol edin:
- Yüksek atma oranı, müşterilerin tercih etmediklerini gösterir
- E-posta içeriğinin geliştirilmesi gerektiğini gösterebilir
- Tercih sorunlarını belirlemeye yardımcı olur

### 5. Düzenli Uyumluluk Denetimleri

Daha fazla uyumluluk için tercihleri periyodik olarak dışa aktarın:
1. **İletişim Tercihleri**'ne gidin
2. Tüm müşterileri seçin
3. **Tercihleri CSV'ye Dışa Aktar** seçeneğini seçin
4. GDPR denetimi için kaydedin

GDPR veri saklama gerekliliklerine uyum sağlamak için dışarı aktarmaları **en az 3 yıl** saklayın.

### 6. Net İletişim

Rıza toplarken:
- Yargısal jargon yerine basit dil kullanın
- Müşterilerin ne alacağını açıklayın
- Sıklığı gösterin (günlük, haftalık, aylık)
- Rıza kutularını dikkat çekici ama önceden işaretli olmayan şekilde gösterin

### 7. Tercihlere Göre Segmentleme

Pazarlama kampanyaları gönderirken:
- Sadece doğrulanmış, rıza edilmiş müşterilere gönderin
- Uygulama özel tercihlerine saygı gösterin (blog e-postalarını blogu kapatmış müşterilere göndermeyin)
- Sıklık tercihlerine uygun olarak gönderin (haftalık özeti alıcılarına anlık e-posta göndermeyin)

## İpuçları

**💡 Göndermeden Önce Tercihi Kontrol Et**

Sistemin, `EmailSendingService.send_template_email()` kullanarak e-posta gönderirken tercihleri otomatik olarak kontrol ettiği doğrudur. Tüm e-posta gönderilerinin doğrudan SMTP çağrıları yerine bu hizmeti kullandığından emin olun.

**💡 Atlanan Durum Normaldir**

Müşteri tercihlerini yerine getirdiği için sistem çalışan bir durumdur. İstisnai e-postaları atlamak, GDPR cezalarına veya spam şikâyetlerine maruz kalmaktan daha iyidir.

**💡 Tercih Önbelleği 5 Dakikadır**

Tercih kontrolü performans için 5 dakika önbelleğe alınır. Müşteriler tercih merkezinden veya yönetici eylemlerinden tercihlerini değiştirdiğinde, değişiklikler hemen geçerli olacak şekilde önbellek hemen geçersiz hale gelir.

**💡 Misafir Müşteriler Kontrollerden Kaçınır**

Hesap sahibi olmayan müşteri (hesap yok) normalde tüm e-postaları alır çünkü tercih kayıtları yoktur. Bu amaçladır — e-posta adresini ödeme anında vermişlerdir.

**💡 İşlemci E-Postaları Her Zaman Gönderilir**

Sipariş onayları, kargo güncellemeleri ve hesap güvenliği e-postaları **her zaman gönderilir** tercihlere bakılmaksızın. Müşterilerin siparişleri ve hesapları hakkında kritik bilgilere erişmelerini sağlar.

**💡 Toplu Eylemleri Dikkatli Kullanın**

"Tüm Pazarlama’dan İptal Et" toplu eylemi, **tüm uygulamaları** (blog, sadakat, öneriler, ortaklık) etkiler. Bu eylemi, açıkça tümünden ayrılmak isteyen müşteriler için kullanın. Belirli tercihler için, bireysel müşteri kayıtlarını düzenleyin.

**💡 Uyumluluk için Denetim İzni**

Sistem şunları izler:
- Rıza zaman damgası ve kaynağı
- IP adresi ve kullanıcı aracı
- E-posta doğrulama zaman damgası
- E-Posta Gelen Kutusu'ndaki atma durumu aracılığıyla her tercih değişikliği

Yetkililerin herhangi bir zaman rıza kanıtını istemesi durumunda GDPR uyumluluğunu kanıtlar.

## İlgili Konular

- [Müşteri Hesaplarını Yönetme](/help/managing-customer-accounts) — Müşteri profil yönetimi
- [E-Posta Yapılandırması](/help/email-configuration) — SMTP kurulumu ve e-posta kalıpları