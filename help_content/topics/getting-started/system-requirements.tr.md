---
title: Sistem Gereksinimleri
---

Spwig, çoğu modern Linux sunucusunda çalışır. Bu sayfa, minimum ve önerilen özelliklerin ne olduğunu, daha küçük sunucularda ne olacağını ve hangi bulut sağlayıcılarının iyi çalıştığını açıklar.

## Minimum gereksinimler

| Kaynak | Minimum | Önerilen |
|----------|---------|-------------|
| **İşletim sistemi** | Ubuntu 22.04 LTS, Ubuntu 24.04 LTS veya Debian 12 | Ubuntu 24.04 LTS |
| **RAM** | 4 GB | 8 GB veya daha fazla |
| **Disk alanı** | 20 GB | 40 GB veya daha fazla |
| **CPU** | 1 vCPU | 2+ vCPUs |
| **Mimari** | x86_64 (AMD64) | x86_64 |
| **Ağ** | Kamu IP adresi (tekil mod için) | Statik kamu IP |
| **Portlar** | 80 ve 443 (tekil mod) veya herhangi bir alternatif port (yan sunucu modu) | 80 ve 443 |

> **Not:** ARM tabanlı sunucular (örneğin AWS Graviton, Oracle Ampere) şu anda desteklenmiyor.

## Kaynak katmanları

Yükleme programı, sunucunuzdaki mevcut RAM'i otomatik olarak algılar ve uygun kaynak katmanını seçer.

### Standart katman (6 GB+ RAM)

Tüm hizmetler tam kapasiteyle çalışır:

- AI destekli **çeviri hizmeti** etkin — ürün açıklamalarını, sayfa içeriğini ve SEO metnini, yönetim panelinizden doğrudan birden fazla dile çevirin
- Uygulama, veritabanı ve arka plan çalışanlar için tam bellek tahsisi
- Arka plan çalışanlarının iş parçacığı sayısı, CPU sayınıza göre optimize edilmiştir

### Küçük katman (4–6 GB RAM)

Yükleme programı, bellek tasarrufu için uyarlanır:

- AI çeviri hizmeti **devre dışı** bırakılır ve yaklaşık 2 GB RAM tasarruf edilir. Hâlâ el ile çevirileri yönetebilir veya harici çeviri araçlarını kullanabilirsiniz — sadece yerleşik AI çeviri hizmeti etkilenir.
- Uygulama ve çalışan bellek sınırları azaltılır
- Diğer tüm özellikleri standart katmanla aynı şekilde çalışır

> **İpucu:** Küçük bir sunucu ile başlarsanız ve daha sonra 6 GB+ RAM'e yükseltirseniz, çeviri hizmetini etkinleştirmek için yükleme programını tekrar çalıştırın.

## Önerilen bulut sağlayıcıları

Spwig, gereksinimleri karşılayan herhangi bir Linux sunucusunda çalışır. Bu sağlayıcılar test edilmiş ve iyi bir değer sunar:

| Sağlayıcı | Önerilen plan | RAM | Disk | Yaklaşık maliyet |
|----------|-----------------|-----|------|-----------------|
| **DigitalOcean** | Temel Droplet | 4 GB | 80 GB | $24/ay |
| **Linode (Akamai)** | Paylaşılan 4 GB | 4 GB | 80 GB | $24/ay |
| **Vultr** | Bulut Hesaplaması | 4 GB | 100 GB | $24/ay |
| **Hetzner** | CX31 | 8 GB | 80 GB | €8/ay |
| **OVH** | Başlangıç VPS | 4 GB | 80 GB | €7/ay |

Günlük trafiği önemli miktarda bekleyen veya büyük ürün kataloğuna (10.000+ ürün) sahip mağazalar için 8 GB RAM ve 2+ vCPU ile başlayın.

## Disk alanı kullanımı

Yeni bir Spwig kurulumu yaklaşık 8 GB disk alanı kullanır:

| Bileşen | Boyut |
|-----------|------|
| Docker görüntüler | ~4 GB |
| Veritabanı (boş mağaza) | ~200 MB |
| AI çeviri modelleri (etkinse) | ~2 GB |
| Uygulama ve yapılandırma dosyaları | ~500 MB |
| İşletim sistemi ve Docker motoru | ~3 GB |

Ekstra alan için planlayın:

- **Ürün resimleri ve medya** — katalog boyutuna bağlıdır. Yüzlerce ürün içeren tipik bir mağaza için 1–5 GB bütçeleme yapın.
- **Veritabanı büyümesi** — siparişler, müşteriler ve analiz verileriyle birlikte büyür. Günlük 100 sipariş işleyen bir mağaza genellikle yılda ~1 GB büyüme gösterir.
- **Yedeklemeler** — yerel olarak yedeklemeler saklanıyorsa, her tam yedekleme, veritabanınızın ve medyanızın boyutu kadar olur. 30 günlük bir saklama politikası varsa, mevcut veri boyutunun 2–3×'i kadar bütçeleme yapın.

## Alan adı ve DNS

Alan adı kurulum sırasında isteğe bağlıdır ancak üretim kullanımı için gereklidir. Aşağıdakilere ihtiyacınız vardır:

- Bir alan adı veya alt alan adı (örneğin `shop.example.com`)
- Sunucunuzun kamu IP adresine işaret eden bir **A kaydı**
- DNS yayılımının tamamlanması (kayıt eklendiğinden sonra genellikle 5–60 dakika sürer)

Yükleme programı, geçerli bir alan adı algılandığında otomatik olarak Let's Encrypt'den ücretsiz bir SSL sertifikası alır. Ayrıca, kurulumdan sonra `./configure-domain.sh` betiğini kullanarak bir alan adı ekleyebilirsiniz.

## Güvenlik Duvarı

Sunucunuzda bir güvenlik duvarı varsa (çoğu bulut sağlayıcısı varsayılan olarak birini etkinleştirir), aşağıdaki portların açık olduğundan emin olun:

| Port | Protocol | Purpose |
|------|----------|---------|
| **22** | TCP | Sunucuyu yönetmek için SSH erişimi |
| **80** | TCP | HTTP (Let's Encrypt sertifika doğrulaması için gerekli) |
| **443** | TCP | HTTPS (mağazanızın güvenli trafiği) |

Sidecar modunda, 80/443 yerine yükleyici tarafından atanan alternatif portu açın.

## Yazılım önkoşulları

Yükleyici, tüm yazılım kurulumunu otomatik olarak gerçekleştirir. Referans olarak, bunları yükler veya doğrular:

- **Docker Engine** — konteyner çalıştırma motoru (eksikse otomatik olarak kurulur)
- **Docker Compose** — hizmet senkronizasyonu (Docker Engine ile birlikte gelir)
- **curl** — yükleyici tarafından kullanılır (neredeyse tüm Linux sistemlerinde mevcuttur)

Ön yüklemek gereken başka bir yazılım yoktur. Spwig, Python, Node.js, PostgreSQL, Redis veya Nginx'i manuel olarak yüklemenizi gerektirmez — her şey Docker konteynerları içinde çalışır.