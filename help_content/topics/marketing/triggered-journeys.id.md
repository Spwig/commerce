---
title: Journey yang Dipicu
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/{journey_id}/report/
  filename: journey-report.webp
  description: The Journey report page for a journey with meaningful enrollment history — the enrollment funnel cards (Enrolled/Active now/Completed/Exited) and Attributed revenue card both showing non-zero numbers, plus the "Revenue by step" table (Step/Revenue/Orders/Sent/Opens/Clicks) with at least one plain step and one A/B step, both showing real Sent/Opens/Clicks counts.
  save-to: core/static/core/admin/img/help/triggered-journeys/
  viewport: 1440x900
-->

**Journeys** di Campaign Studio adalah rangkaian email multi-langkah yang otomatis, yang dimulai secara mandiri kapan pun pelanggan melakukan sesuatu yang spesifik — mendaftar, melakukan pemesanan, meninggalkan barang di keranjang, tidak aktif untuk sementara waktu, atau pesanan mereka telah dikirim. Daripada mengingat untuk mengirim email sambutan, pengingat pemulihan keranjang, atau permintaan ulasan secara manual, Anda membangun rangkaian sekali dan Spwig menjalankannya untuk setiap pelanggan yang memenuhi syarat, selama journey tetap aktif.

## Tiga cara mengirim email

Campaign Studio sekarang mencakup tiga pola pengiriman yang berbeda:

| Tipe | Perilaku |
|------|-----------|
| **Broadcast** | Dikirim sekali — segera atau pada tanggal dan waktu terjadwal tertentu. Gunakan untuk pengumuman atau penjualan sekali waktu. |
| **Recurring** | Template yang dikirim pada jadwal berulang (lihat [Recurring Campaigns](/help/recurring-campaigns)). |
| **Journey** | Rangkaian multi-langkah yang dimulai secara otomatis untuk satu pelanggan ketika peristiwa siklus hidup terjadi, kemudian mengirimkan langkah-langkahnya selama beberapa jam atau hari. |

Journey tidak memiliki tombol "kirim" sendiri dan tidak ada jadwal yang perlu dikonfigurasi — ia bereaksi terhadap peristiwa, bukan jam.

## Pemicu (Triggers)

Setiap journey mendengarkan tepat satu peristiwa, yang diatur sebagai **Trigger** journey:

| Trigger | Terpicu ketika |
|---------|-----------|
| **Pelanggan mendaftar** | Akun pelanggan baru dibuat. |
| **Pesanan dibuat** | Pesanan apa pun dibuat, oleh pelanggan baru atau yang kembali. |
| **Pesanan pertama dibuat** | Secara khusus pesanan pertama pelanggan. |
| **Keranjang ditinggalkan** | Pembeli menambahkan sesuatu ke keranjang mereka, lalu tidak aktif tanpa melakukan checkout. |
| **Pelanggan tidak aktif (win-back)** | Pelanggan tidak melakukan pemesanan dalam waktu yang cukup lama. |
| **Pesanan dikirim** | Status pesanan berubah menjadi Delivered. |
| **Produk kembali tersedia** | Produk yang pelanggan minta untuk diberi tahu kembali menjadi tersedia. |

## Pemicu pemulihan dan re-engagement, secara detail

**Order delivered** dan **Product back in stock** terpicu segera, dengan cara yang sama seperti **Order is placed**. **Cart abandoned** dan **Customer lapsed (win-back)** bekerja dengan cara yang berbeda: alih-alih bereaksi terhadap satu momen, Spwig secara berkala memeriksa pembeli dan pelanggan yang cocok, sehingga dapat ada penundaan singkat antara keranjang menjadi tidak aktif (atau pelanggan menjadi tidak aktif) dan pendaftaran.

**Cart abandoned** — mendaftarkan pembeli yang menambahkan sesuatu ke keranjang mereka dan kemudian tidak aktif tanpa menyelesaikan checkout. Secara default, itu terjadi setelah sekitar satu jam tidak aktif; jendela tidak aktif yang tepat (dan seberapa jauh ke belakang Spwig masih akan melihat) adalah ambang batas yang dapat disetel oleh host Anda untuk toko Anda. Ini bekerja untuk pembeli yang masuk dan tamu — untuk tamu, Spwig menggunakan alamat email yang ditangkap saat checkout. Jika pembeli kembali dan menyelesaikan pesanan mereka, mereka secara otomatis dikeluarkan dari journey, sehingga pembelian yang selesai tidak pernah mendapatkan email "apakah Anda lupa sesuatu?". Tambahkan blok konten **Abandoned Cart** ke email pemulihan untuk menunjukkan persis apa yang ditinggalkan, dengan harga langsung, gambar, dan tautan kembali ke keranjang — atau gunakan blok **Featured Product** untuk menyorot satu item.

**Customer lapsed (win-back)** — mendaftarkan pelanggan yang tidak melakukan pemesanan dalam waktu yang cukup lama, untuk memberi mereka alasan untuk kembali.

Secara default, itu adalah 90 hari tanpa pembelian (juga ambang batas yang dapat disetel oleh host).

Seorang pelanggan hanya dimasukkan kembali ke dalam perjalanan pemulihan (win-back) paling banyak sekali per jendela tertentu, jadi seseorang yang sudah lama tidak aktif tidak akan di-daftarkan ulang secara langsung.

**Pesanan Diterima** — memasukkan pelanggan sekali ketika status pesanan mereka berubah menjadi **Diterima**, yaitu momen alami untuk meminta ulasan beberapa hari kemudian. Ini hanya berjalan sekali per pesanan, pada transisi ke status Diterima — perubahan pada pesanan yang sudah diterima sebelumnya tidak akan memicu ini lagi. Catatan bahwa tindakan massal **Tandai pesanan yang dipilih sebagai Diterima** pada daftar pesanan langsung memperbarui pesanan secara langsung dan tidak memicu pengingat ini (atau email konfirmasi pengiriman); perbarui pesanan satu per satu, atau melalui aplikasi seluler Spwig, agar ini berjalan.

**Produk Kembali Tersedia** — ketika produk yang diminta pelanggan untuk diberi tahu kembali tersedia, Spwig memeriksa apakah Anda memiliki perjalanan aktif yang mendengarkan pengingat ini. Jika ya, pelanggan akan masuk ke dalam perjalanan tersebut alih-alih pemberitahuan satu kali biasa — jadi Anda bisa menambahkan penundaan, blok **Produk Unggulan** yang menunjukkan barang yang kembali tersedia, atau email tindak lanjut. Jika tidak ada perjalanan ketersediaan ulang yang aktif, pelanggan tetap menerima email pemberitahuan satu kali standar seperti sebelumnya, jadi mengaktifkan perjalanan untuk pengingat ini sama sekali opsional.

## Membangun sebuah perjalanan

Navigasi ke **Campaign Studio > Journeys** dan klik **Tambahkan Perjalanan**.

1. Beri nama perjalanan tersebut dengan **Nama** — ini hanya untuk referensi Anda; pelanggan tidak per mai mengalaminya.
2. Pilih **Peristiwa Trigger**.
3. Secara opsional atur **Hanya untuk segment** menjadi Segment — ketika diatur, hanya pelanggan yang termasuk dalam segment tersebut yang akan pernah dimasukkan. Biarkan kosong untuk mendaftarkan setiap pelanggan yang memenuhi syarat.
4. Atur **Hanya sekali per pelanggan** dan **Waktu jeda pendaftaran ulang (hari)** — lihat [Mencegah pendaftaran berlebihan](#mencegah-pendaftaran-berlebihan) di bawah ini.
5. Atur **Status** menjadi **Aktif** untuk mengaktifkan perjalanan tersebut. Biarkan sebagai **Rancangan** saat Anda masih merancangnya, atau atur menjadi **Ditunda** untuk menghentikan pendaftaran baru tanpa kehilangan pengaturan Anda.
6. Klik **Simpan** — Spwig langsung membawa Anda ke [Journey Builder](/bantuan/journey-builder), kanvas visual di mana Anda merancang urutan sebenarnya: email apa yang dikirim, durasi antar email, dan apakah pelanggan yang berbeda mengikuti jalur yang berbeda.

Seri undangan tiga langkah yang sederhana, setelah dirancang di kanvas, mungkin terlihat seperti:

| Langkah | Menunggu | Mengirimkan |
|--------|---------|------------|
| 1 | Langsung | Email Selamat Datang |
| 2 | 3 hari kemudian | Tips Memulai |
| 3 | 7 hari setelahnya | Diskon Pesanan Pertama |

Email-email itu sendiri adalah kampanye biasa yang Anda rancang di builder visual yang sama yang Anda gunakan untuk Broadcast — subjek, blok konten, semuanya. Tidak perlu merencanakan atau mengirimkannya sendiri; biarkan sebagai **Rancangan** dan pilih saja dari dropdown langkah di builder. Journey mengirimkannya untuk Anda, sekali per pelanggan yang mencapai langkah tersebut.

Lihat [Journey Builder](/bantuan/journey-builder) untuk panduan lengkap dalam merancang langkah di kanvas, membangun perjalanan dengan kondisi **Ya/Tidak**, dan memulai dari template siap pakai alih-alih kanvas kosong.

## Uji coba A/B sebuah langkah

Setiap langkah **Kirim email** bisa diubah menjadi uji coba A/B, sehingga perjalanan secara otomatis menemukan — lalu terus menggunakan — email yang performanya terbaik. Karena perjalanan berjalan terus-menerus (pelanggan tiba secara bertahap), Spwig tidak menguji batch tetap dan berhenti; alih-alih itu, **membagi peserta secara merata ke berbagai variasi seiring alirannya, mengamati bagaimana masing-masing performanya, dan sekali salah satu dari mereka menjadi pemenang statistik yang jelas maka varian tersebut akan dikunci untuk setiap peserta yang datang berikutnya.** Pelanggan yang sudah sebagian besar selesai tetap menggunakan versi yang pertama kali dikirimkan.

Buka langkah **Kirim email** di [Journey Builder](/bantuan/journey-builder) dan atur **Jenis Langkah**:

- **Satu email** — perilaku normal: semua orang menerima satu email yang Anda pilih.
- **A/B: email berbeda** — pilih **dua hingga empat** email (desain, penawaran, atau tata letak berbeda); setiap pendaftar menerima satu email.
- **A/B: baris subjek berbeda** — pilih satu email dan masukkan **dua hingga empat** baris subjek; setiap pendaftar menerima email tersebut dengan subjek yang berbeda.

Lalu pilih **Pilih pemenang berdasarkan** — **Tingkat buka** (biasanya terbaik untuk uji subjek) atau **Tingkat klik** — dan Anda selesai. Atur perjalanan menjadi **Aktif** dan pendaftar mulai dibagi ke berbagai varian.

Panel langkah menampilkan **papan skor langsung** saat data masuk — penerima, tingkat buka, dan tingkat klik untuk setiap varian, plus seberapa yakin Spwig terhadap pemimpinnya ("Memimpin dengan keyakinan 92%"). Pemenang hanya dikunci setelah Spwig setidaknya **95% yakin** *dan* ada cukup data untuk mempercayainya, sehingga perjalanan dengan lalu lintas rendah tidak akan menarik kesimpulan terlalu cepat. Setelah dikunci, langkah membaca **"Pemenang dikunci: Varian B"** dan setiap pendaftar baru menerima varian tersebut; di kanvas, kartu menampilkan **"A/B · N email"** selama pengujian, lalu **"Pemenang A/B: B"** setelah diputuskan.

Beberapa hal yang perlu diketahui:

- **Berikan lalu lintas.** Keyakinan bergantung pada volume — langkah yang hanya dijangkau oleh segelintir orang mungkin tetap pada "Belum cukup data" untuk sementara waktu. Pengujian A/B bersinar pada perjalanan dengan pendaftaran yang stabil.
- **Mengedit varian atau metrik pemenang memulai pengujian baru** — pemenang yang sebelumnya dikunci dihapus agar pengaturan baru mendapatkan hasil sendiri.
- Langkah A/B dengan kurang dari dua varian **memblokir perjalanan menjadi Aktif** hingga Anda melengkapinya (atau mengembalikannya ke satu email).

Lihat [Pengujian A/B](ab-testing) untuk lebih lanjut tentang bagaimana Spwig membaca keyakinan dan signifikansi.

## Cara pendaftaran bekerja

Ketika peristiwa pemicu terjadi untuk pelanggan, Spwig memeriksa setiap perjalanan aktif yang mendengarkan peristiwa tersebut dan, untuk setiap perjalanan yang memenuhi syarat pelanggan, **mendaftarkan** mereka di titik awal alur. Dari sana, Spwig memajukan pelanggan melalui apa pun yang Anda rancang di kanvas — menunggu setiap langkah **Tunggu**, mengirim email dari setiap langkah **Kirim email**, dan mengikuti jalur **Ya**/**Tidak** yang benar di setiap **Cabang** — hingga mereka mencapai langkah **Keluar**, di mana perjalanan ditandai **Selesai** untuk pelanggan tersebut.

**Persetujuan selalu dihormati.** Pelanggan yang belum memilih masuk ke email pemasaran, atau yang telah berhenti berlangganan, akan dilewati — perjalanan tidak berhenti untuk pelanggan lain, dan penghentian berlangganan di tengah perjalanan secara otomatis menghentikan pengiriman tersisa untuk pelanggan tersebut. Anda tidak perlu menyaring perjalanan Anda berdasarkan status persetujuan sendiri.

## Mencegah pendaftaran berlebihan

Dua pengaturan pada perjalanan mengontrol seberapa sering pelanggan dapat melaluinya:

| Pengaturan | Apa yang dilakukan | Penggunaan umum |
|---------|--------------|-------------|
| **Sekali per pelanggan** *(aktif secara default)* | Setiap pelanggan didaftarkan paling banyak sekali, selamanya, berapa pun kali peristiwa pemicu terjadi lagi untuk mereka. | Seri sambutan — pelanggan seharusnya hanya menerimanya sekali. |
| **Pendinginan pendaftaran ulang (hari)** | Ketika **Sekali per pelanggan** mati, mengatur jumlah minimum hari yang harus berlalu sejak pendaftaran terakhir pelanggan sebelum mereka dapat didaftarkan lagi. Atur ke `0` untuk tanpa pendinginan. | Seri yang dipicu pesanan yang harus berjalan lagi untuk pesanan baru, tetapi tidak memicu ulang untuk setiap pesanan yang ditempatkan minggu yang sama. |

Matikan **Sekali per pelanggan** untuk perjalanan yang ingin Anda jalankan per pesanan (seperti ucapan terima kasih pasca-pembelian), dan kombinasikan dengan pendinginan agar pelanggan yang memesan dua kali dalam hari yang sama hanya didaftarkan sekali. Pelanggan yang sedang aktif menjalani perjalanan tidak pernah didaftarkan ke jalanan kedua yang tumpang tindih dari perjalanan yang sama terlepas dari pengaturan ini.

## Memantau perjalanan


Daftar **Campaign Studio > Journeys** menampilkan **Trigger**, **Status**, jumlah **Email** yang dikirim, serta total **Enrolled** / **Completed** yang berjalan, sehingga Anda dapat melihat sekilas apakah sebuah journey benar-benar menjangkau orang.

![Daftar Journeys yang menampilkan dua journey aktif dengan jumlah pendaftaran dan penyelesaian](/static/core/admin/img/help/triggered-journeys/journey-list.webp)

Untuk melihat pelanggan individual alih-alih total, buka daftar **Journey Enrollments** di `/admin/email_marketing/journeyenrollment/`. Setiap baris menampilkan kemajuan satu pelanggan melalui satu journey: **Journey** apa yang sedang diikuti, **Current step** mereka, **Status** (Active, Completed, atau Cancelled), dan kapan **Next step** mereka jatuh tempo. Gunakan filter untuk menyempitkan ke satu journey atau satu status — misalnya, memfilter ke **Active** menampilkan semua orang yang saat ini sedang di tengah urutan.

![Daftar Journey Enrollments yang menampilkan kemajuan pelanggan di dua journey](/static/core/admin/img/help/triggered-journeys/journey-enrollments.webp)

## Laporan Journey

Setiap journey memiliki halaman **Report** tersendiri, yang dibuka dengan mengklik tombol **Report** pada kartu journey di **Campaign Studio > Journeys**, atau di halaman pengaturan journey itu sendiri. Ini adalah ringkasan satu halaman tentang sejauh mana peserta mencapai urutan dan, jika email Anda berisi tautan yang dilacak, berapa banyak pendapatan yang dihasilkan oleh journey tersebut.

![Halaman laporan Journey yang menampilkan funnel pendaftaran, kartu pendapatan yang diatribusikan, dan tabel pendapatan per langkah](/static/core/admin/img/help/triggered-journeys/journey-report.webp)

### Funnel pendaftaran

Empat kartu menunjukkan posisi peserta saat ini:

| Kartu | Apa yang ditampilkan |
|------|---------------|
| **Enrolled** | Total jumlah pelanggan yang pernah masuk ke journey ini. |
| **Active now** | Peserta yang saat ini sedang di tengah urutan, menunggu atau mengerjakan langkah berikutnya. |
| **Completed** | Peserta yang mencapai langkah **Exit** journey. |
| **Exited** | Peserta yang dikeluarkan dari journey sebelum menyelesaikannya — misalnya, pembeli yang menyelesaikan checkout di tengah urutan cart-abandonment, atau pelanggan yang berhenti berlangganan. |

Jika journey belum memiliki pendaftaran, keempat kartu akan menampilkan nol dan catatan mengingatkan Anda bahwa metrik akan muncul setelah pelanggan mulai masuk ke journey.

### Pendapatan yang diatribusikan

Kartu **Attributed revenue** bekerja dengan cara yang sama seperti [laporan campaign](campaign-reports) — Spwig menelusuri pesanan kembali ke klik pada tautan di email journey, atribusi click-through yang dikendalikan persetujuan yang sama seperti yang dijelaskan dalam [Attributed revenue](campaign-reports#attributed-revenue) di halaman tersebut. Catatan yang sama berlaku di sini: atribusi hanya click-through (hanya membuka tidak pernah mengatribusikan pendapatan), mengikuti model atribusi aktif dan jendela lookback toko Anda, menghormati persetujuan analitik, dan tidak bersifat retroaktif — journey hanya menampilkan pendapatan dari email yang dikirim setelah pelacakan atribusi diaktifkan untuk toko Anda.

Baris sub kartu memecah total menjadi:

- **Orders** — berapa banyak pesanan yang dikreditkan ke journey ini, digabungkan dari email di setiap langkah.
- **AOV** — nilai rata-rata pesanan di antara pesanan tersebut.
- **Revenue per enrollee** — pendapatan yang diatribusikan dibagi dengan total **Enrolled**. Journey tidak memiliki satu "pengeluaran" tunggal seperti campaign — ia berjalan secara berkelanjutan alih-alih memiliki biaya sekali — sehingga tidak ada angka ROAS di sini. **Revenue per enrollee** adalah ekuivalen terdekat: ukuran yang stabil dan dapat dibandingkan tentang seberapa efisien journey mengubah pendaftaran menjadi penjualan, yang dapat Anda lacak dari waktu ke waktu atau bandingkan dengan journey lain.

### Pendapatan per langkah

Ketika journey memiliki setidaknya satu langkah **Send email**, tabel **Revenue by step** memecah total lebih lanjut, satu baris per langkah, sehingga Anda dapat melihat email mana dalam urutan yang benar-benar menghasilkan nilai:

| Kolom | Apa yang ditunjukkan |
|--------|-------------------|
| **Langkah** | Email langkah tersebut, dengan label **A/B** jika langkah tersebut sedang menjalankan [uji coba A/B](ab-testing). |
| **Pendapatan** | Pendapatan yang diatribusikan dari pesanan yang dilacak kembali ke email langkah tersebut. |
| **Pesanan** | Jumlah pesanan di balik angka pendapatan tersebut. |
| **Dikirim** | Berapa kali email langkah ini telah dikirim. |
| **Dibuka** / **Klik** | Berapa dari pengiriman ini yang dibuka, dan berapa yang diklik. Spwig melacak pembukaan dan klik untuk setiap pengiriman langkah, baik yang biasa maupun yang A/B. |

Gunakan tabel ini untuk menemukan titik lemah dalam perjalanan yang sebelumnya sehat — misalnya, rangkaian sambutan di mana email pertama menghasilkan sebagian besar pendapatan dan langkah berikutnya berkontribusi sedikit mungkin bisa menjadi kandidat untuk tawaran yang lebih kuat atau penulisan ulang, daripada mengasumsikan keseluruhan rangkaian perlu direvisi.

## Tips

- Cara tercepat untuk memulai perjalanan penghapusan keranjang belanja, pemulihan pelanggan yang hilang, permintaan ulasan setelah pengiriman, atau pemberitahuan stok kembali adalah dengan menggunakan template awal — ketika Anda menyimpan perjalanan baru dengan salah satu pengatur lalu lintas ini, pemilih **Template** di [Journey Builder](/help/journey-builder) menawarkan alur yang sudah jadi (**Pemulihan keranjang yang ditinggalkan**, **Pemulihan pelanggan yang hilang**, **Permintaan ulasan setelah pengiriman**, atau **Pemberitahuan stok kembali**) yang bisa Anda sesuaikan daripada membangun dari awal.
- Mulailah setiap perjalanan sebagai **Rancangan** saat Anda membangun langkah-langkahnya, lalu ubah **Status** menjadi **Aktif** setelah Anda memeriksa email dan penundaan — tidak ada yang mendaftar hingga perjalanan tersebut aktif.
- Pertahankan **Hanya untuk Pelanggan** aktif untuk apa pun yang terkait dengan milestone satu kali (pendaftaran, pesanan pertama); nonaktifkan dengan periode cooldown yang masuk akal untuk apa pun yang seharusnya berulang, seperti rangkaian pasca-pesanan.
- Gunakan **Hanya untuk Segment** untuk menjalankan rangkaian sambutan yang berbeda untuk audiens tertentu — misalnya, segmentasi VIP menerima rangkaian yang lebih kaya dibandingkan yang lainnya.
- Atur waktu tunggu langkah pertama menjadi `0` jika Anda ingin email pertama dikirim segera setelah pengatur berjalan, daripada menunggu.
- Periksa daftar **Pendaftaran Perjalanan** setelah mengaktifkan perjalanan baru untuk memastikan pelanggan sebenarnya mendaftar dan maju melalui langkah-langkah mereka sesuai harapan.
- Menonaktifkan perjalanan (**Status: Dihentikan**) menghentikan pendaftaran baru tetapi tidak membatalkan pelanggan yang sudah sebagian jalan — mereka terus menerima langkah-langkah tersisa mereka.