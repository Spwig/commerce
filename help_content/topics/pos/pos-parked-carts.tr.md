---
title: İşlem Duraklatma ve Devresine Alma
---

<!-- screenshots-needed:
- url: /en/admin/pos_app/parkedcart/
  filename: parked-cart-list.webp
  description: Parked cart list view (may be empty on fresh install — capture anyway)
  save-to: core/static/core/admin/img/help/pos/
-->

İşlem duraklatma özelliği, kasiyerlerin bir işlemi duraklatabilir ve hemen bir sonraki müşteriye hizmet verebilir — hiçbir ürün veya indirim kaybedilmeden. Hazır olduğunuzda, orijinal sepet tam olarak olduğu gibi geri yüklenir ve işlem önceki durumundan devam eder.

## İşlem Duraklatmanın Ne Anlama Geldiğini

Bir kasiyer POS terminalinde **Duraklat** butonuna bastığında, Spwig mevcut sepetin tam bir kopyasını sunucuya kaydeder. Terminal temizlenir ve hemen yeni bir işlem başlatılabilir. Duraklatılmış sepet, oluşturulduğu terminalle ilişkilendirilir.

Kopyada hiçbir şey kaybolmaz. Duraklatılmış sepet şu bilgileri korur:

- Her ürün ve miktarı
- Satışa eklenen müşteri
- Sepete veya bireysel ürünlere uygulanan el ile indirimler

Duraklatılmış sepet, aynı terminalde en fazla **24 saat** boyunca kullanılabilir. Bunun ardından Spwig otomatik olarak onu kaldırır. Geri yüklenen sepetler, geri yükleme işleminden sonra hemen kaldırılır ve 24 saatlik pencereye dahil değildir.

## İşlem Nasıl Duraklatılır

Bir sepeti duraklatmak için onun içinde en az bir ürün olmalıdır. Boş bir sepet duraklatılamaz.

1. Bir işlem devam ederken, POS terminalindeki **Duraklat** butonuna bastırın.
2. Spwig sepeti kaydeder ve terminali temizler. Onay mesajı göreceksiniz ve duraklatılmış sepetler alanındaki sayacın güncelleneceğini göreceksiniz.
3. Artık boş terminalde bir sonraki müşterinin işlemine başlayın.

Eğer işlem duraklatılmadan önce bir müşteri eklenmişse, onun adı duraklatılmış sepetler listesinde kolayca tanımlanması için görünür olur.

## Duraklatılmış Bir İşlem Nasıl Devresine Alınır

1. POS terminalindeki **Duraklatılmış Sepetler** alanına veya simgesine bastırın. Bu terminalde şu anda duraklatılmış tüm sepetlerin listesini göreceksiniz. Listede müşteri adı (eğer eklenmişse), ürün sayısı, toplam tutar, duraklatan kasiyer ve duraklatma zamanı yer alır.
2. Devresine almak istediğiniz sepeti seçin.
3. Eğer mevcut terminalinizde ürün varsa, POS bu ürünleri temizleyerek duraklatılmış sepeti geri yükler. Mevcut işlemi tamamlamadan veya duraklatmadan başka bir işlemi devresine almak istemeyin.
4. Duraklatılmış sepetin ürünleri, müşteri bağlantısı ve el ile indirimleri tümüyle geri yüklenir. Satış normal şekilde devam eder.

## Duraklatılmış Sepet Görünürlüğü

Duraklatılmış sepetler, oluşturuldukları terminalle **bağlıdır**. Aynı terminalde oturum açan herhangi bir kasiyer, o terminalde duraklatılmış herhangi bir sepeti görebilir ve devresine alabilir — bir sepetin kim tarafından alınacağına dair kasiyer bazlı bir kısıtlama yoktur.

Farklı bir terminalde duraklatılmış sepetler, aynı mağaza konumunda olsalar bile, mevcut terminalinizde görünmez.

## POS'dan Duraklatılmış Bir Sepeti İptal Etme

Bir kasiyer, terminaldeki duraklatılmış sepetler listesinden doğrudan bir duraklatılmış sepeti silebilir — sepeti seçin ve sil veya atma seçeneğini kullanın. Silinen duraklatılmış sepetler kalıcı olarak kaldırılır ve geri alınamaz.

## Otomatik Süre Bitişi ve Temizlik

Her duraklatılmış sepet, **duraklatıldıktan sonra 24 saat sonra** sona erer. Spwig, geri yüklemeden sonra süresi geçmiş sepetleri kaldırmak için arka planda bir görev çalıştırır. Bu işlem için herhangi bir şey yapmanız gerekmez — temizlik otomatik olarak gerçekleşir.

Eğer 24 saatlik pencere bitmeden önce duraklatılmış sepetleri temizlemek isterseniz, bir kasiyer terminaldeki duraklatılmış sepetler listesinden onları tek tek silebilir.

## Vardiya ve Duraklatılmış Sepetler

Bir duraklatılmış sepetin, duraklatıldığı zaman açık olan vardiya ile herhangi bir sert bağlantı yoktur. Bir vardiyanın kapatılması, o terminaldeki duraklatılmış sepetleri otomatik olarak silmez veya iptal etmez. Duraklatılmış sepetler vardiya değişikliklerinden etkilenmez ve 24 saatlik tam süre boyunca mevcuttur.

Bu şu anlamlara gelir:

- Sabah vardiyasının sonunda duraklatılmış bir sepet, daha sonra bir vardiya sırasında bir kasiyer tarafından devresine alınabilir.
- Eğer duraklatılmış sepetlerin vardiya arasında taşınmasını istemiyorsanız, kasiyerlerin vardiya kapatmadan önce duraklatılmış sepetler listesini temizlemesini sağlayın.

## İpuçları

Tüm markdown biçimlendirmesini, görsel yollarını, kod bloklarını ve teknik terimleri koruyun.

- Müşteri "Sadece bir tane daha almak istiyorum" derse, hemen bir sepeti park etmeniz daha hızlıdır — onu tekrar kuyrukta bekletmek ya da manuel olarak ürünleri tekrar eklemekten daha iyidir.
- Eğer park edilmiş sepet listesi uzunsa, önceki bir kasiyerin iş bitiminde işlemi çözemediğini kontrol edin ve eski sepetleri temizleyin.
- Sepeti park etmeden önce mümkün olduğunca müşteriye satışa ekleyin — ismi listede görünür, bu da müşteri geri döndüğünde doğru sepeti bulmak için çok daha kolay olur.
- Park edilmiş sepetler 24 saat sonra sona erer, bu nedenle birden fazla iş gününü kapsayan gece boyu işlemler için uygun değildir.
- Unutmayın ki park edilmiş bir sepette devam etmek, kasadaki mevcut öğeleri temizler.

Aktif işlemi tamamlayın veya başka bir park edilmiş sepeti almadan önce park edin.