---
title: Bakım Modu
---

Bakım modu, mağazanızı geçici olarak çevrimdışı hale getirir ve müşterilere "yakında geri döneriz" mesajı gösterir. Bakım modu sırasında yönetici arka ucu tamamen erişilebilir kalır — müşterilerin bakım sayfasında tutulduğu sürece çalışmayı sürdürebilirsiniz.

Bakım modunu, kısa süreli tutarsız bir durum yaratabilecek değişiklikler yapmadan önce kullanın. Örneğin, büyük bir ürün içeriği aktarımı yaparken, önemli bir tema yeniden tasarımı uygularken veya bir geri yükleme işlemi tamamlanana kadar.

![Sistem paneline bakımda modu açma](/static/core/admin/img/help/maintenance-mode/system-dashboard-maintenance.webp)

## Bakım modunu etkinleştirme

1. **Yönetim > Sistem Metrikleri**'ne gidin
2. Araç çubuğundan **Sistem Panosu**'nu tıklayın
3. **Mağaza Durumu** panelinde **Bakım Modunu Etkinleştir**'i tıklayın
4. Opsiyonel olarak bir **Neden** girin — bu sadece kendi referansınız için ve müşterilere gösterilmez (örneğin, `Ürün kataloğu güncelleniyor`)
5. **Etkinleştir**'i tıklayarak onaylayın

Mağazanız, bakım sayfasını tüm ziyaretçilere hemen göstermeye başlar. Yönetici arka ucu etkilenmez ve normal şekilde çalışmayı sürdürebilirsiniz.

## Müşterilerin göründüğü şey

Bakım modu etkin olduğunda, mağazanızın her sayfası (mağaza, ürün sayfaları, ödeme ve hesap sayfaları) markalı bir bakım bildirimi görüntüler. Mesaj, mağazanın geçici olarak kullanılamaz olduğunu belirtir ve müşterilere kısa süre sonra geri dönmelerini teşvik eder.

Bakım modu etkinleştirildiğinde oturum ortasında veya ödeme sürecinde olan müşteriler, bir sonraki isteklerinde bakım sayfasını görecektir. Devam eden siparişler kaybolmaz — bakım modu devre dışı bırakıldığında veriler hala orada olacaktır.

## Bakım modunu devre dışı bırakma

1. **Yönetim > Sistem Metrikleri**'ne gidin
2. **Sistem Panosu**'nu tıklayın
3. **Mağaza Durumu** panelinde, bakım modunun etkin olduğuna dair bir banner görünecektir
4. **Bakım Modunu Devre Dışı Bırak**'ı tıklayın
5. İstenirse onaylayın

Mağazanız hemen çevrimiçi hale gelir. Müşteriler normal şekilde tarayabilir ve satın alabilir.

## Spwig'in otomatik olarak bakım modunu etkinleştirme zamanları

Belirli sistem işlemleri bakım modunu otomatik olarak etkinleştirir ve işlem tamamlandığında mağazayı tekrar çevrimiçi hale getirir:

- **Platform yükseltmeleri** — yükseltme işlemi, değişiklikleri uygulamadan önce bakım modunu etkinleştirir ve yükseltme tamamlandığında devre dışı bırakır
- **Geriyükleme işlemleri** — bir yedekten geri yükleme, geri yükleme süresince mağazayı bakım moduna alır

Eğer bir otomatik işlem beklenmeden sonlanırsa, bakım modu hala etkin olabilir. Bu durumda, yukarıda belirtilen adımları izleyerek manuel olarak devre dışı bırakabilirsiniz.

## İpuçları

- Bakım modunu etkinleştirmeden önce ekibinize haber verin — mağazanızın her ziyaretçisini etkiler
- Bakım pencerelerini mümkün olduğu kadar kısa tutun; bile birkaç dakika çevrimdışı olmak müşteri güvenini etkileyebilir
- Neden alanını, bakım modunun neden etkinleştirildiğini hatırlatmak için kullanın — sistem günlüğüne görünür
- Bakım modunun etkin olduğu ama kendiniz etkinleştirmemiş olduğunuzu fark ederseniz, otomatik işlemler tarafından tetiklendiğini kontrol etmek için sistem günlüğünü inceleyin
- Satış üzerindeki etkileri en aza indirmek için, düşük trafiğe sahip dönemlerde (akşamlar veya erken sabahlar) bakım pencerelerini planlayın