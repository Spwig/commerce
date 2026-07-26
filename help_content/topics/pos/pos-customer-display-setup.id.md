---
title: Pengaturan Tampilan Pelanggan POS
---

Tampilan pelanggan adalah layar kedua yang menghadap pelanggan selama transaksi. Saat Anda memproses transaksi, pelanggan melihat setiap item saat di-scan, total sementara, pemecahan harga dan pajak, serta — ketika tidak ada transaksi yang berlangsung — slideshow promosi rotasi dari konten promosi Anda."
    },
    {
      "type": "paragraph",
      "content": "Panduan ini mencakup aspek perangkat keras dan pasangan dalam mengatur tampilan pelanggan Anda: mengaktifkan fitur tersebut di terminal, memasangkan perangkat terpisah sebagai layar tampilan, dan menangani skenario pengaturan umum. Untuk informasi mengenai slideshow promosi yang ditampilkan selama periode idle, lihat [Customer Display Promo Slides](customer-display-promo-slides)."
    },
    {
      "type": "heading",
      "content": "Apa yang ditampilkan oleh tampilan pelanggan"
    },
    {
      "type": "paragraph",
      "content": "Ketika transaksi aktif, tampilan pelanggan menampilkan:"
    },
    {
      "type": "list",
      "content": [
        "Setiap item saat ditambahkan atau dihapus, dengan jumlah dan harga",
        "Subtotal keranjang, diskon yang diterapkan, dan pemecahan pajak",
        "Total yang harus dibayar dan, saat pembayaran, jumlah uang yang diberikan dan kembalian"
      ]
    },
    {
      "type": "paragraph",
      "content": "Ketika terminal dalam keadaan idle (tidak ada transaksi aktif), tampilan beralih ke slideshow promosi. Anda mengontrol konten slideshow tersebut secara terpisah — lihat [Customer Display Promo Slides](customer-display-promo-slides)."
    },
    {
      "type": "heading",
      "content": "Konfigurasi perangkat keras umum"
    },
    {
      "type": "paragraph",
      "content": "Ada tiga cara praktis untuk mengatur layar yang menghadap pelanggan:"
    },
    {
      "type": "list",
      "content": [
        "**Tablet atau monitor terpisah di atas stand** — pengaturan paling umum untuk penjualan di meja. Tablet kecil yang didukung di atas stand menghadap pelanggan, sementara terminal utama menghadap Anda. Anda memasangkan dua perangkat menggunakan kode sementara (dijelaskan di bawah).",
        "**Monitor kedua dalam mode desktop diperpanjang** — jika terminal utama Anda adalah laptop atau desktop, colokkan monitor kedua, perpanjang desktop Anda ke monitor tersebut, lalu drag jendela tampilan ke monitor kedua dan maksimalkan. Kedua layar berjalan di perangkat yang sama; tidak diperlukan kode pasangan.",
        "**Pole display khusus** — unit tampilan perangkat keras yang dipasang di tiang, biasanya terhubung ke terminal meja melalui USB atau ditempatkan di meja. Buka `/pos/display/` di browser perangkat pole dan pasangkan menggunakan kode dari terminal utama."
      ]
    },
    {
      "type": "heading",
      "content": "Mengaktifkan tampilan pelanggan di terminal"
    },
    {
      "type": "paragraph",
      "content": "Fitur tampilan pelanggan diaktifkan per terminal melalui konfigurasi perangkat keras terminal."
    },
    {
      "type": "list",
      "content": [
        "Navigasikan ke **POS > Terminals** dan buka terminal yang ingin Anda konfigurasi (atau klik **+ Tambahkan Terminal POS** untuk yang baru).",
        "Klik tab **Device**.",
        "Gulir ke kartu **Hardware Configuration**. Anda akan melihat bidang JSON.",
        "Tambahkan `"customer_display": true` ke objek JSON. Contohnya:"
      ]
    },
    {
      "type": "code-block",
      "content": "{'customer_display': true}"
    },
    {
      "type": "paragraph",
      "content": "Jika bidang sudah berisi pengaturan perangkat keras lainnya (seperti konfigurasi printer atau scanner), tambahkan `"customer_display": true` bersamanya:"
    },
    {
      "type": "code-block",
      "content": "{'printer': 'HP', 'scanner': 'Datalogic', 'customer_display': true}"
    },
    {
      "type": "list",
      "content": [
        "Klik **Save**."
      ]
    },
    {
      "type": "image",
      "content": "![Konfigurasi perangkat keras terminal dengan customer_display diaktifkan](/static/core/admin/img/help/pos-customer-display-setup/terminal-capabilities-toggle.webp)"
    },
    {
      "type": "paragraph",
      "content": "Setelah diaktifkan, aplikasi POS di terminal tersebut akan membuka tampilan pelanggan dalam jendela atau tab browser kedua saat sesi dimulai."
    },
    {
      "type": "heading",
      "content": "Memasangkan perangkat terpisah sebagai tampilan"
    },
    {
      "type": "paragraph",
      "content": "Jika Anda menggunakan perangkat fisik terpisah untuk layar pelanggan (tablet, ponsel, atau komputer kedua), pasangkan perangkat tersebut ke terminal menggunakan kode 6 digit sementara."
    },
    {
      "type": "heading",
      "content": "Langkah 1: Buat kode pasangan di terminal utama

Buka aplikasi POS di terminal utama Anda dan pergi ke pengaturan tampilan atau bagian pasangan tampilan dari antarmuka terminal.

Minta kode pasangan tampilan baru.

Kode adalah angka 6 digit dan berlaku selama **5 menit**.

Ketika Anda menghasilkan kode baru, semua kode sebelumnya yang belum digunakan untuk terminal ini secara otomatis dibatalkan.

### Langkah 2: Buka URL tampilan di perangkat pelanggan

Di perangkat yang menghadap ke pelanggan, buka browser web dan pergi ke:

```
https://your-store-domain.com/pos/display/
```

Tidak diperlukan login — halaman tampilan dapat diakses secara umum. Ini disengaja: perangkat tampilan tidak memerlukan kredensial staf, dan kode pasangan menyediakan tautan antara tampilan dan terminal yang benar.

![Tampilan pelanggan idle](/static/core/admin/img/help/pos-customer-display-setup/customer-display-view.webp)

### Langkah 3: Masukkan kode pasangan

Di perangkat pelanggan, masukkan kode 6 digit dari terminal utama. Tampilan akan dipasangkan ke terminal tersebut dan mulai menampilkan data keranjang secara langsung.

Setelah kode digunakan, kode tersebut segera menjadi tidak valid dan tidak dapat digunakan kembali.

## Menghasilkan ulang kode pasangan

Jika kode pasangan kedaluwarsa sebelum Anda dapat memasukkannya, atau jika Anda perlu memasangkan ulang perangkat tampilan (misalnya, jika perangkat tampilan diganti atau diatur ulang), hasilkan kode baru dari aplikasi POS di terminal utama.

Menghasilkan kode baru secara otomatis membatalkan kode yang sudah ada dan belum digunakan untuk terminal tersebut. Kode baru berlaku selama 5 menit.

Anda tidak perlu mengubah apa pun di admin untuk menghasilkan ulang kode — ini dilakukan sepenuhnya dalam aplikasi POS.

## Pengaturan multi-monitor di satu perangkat

Jika terminal utama Anda adalah laptop atau desktop dengan dua monitor:

1. Hubungkan monitor kedua dan atur ke mode **desktop diperpanjang** di pengaturan tampilan sistem operasi Anda (bukan mode cermin).
2. Buka aplikasi POS di layar utama seperti biasa.
3. Aplikasi POS akan membuka tampilan pelanggan dalam jendela kedua. Tarik jendela tersebut ke monitor kedua.
4. Perbesar atau masuk ke mode layar penuh di monitor kedua.

Tidak diperlukan kode pasangan karena kedua jendela berjalan di perangkat yang sama dan berkomunikasi langsung.

## Perilaku idle

Ketika tidak ada penjualan aktif, tampilan pelanggan menampilkan slideshow berputar dari gambar promosi. Anda membuat dan mengelola slide-slide tersebut secara terpisah di bawah **POS > Promo Slides**.

Untuk detail tentang membuat slide, menargetkannya ke toko tertentu, dan mengelola konten musiman, lihat [Customer Display Promo Slides](customer-display-promo-slides).

Jika tidak ada slide yang dikonfigurasi, tampilan menampilkan layar selamat datang sederhana dengan nama toko Anda.

## Penyelesaian Masalah

**Tampilan menjadi kosong atau berhenti memperbarui**

Tampilan berkomunikasi dengan terminal utama secara real time. Jika koneksi terputus, tampilan mungkin menjadi kosong atau menampilkan data yang sudah usang. Perbarui browser di perangkat pelanggan. Jika hal tersebut tidak membantu, hasilkan kode pasangan baru dan pasangkan ulang.

**Tampilan menampilkan keranjang dari terminal yang salah**

Setiap tampilan dipasangkan ke terminal tertentu. Jika Anda memiliki beberapa terminal, pastikan Anda menghasilkan kode pasangan di terminal yang benar dan memasukkannya di tampilan. Untuk memperbaiki ketidakcocokan, hasilkan kode baru di terminal yang benar dan pasangkan ulang perangkat tampilan.

**Kode pasangan kedaluwarsa sebelum saya dapat memasukkannya**

Kode berlaku selama 5 menit. Hasilkan kode baru dari aplikasi POS dan masukkan segera ke perangkat tampilan. Pertahankan kedua perangkat dekat satu sama lain selama proses pasangan.

**Kode pasangan telah dimasukkan tetapi tampilan tidak terhubung**

Periksa bahwa perangkat pelanggan dapat mengakses domain toko Anda (membutuhkan akses jaringan). Juga verifikasi bahwa `"customer_display": true` diatur dalam konfigurasi perangkat keras terminal dan bahwa terminal telah disimpan.

**URL tampilan mengembalikan kesalahan**

Pastikan Anda mengakses `/pos/display/` di domain toko Anda, bukan URL admin. Tampilan tidak memerlukan login — jika Anda diminta untuk login, periksa kembali URL.

## Tips

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis tetap utuh.

- **Jaga sesi pasangan singkat** — pastikan perangkat pelanggan siap dan browser terbuka ke `/pos/display/` sebelum menghasilkan kode pasangan.

Anda memiliki 5 menit, tetapi menyelesaikannya dalam waktu kurang dari satu menit menghindari timeout.
- **Uji sebelum membuka** — lakukan penjualan uji dengan layar terhubung untuk memverifikasi pelanggan akan melihat item dan total yang benar sebelum transaksi pertama Anda.
- **Tambahkan bookmark URL layar** — atur browser perangkat pelanggan untuk membuka `/pos/display/` saat startup sehingga selalu siap.
- **Gunakan desktop diperpanjang untuk kesederhanaan** — jika terminal Anda memiliki port HDMI tambahan dan monitor tersedia, pendekatan desktop diperpanjang tidak memerlukan pasangan terus-menerus dan tidak pernah kedaluwarsa.
- **Tambahkan slide promo sebelum membuka** — layar yang hanya menampilkan layar selamat datang kosong saat tidak aktif adalah kesempatan yang terlewat.

Buat setidaknya beberapa slide promosi agar layar tetap berguna bahkan saat tidak ada transaksi yang berlangsung.

Lihat [Slide Promo Layar Pelanggan](customer-display-promo-slides).
- **Lindungi perangkat layar** — URL layar dirancang untuk dapat diakses secara publik, tetapi hanya menampilkan data keranjang aktif saat dipasangkan dengan terminal yang aktif.

Meskipun demikian, pertimbangkan mode browser kiosk di perangkat pelanggan untuk mencegah pelanggan mengakses halaman lain.