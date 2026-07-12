---
title: POS ile Başlangıç
---

<!-- screenshots-needed:
- url: /en/admin/pos/
  filename: getting-started-dashboard.webp
  description: POS dashboard as it appears on a fresh install with no terminals registered
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/pos/terminal-provider/wizard/step1/
  filename: getting-started-provider-wizard-step1.webp
  description: Payment provider wizard first step showing available provider options
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/catalog/warehouse/
  filename: getting-started-store-location.webp
  description: Warehouse list showing a store location with the POS toggle enabled
  save-to: core/static/core/admin/img/help/pos/
-->

Spwig POS, herhangi bir tablet ya da tarayıcıyı mağaza içi kasa olarak dönüştürür — ürün kataloğunuza, stoklarınıza ve sipariş geçmişinize bağlı. Bu kontrol listesi, yeni bir kurulumdan ilk satışınızı kaydetmeye kadar size rehberlik eder. Her adım, tam detayları görmek isterseniz özel bir konuya yönlendirir.

![POS Dashboard](/static/core/admin/img/help/pos/getting-started-dashboard.webp)

## Adım 1: Bir mağaza konumuna için POS'u etkinleştir

POS terminalleri fiziksel bir mağaza konumuna bağlıdır. Spwig'de, mağaza konumları, mağaza konumu olarak işaretlenmiş depolar olarak tanımlanır.

1. Yönetici menüsünden **Catalog > Warehouses**'a gidin.
2. Kullanmak istediğiniz depoyu açın veya yeni bir tane oluşturun.
3. **Retail location** (Mağaza konumu) anahtarını işaretleyin ve bir **POS display name** (örneğin, "High Street Store") girin. Bu isim, faturalar ve terminaller seçici üzerinde görünür.
4. Depoyu kaydedin.

Birden fazla mağaza ya da bölgesel raporlama için gruplamak istiyorsanız, önce **POS > Store Groups**'da bir **Store Group** (Mağaza Grubu) oluşturun, ardından her depoyu bu gruba atayın. Mağaza grupları, gruptaki tüm konumların ortak para birimi, saat dilimi ve fatura şablonunu ayarlamaya olanak tanır.

## Adım 2: En az bir POS erişimine sahip çalışan hesabı oluşturun veya doğrulayın

Çalışanlar, Spwig yönetici paneline giriş yapmak için kullandıkları aynı kimlik bilgilerini kullanarak POS'a giriş yapar. **Active** durumunda olan ve en az `pos_admin` iznine sahip olan herhangi bir çalışan hesabı POS'a erişebilir.

Erişimi kontrol etmek veya vermek için **Settings > Staff Management**'a gidin, çalışanın hesabını açın ve uygun POS rolünün atandığını doğrulayın. Ek bir POS hesabı gerekmez.

## Adım 3: İlk POS terminalinizi kaydedin

Bir terminal, tek bir kasa veya cihazı temsil eder. Onu yönetici panelinde kaydeder, ardından tek seferlik eşleştirme kodu kullanarak fiziksel bir cihazı ona bağlar.

1. **POS > POS Terminals**'a gidin ve **+ Add POS Terminal** (POS Terminali Ekle) butonuna tıklayın.
2. Terminal için bir isim verin (örneğin, "Front Register") ve Adım 1'de etkinleştirdiğiniz mağaza konumuna atayın.
3. Terminali kaydedin. Spwig, **8 karakterlik bir eşleştirme kodu** oluşturur — bunu terminalin detay sayfasında göreceksiniz.
4. Kullanmak istediğiniz cihazı bir kasa olarak kullanın, bir tarayıcı açın ve `/pos/` adresine gidin.
5. İstenirse eşleştirme kodunu girin. Cihaz artık bu terminalle bağlantılıdır.

Eşleştirme kodu tek seferlik kullanıma sahiptir. Bir cihazı yeniden eşleştirmek isterseniz, yönetici panelinde terminali açın ve **Regenerate pairing code** (Eşleştirme Kodunu Yeniden Oluştur) butonuna tıklayın.

Donanım yapılandırma seçenekleri (fatura yazıcı, barkod okuyucu, nakit çekme kasası) için [POS Terminal Setup](pos-terminal-setup) konusuna bakın.

## Adım 4: Ödeme sağlayıcısını yapılandırın

Ödeme sağlayıcısı, kart okuyucularınızı Stripe Terminal veya Square gibi bir ödeme ağına bağlar. 5 adımlık kurulum asistanını kullanarak kimlik bilgilerinizi girin.

1. **POS > Payment Providers**'a gidin ve **Configure provider** (Sağlayıcıyı Yapılandır) butonuna tıklayın.
2. Asistan, `/admin/pos/terminal-provider/wizard/step1/` adresinde açılır.

![Payment Provider Wizard](/static/core/admin/img/help/pos/getting-started-provider-wizard-step1.webp)

3. Sağlayıcınızı (örneğin, **Stripe Terminal**) seçin ve ekrandaki talimatları beş adımdan geçerek takip edin: sağlayıcı seçme → kurulum talimatları → kimlik bilgilerini girme → bağlantı testi → konum yapılandırması.
4. **Connected** (Bağlantılı) olan yeşil bir badge, entegrasyonun canlı olduğunu onaylar.

Sadece nakit ve el ile kart girişi gerekirse, sağlayıcı olarak **Manual**'i seçin — kimlik bilgileri gerekmez.

Her desteklenen sağlayıcı için ayrıntılı kimlik bilgisi alanları için [POS Ödeme Sağlayıcısı Kurulumu](pos-payment-provider-setup) bölümüne bakın.

## Adım 5: Kart okuyucunu eşle

Ödeme sağlayıcısı bağlıysa, 3 adımlık okuyucu sihirbazını kullanarak fiziksel bir kart okuyucunu terminalinizden birine eşleyebilirsiniz.

1. **POS > Kart Okuyucuları**'na gidin ve **Okuyucu Ekle**'ye tıklayın.
2. Sihirbaz, `/admin/pos/reader/wizard/step1/` adresinden başlar.
3. Sağlayıcınızı seçin, ardından **Yeni Cihaz Kaydet** (okuyucunun ekranında görünen kodu girin) veya **Mevcut Cihazı Keşfet** (Spwig, sağlayıcıyla zaten kaydedilmiş okuyucuları alır) seçeneğini seçin.
4. Son adımda, Adım 3'te oluşturduğunuz terminali okuyucuya atayın.

Her terminal, bir atanan kart okuyucusunu destekler. Kart okuyucularını herhangi bir zamanda Kart Okuyucular listesinden yeniden atayabilirsiniz.

## Adım 6: Fatura tasarımı (birinci gün için isteğe bağlı)

Spwig, varsayılan bir fatura şablonunu otomatik olarak oluşturur. Onu değiştirmeden hemen satışa başlayabilirsiniz — varsayılan, mağazanızın adını, adresini, ayrıntılı satış bilgilerini, ödeme yöntemini ve "Satın alma için teşekkür ederiz!" alt bilgisini basar.

Özelleştirmeye hazırsanız, **POS > Fatura Şablonları**'na gidin. Seçenekler arasında logonuz, vergi kimlik numaranız, QR kod promosyonu, iade politikası ve kağıt genişliği (58mm veya 80mm termal yazıcılar için) yer alır. Mağaza başına veya mağaza grubu başına ayrı şablonlar oluşturabilirsiniz.

## Adım 7: İlk iş gününüzü açın

İş günleri, satışları hangi kişi işleştirdiğini ve çekerce ne kadar nakit olmalı olduğunu izler. Kasa görevlileri, POS cihazında iş günlerini açıp kapatır.

1. Eşlenmiş cihazda `/pos/` adresine gidin ve personel kimlik bilgilerinizle oturum açın.
2. Terminali ve mağaza konumunu seçin.
3. Spwig, **açılış nakit miktarını say** isteyerek size sorar — çekerce zaten ne kadar nakit olduğunu girin (çekerce boşsa `0` girin).
4. **İş Gününü Aç**'a tıklayın. Kasa artık satışa hazır hale gelir.

İş günleri, nakit hareketleri ve dengeleme raporları hakkında tam bir açıklama için [POS İş Günlerini Yönetme](pos-shifts) bölümüne bakın.

## Adım 8: İlk satışınızı kaydet

Bir iş günü açıkken satış yapmak oldukça basittir:

1. Ürünleri adı, barkod tarayarak veya kategorileri tarayarak sepete ekleyin.
2. Gerekirse bir indirim veya kupon kodu uygulayın.
3. **Ödeme**'ye tıklayarak ödeme işlemini başlatın. Ödeme yöntemini seçin (nakit, okuyucu aracılığıyla kart veya bölünmüş ödeme).
4. Kart ödemeleri için, okuyucu müşteriye kartı tıklamalarını veya takmalarını isteyerek uyarır.
5. Fatura otomatik olarak basılır (veya dijital fatura seçeneği gösterilir). Sipariş, gerçek zamanlı olarak sipariş geçmişinize kaydedilir.

## Adım 9: Gün sonunda iş gününü kapat

İş gününü kapatmak, kasayı kilitleyip dengeleme özeti oluşturur.

1. POS menüsünden **İş Gününü Kapat**'a tıklayın.
2. Çekerceki nakiti sayın ve istendiğinde toplamı girin.
3. Spwig, açılış nakit miktarına, nakit satışlara ve iş günü sırasında yapılan nakit hareketlerine dayalı beklenen nakiti hesaplar ve farkı size gösterir.
4. Kapatmak için onaylayın. İş raporu kaydedilir ve yönetici panelinizde **POS > İş Günleri** altında görünür.

Gün içinde çekerceki nakit kaldırıldığını veya eklenildiğini **nakit hareketleri** olarak kaydedin (iş menüsünden) — bu, dengelemenizi doğru tutar.

## İpuçları

- İş gününüzün ilk günü için Adım 1 ile Adım 5'i tamamlayın.

Adım 6 ile Adım 9, gün içinde yapılabilir.
- Güçlü ama hatılayabileceğiniz personel şifresi kullanın — POS personeli, kasada kendi kimlik bilgilerini girer, bu nedenle aşırı karmaşık şifreler onları yavaşlatır.
- Kart okuyucu çevrimiçi görünmüyorsa, Kart Okuyucular sayfasında **Okuyucuları Senkronize Et**'e tıklayarak sağlayıcınızdan en son durumu çekin.
- Meşgul ticari dönemden önce $0.01 test işlemiyle tam akışı test edin (iş gününü aç → satış → fatura → iş gününü kapat).
- POS, temel nakit satışlar için çevrimdışı çalışır.

Kart terminali ödemeleri, onaylamak için internet bağlantısı gerektirir.
- Bir mağaza konumunda birden fazla terminal olabilir — admin'de yeni bir terminal kaydı oluşturun ve farklı bir cihaza bağlayın.