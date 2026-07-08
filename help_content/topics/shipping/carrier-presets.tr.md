---
title: Taşıyıcı Ön Ayarları
---

Taşıyıcı ön ayarları, API entegrasyonu olmadan oluşturulan gönderimler için manuel taşıyıcıları (DHL, FedEx, UPS, özel taşıyıcılar) tanımlar—her ön ayar, taşıyıcı logolu, izleme URL şablonu ve görüntüleme ayarları sağlar. Sistem ön ayarları (DHL, FedEx, UPS, USPS) önceden yapılandırılmıştır ve silinemez, ancak özel ön ayarlar satıcıların bölgesel veya özel taşıyıcılar eklemelerine olanak tanır. Ön ayarlar, satıcıların manuel gönderimlerde takip numaralarını manuel olarak girmesi gereken gönderimlere bağlanır. API üzerinden etiket satın almak yerine.

API entegrasyonu olmadan manuel gönderimler oluştururken veya yalnızca izleme bağlantıları kullanmak istediğinizde taşıyıcı ön ayarlarını kullanın.

## Sistem Ön Ayarları vs. Özel Ön Ayarlar

**Sistem Ön Ayarları** (Önceden yüklenmiş):
- DHL, FedEx, UPS, USPS, Royal Mail, Canada Post, Australia Post
- Silinemez (is_system=True)
- Takip URL'si veya logoyu geçersiz kılabilir
- Varsayılan takip URL şablonları sağlanmıştır

**Özel Ön Ayarlar** (Satıcı tarafından oluşturulmuş):
- Bölgesel taşıyıcılar (OnTrac, LaserShip, bölgesel posta)
- Özel taşıyıcılar (kargo, beyaz el teslimatı)
- Düzenlenebilir veya silinebilir
- Manuel takip URL şablonu gerekir

---

## Taşıyıcı Ön Ayarları Yapılandırması

Her ön ayar aşağıdaki öğeleri tanımlar:

**Temel Ayarlar**:
- **Ad**: Taşıyıcı görüntüleme adı (örneğin, "DHL Express", "Yerel Kurye")
- **Kod**: İç kimlik (örneğin, "dhl", "local_courier")
- **Logo**: Taşıyıcı logosu (isteğe bağlı, sağlanmazsa ikon kullanılır)
- **İkon**: FontAwesome ikonu (örneğin, "fa-truck")
- **Aktif**: Görünürlüğü aç/kapa

**Takip Yapılandırması**:
- **Takip URL Şablonu**: {tracking_id} yer tutuculu URL kalıbı
- **Takip URL'si Geçersiz Kılma**: Özel URL (varsayılan şablonu geçersiz kılar)

**Sistem Ayarları** (yalnızca sistem ön ayarları için):
- **Sistem Mi**: Silinemez
- **Varsayılan Mi**: Her taşıyıcı türü için bir varsayılan

---

## Takip URL Şablonları

Takip URL'leri {tracking_id} yer tutucu kullanır:

**Örnekler**:

DHL: `https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}`

FedEx: `https://www.fedex.com/fedextrack/?tracknumbers={tracking_id}`

UPS: `https://www.ups.com/track?tracknum={tracking_id}`

USPS: `https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_id}`

Özel: `https://track.localcourier.com/tracking/{tracking_id}`

**Nasıl Çalışır**:
1. Satıcı, takip numarası "1234567890" ile gönderim oluşturur
2. Sistem {tracking_id} yerine gerçek numarayı değiştirir
3. Müşteri takip bağlantısını tıklar → taşıyıcı sitesine yönlendirilir
4. Sonuç: `https://www.dhl.com/en/express/tracking.html?AWB=1234567890`

---

## Özel Taşıyıcı Ön Ayarı Oluşturma

**Adım Adım**:

1. Ayarlar > Sevkiyat > Taşıyıcı Ön Ayarları'na gidin
2. "Taşıyıcı Ön Ayarı Ekle"yi tıklayın
3. Ad girin (örneğin, "OnTrac")
4. Kod girin (slug: "ontrac")
5. Opsiyonel: Logo resmini yükleyin
6. İkonu seçin (fa-truck, fa-shipping-fast, v.b.)
7. {tracking_id} ile takip URL şablonu girin
8. Aktif = Evet olarak ayarlayın
9. Kaydedin

**Örnek - OnTrac**:
```
Ad: OnTrac
Kod: ontrac
Takip URL'si: https://www.ontrac.com/tracking.asp?tracking_number={tracking_id}
İkon: fa-truck
Aktif: Evet
```

---

## Sistem Ön Ayarı Takip URL'lerini Geçersiz Kılma

Sistem ön ayarları, takip URL'lerini geçersiz kılabilir:

**Kullanım Durumu**: Taşıyıcı hesabınız özel bir takip portalına sahipse

**Geçersiz Kılma Nasıl Yapılır**:
1. Sistem ön ayarını düzenle (örneğin, DHL)
2. "Takip URL'si Geçersiz Kılma" alanına geçersiz URL girin
3. Geçersiz kılma, varsayılan şablonu geçersiz kılar
4. Kaydedin

**Örnek**:
```
Sistem: DHL
Varsayılan URL: https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}
Geçersiz URL: https://track.dhl.com/special-account/{tracking_id}
Sonuç: Tüm DHL gönderimleri için geçersiz URL kullanılır
```

---

## Taşıyıcı Logoları

**Logo Kılavuzu**:
- Format: PNG veya SVG (ölçeklenebilirlik için SVG tercih edilir)
- Boyut: 200×60px önerilir
- Arka Plan: Şeffaf veya beyaz
- Renk: Tam renk taşıyıcı markajı

**Varsayılan İkon**:
Logo yüklenmezse sistem FontAwesome ikonu gösterir:
- fa-truck (varsayılan)
- fa-shipping-fast (hızlı kargo)
- fa-plane (hava kargo)
- fa-box (koli)

---

## Taşıyıcı Ön Ayarlarını Gönderimlerde Kullanma

El ile gönderim oluştururken:

1. Siparişler > Sipariş Detayı > Gönderim Oluştur
2. "El ile Gönderim" modunu seçin
3. Ön ayar dropdown'dan taşıyıcı seçin
4. Takip numarasını girin
5. Opsiyonel: Bu gönderim için takip URL'sini geçersiz kılın
6. Kaydedin

**Gönderim Görünümü**:
- Taşıyıcı logosu gösterilir (veya ikon)
- Takip numarası görüntülenir
- Tıklanabilir takip bağlantısı (ön ayar URL şablonu kullanır)

---

## Varsayılan Taşıyıcı

Sistemde her taşıyıcı türü için bir ön ayar varsayılan olarak ayarlanabilir:

**Kullanım Durumu**: En çok kullanılan taşıyıcı, gönderim oluşturma sırasında otomatik olarak seçilir

**Varsayılan Nasıl Ayarlanır**:
1. Taşıyıcı ön ayarını düzenle
2. "Varsayılan" kutusunu işaretleyin
3. Kaydedin
4. Önceki varsayılan (varsa) otomatik olarak kaldırılır

**Sadece bir varsayılan izin verilir** - yeni varsayılan ayarlanırsa önceki varsayılan bayrağı kaldırılır.

---

## İpuçları

- **Açıklayıcı adlar kullanın** - "DHL Express" "DHL"'den daha iyidir
- **Takip URL'lerini test edin** - Gerçek takip numaralarıyla şablonun çalıştığını doğrulayın
- **Taşıyıcı logolarını yükleyin** - Müşteri e-postalarında profesyonel görünüm sağlar
- **Sistem ön ayarlarını silmeyin** - Bunlar doğru şekilde önceden yapılandırılmıştır
- **Geçersiz kılma az kullanın** - Taşıyıcı takip sistemini değiştirdiğinizde yalnızca kullanın
- **Ana taşıyıcı için varsayılan ayarlayın** - Gönderim oluşturma sırasında zaman kazandırır
- **Ön ayarları aktif tutun** - Taşıyıcı hizmeti durdurulmazsa yalnızca devre dışı bırakın
- **Özel taşıyıcıları belgeleyin** - Bölgesel taşıyıcılar hakkında notlar ekleyin
