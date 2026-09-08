---
title: Pazarlama Gönderim Alan Adı
---

# Pazarlama gönderim alan adı

Mağazanız iki çok farklı türde e-posta gönderir:

- **İşlemsel** — sipariş onayları, kargo güncellemeleri, şifre sıfırlamaları. Bunlar her zaman gelen kutusuna ulaşmalıdır.
- **Pazarlama** — bültenler, promosyonlar, sepet kurtarma, stokta geri bildirimleri.

Varsayılan olarak her ikisi de aynı gönderim kimliği altında gönderilir, bu da **tek bir gönderici itibarını paylaştıkları** anlamına gelir. Bir pazarlama kampanyası spam şikayetleri alırsa veya eski adreslere ulaşırsa, bu itibar düşer — ve sipariş onaylarınız ile şifre sıfırlamalarınız da spama düşmeye başlayabilir.

Bir **pazarlama gönderim alan adı** bunu düzeltir. Kendi alt alan adınızda (örneğin `news.yourstore.com`) ikinci bir gönderim kimliği kurar ve onu pazarlama için işaretlersiniz. Spwig ardından tüm kampanyaları bu kimlikten gönderir ve işlemsel e-postaları ana alan adınızda tutar. Kötü bir kampanya artık müşterilerinizin *almak zorunda olduğu* e-postaları olumsuz etkileyemez.

> Bu, kendi kendine barındırılan mağazalar için geçerlidir. Spwig barındırmalı planlarda, gönderim itibarı sizin adınıza yönetilir.

## Spwig hangi kimliği kullanacağını nasıl belirler

Bir pazarlama gönderim hesabı oluşturulduğunda, yönlendirme otomatiktir — hiçbir şeyi etiketlemenize gerek yoktur:

- **Pazarlama e-postaları** (kampanyalar, yolculuklar, bültenler, sepet kurtarma, stokta geri bildirimleri) →
  pazarlama gönderim alan adı.
- **İşlemsel e-postalar** (siparişler, kargo, şifre sıfırlamaları, doğrulama) → ana
  alan adınız.

Hiçbir zaman bir pazarlama alan adı kurmazsanız, hiçbir şey değişmez: her şey tam olarak daha önce olduğu gibi varsayılan hesabınızdan gönderilmeye devam eder.

## Kurulum

Herhangi bir giriş noktasından başlayabilirsiniz:

- Campaign Studio gösterge paneli pankartındaki **"Pazarlama alan adı kur"** düğmesi veya
- **E-posta Hesapları → "Pazarlama gönderim alan adı"**.

!["İşlemsel e-postanızı koruyun" pankartı ve Pazarlama alan adı kur düğmesiyle Campaign Studio gösterge paneli](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-nudge.webp)

![E-posta Hesapları listesinde, Sağlayıcıları Gözden Geçir'in yanında Pazarlama gönderim alan adı düğmesi](/static/core/admin/img/help/marketing-sending-domain/marketing-domain-button.webp)

Her ikisi de pazarlama hesabı için önceden işaretlenmiş e-posta kurulum sihirbazını açar. Ardından:

1. **Bir alt alan adı seçin.** `news.yourstore.com` veya
   `mail.yourstore.com` gibi bir şey kullanın. Bu en önemli adımdır: pazarlama kimliği, işlemsel e-postalarınızın kullandığı alan adından **farklı bir (alt)alan adı** olmalıdır — bu ayrım, işlemsel itibarınızı koruyan şeydir. Ana alan adınızdan pazarlama gönderimi yapmak size hiçbir izolasyon sağlamaz.
2. **Gönderici adresini girin** o alt alan adında, örneğin `news@news.yourstore.com`.
3. **DNS kayıtlarını ekleyin.** Sihirbaz, alt alan adı için SPF, DKIM ve DMARC kayıtlarını oluşturur — bu pazarlama kimliğine özgü bir DKIM anahtarı dahil. Bunları DNS sağlayıcınıza ekleyin (sihirbazda kopyalama düğmeleri ve sağlayıcı başına sekmeler var), ardından tüm kayıtlar geçene kadar denetimi çalıştırın.
4. **Tamamlayın.** Hesap oluşturulur ve **Sadece Pazarlama** olarak işaretlenir. Bundan sonra kampanyalarınız bundan gönderilir.

**E-posta Hesapları** listesinde çalıştığını doğrulayabilirsiniz: **Sadece Pazarlama** amaçlı ikinci bir hesap göreceksiniz ve Campaign Studio pankartı kaybolacak.

## İyi bilinenler

- **İşlemsel e-postayı yanlışlıkla bozamazsınız.** Spwig, tek hesabınızı "Sadece Pazarlama" olarak ayarlamanıza veya son işlemsel hesabınızı devre dışı bırakmanıza/silmenize izin vermez — sipariş onayları ve şifre sıfırlamaları için her zaman bir yer vardır.
- **Kademeli olarak ısının.** Yeni bir gönderim alan adının henüz itibarı yoktur.

Tüm listenizi birinci gün patlatmak yerine, hacminizi birkaç hafta içinde kademeli olarak artırın.
- **Alt alan adının DNS sağlığını koruyun.** Pazarlama alt alan adındaki SPF, DKIM ve DMARC, ana alan adınız gibi geçerli kalmalıdır.

Tam resim için [E-posta Teslimat El Kitabı](deliverability) sayfasına bakın.
- **Onay hâlâ geçerlidir.** Pazarlama e-postaları yalnızca kayıt olan abonelere gönderilir ve her kampanya bir abonelikten çıkarma bağlantısı içerir — alan adının ayrılması bunun hiçbir şeyini değiştirmez.