---
title: Laporan Kampanye
---

<!-- screenshots-needed:
- url: /admin/campaigns/{campaign_id}/report/
  filename: engagement-over-time-chart.webp
  description: The report page scrolled to the "Engagement over time" chart card, with a campaign that has several days of send history so all three lines (Sent, Opened, Clicked) show a realistic shape.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: top-links-table.webp
  description: The report page's "Top links" card, with a campaign whose email contains at least 3 distinct links and a realistic spread of Clicks/Unique/CTR values.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipients-list.webp
  description: The Recipients page with the filters panel open and a mixed list of rows (some opened, some clicked, some bounced) so the engagement states are visibly distinct.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipient-activity-modal.webp
  description: The Recipients page with the "Recipient activity" modal open for a recipient who has multiple event types (delivered, opened, at least one clicked entry naming a link).
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: attributed-revenue-card.webp
  description: A close-up of the report page's "Attributed revenue" stat card, for a campaign with a logged Spend so the orders/AOV/revenue-per-email/ROAS sub-line is fully populated.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: dashboard-attributed-revenue-kpi.webp
  description: The Campaign Studio dashboard's stat card grid, scrolled/cropped to show the "Attributed revenue (30d)" tile alongside its neighboring cards, with a non-zero revenue figure.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: report-stat-cards.webp
  description: 'RECAPTURE NEEDED: the existing report-stat-cards.webp only shows 6 cards (Recipients, Delivered, Open rate, Click rate, Bounce rate, Spam complaints). The stat grid now has a 7th "Attributed revenue" card — recapture this shot with a campaign that has both attribution data and a logged Spend so all 7 cards are visible in a realistic state.'
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
-->

Setiap kampanye yang Anda kirim melalui Campaign Studio memiliki halaman **Report** (Laporan) tersendiri — ringkasan satu halaman tentang berapa banyak orang yang terjangkau, berapa banyak email yang benar-benar diterima, dan bagaimana penerima merespons. Gunakan halaman ini untuk memeriksa apakah pengiriman berjalan lancar, mendeteksi masalah ketercapaian (deliverability) sejak dini, atau membandingkan kinerja kampanye yang berbeda dari waktu ke waktu.

## Membuka laporan

Dari **Campaign Studio > Campaigns**, temukan kampanye yang ingin Anda periksa dan klik ikon grafik (**Report**) pada kartunya.

![Grid kartu statistik halaman laporan Kampanye, menunjukkan penerima, terkirim, tingkat buka, tingkat klik, tingkat pantulan, dan keluhan spam](/static/core/admin/img/help/campaign-reports/report-stat-cards.webp)

Laporan hanya akan menampilkan angka setelah kampanye benar-benar dikirim — kampanye yang masih dalam status **Draft** (Draf) akan menampilkan semua statistik sebagai nol, karena belum ada yang dapat diukur.

## Kartu statistik

| Kartu | Apa yang ditampilkan |
|------|---------------|
| **Penerima** | Berapa banyak pelanggan yang ditargetkan oleh kampanye ini, plus baris sub yang mencatat berapa banyak yang dilewati dan, dari jumlah tersebut, berapa yang dilewati secara khusus karena alamatnya ada di [daftar penekanan](list-hygiene). Pelanggaran tidak selalu berarti penekanan — Spwig juga melewatkan pelanggan yang tidak memiliki alamat email yang dapat digunakan, misalnya — sehingga kedua jumlah tersebut ditampilkan secara terpisah. |
| **Terkirim** | Berapa banyak email yang benar-benar diterima oleh server email penerima dan tidak pernah memantul kembali, plus **tingkat pengiriman** — pengiriman sebagai bagian dari setiap pengiriman yang *dicoba* oleh Spwig (diterima oleh server email atau penyedia Anda, terlepas dari apakah kemudian memantul). |
| **Tingkat pembukaan** | Bagian dari email *terkirim* yang dibuka, plus jumlah **dibuka** mentah. |
| **Tingkat klik** | Bagian dari email *terkirim* yang diklik, plus jumlah **diklik** mentah dan **tingkat klik-ke-pembukaan** — klik sebagai bagian dari pembukaan, sebuah pembacaan tentang seberapa menarik konten Anda bagi orang-orang yang sudah membukanya. |
| **Tingkat pantulan** | Bagian dari pengiriman *dicoba* yang memantul, dipecah menjadi pantulan **keras** dan **lunak**. |
| **Keluhan spam** | Berapa banyak penerima yang menandai email sebagai spam atau sampah, plus **tingkat keluhan** — keluhan sebagai bagian dari email *terkirim*. |
| **Pendapatan yang diatribusikan** | Pendapatan dari pesanan yang dapat ditelusuri kembali ke kampanye ini oleh Spwig, plus jumlah pesanan, nilai rata-rata pesanan (**AOV**), pendapatan per email terkirim, dan — setelah Anda mencatat biaya kampanye — **ROAS**-nya. Lihat [Pendapatan yang diatribusikan](#attributed-revenue) di bawah. |

## Mengapa tingkat menggunakan penyebut yang berbeda

Tingkat pembukaan, tingkat klik, dan tingkat keluhan semuanya diukur terhadap email **terkirim** — penerima yang benar-benar dapat melihat email — sementara tingkat pengiriman dan tingkat pantulan diukur terhadap pengiriman **dicoba**. Ini adalah praktik standar industri email, dan itulah mengapa tidak ada satu pun tingkat ini yang bisa membaca di atas 100%: email yang memantul tidak pernah terkirim, sehingga tidak dapat dihitung terhadap tingkat pembukaan atau klik Anda, dan email yang bahkan tidak pernah dicoba (pelanggaran) tidak dihitung terhadap salah satu dari mereka.

## Pantulan keras vs. pantulan lunak

- **Pantulan keras** — alamatnya tidak dapat dikirim secara permanen. Alamatnya tidak ada, atau domain menolak menerima email untuknya sama sekali.
- **Pantulan lunak** — masalah sementara: kotak masuk penuh, server penerima yang tidak tersedia untuk waktu singkat, dan sejenisnya. Pantulan lunak sering kali menyelesaikan diri sendiri.

Perhatikan pembagiannya, bukan hanya totalnya. Kenaikan jumlah **pantulan keras** biasanya berarti daftar Anda memiliki alamat yang usang atau salah ketik; kenaikan jumlah **pantulan lunak** lebih sering merupakan gangguan sementara di sisi penerima. Setiap pantulan keras, setiap keluhan spam, dan alamat yang mengumpulkan pantulan lunak berulang semuanya memberi makan [daftar penekanan](list-hygiene) otomatis Spwig — Anda tidak perlu bertindak sendiri, tetapi laporan adalah tempat Anda pertama kali akan memperhatikan lonjakan yang layak diselidiki.

## Pendapatan yang diatribusikan

Karena toko Anda dan Campaign Studio berada dalam sistem yang sama, Spwig tidak memerlukan platform analitik eksternal atau piksel pelacakan untuk memberi tahu Anda apakah kampanye benar-benar mendorong penjualan. Ketika pelanggan mengklik tautan di email kampanye ini dan mendarat di toko Anda, Spwig dapat mengikuti kunjungan tersebut hingga ke checkout dan mengkreditkan pendapatan pesanan yang dihasilkan kembali ke kampanye — itulah yang ditampilkan oleh kartu **Pendapatan yang diatribusikan**.

Baris sub kartu memecah angka tersebut lebih lanjut:

- **Pesanan** — berapa banyak pesanan yang dikreditkan ke kampanye ini.
- **AOV** — nilai rata-rata pesanan di antara pesanan-pesanan tersebut.
- **Pendapatan per email** — pendapatan yang diatribusikan dibagi dengan jumlah email *terkirim*, penyebut yang sama yang digunakan laporan untuk tingkat pembukaan dan tingkat klik.
- **ROAS** — pengembalian pada pengeluaran iklan, hanya ditampilkan setelah Anda memasukkan jumlah **Pengeluaran** pada kampanye itu sendiri.

Ini dihitung sebagai pendapatan yang diatribusikan dibagi dengan pengeluaran.

Jika pengeluaran dicatat dalam mata uang yang berbeda dari mata uang dasar toko Anda, Spwig menyembunyikan ROAS daripada menampilkan angka yang tidak sebanding — masukkan pengeluaran dalam mata uang dasar toko Anda untuk melihatnya.

Beberapa hal yang perlu diketahui tentang bagaimana angka ini dihitung:

- **Ini adalah klik, bukan terbuka.** Pelanggan harus mengklik tautan yang terlacak di email dan tiba di toko Anda — sekadar terbuka tidak per mai mengatributkan pendapatan. Hal ini sengaja dilakukan: pelacakan terbuka semakin tidak dapat dipercaya karena layanan seperti Apple Mail Privacy Protection yang secara otomatis memuat gambar untuk hampir setiap pesan, yang meningkatkan jumlah terbuka tanpa memandang apakah seseorang sebenarnya membaca email tersebut.
- **Ini mengikuti model penugasan toko Anda.** Secara default, ini adalah **satuan terakhir yang tidak langsung** dengan jendela 90 hari — klik yang sama harus mengarah ke pesanan dalam jendela ini untuk dihitung, dan kunjungan langsung berikutnya tidak akan menghapus kredit yang sudah diperoleh oleh klik kampanye ini.
- **Ini menghormati izin analitik.** Hanya pengunjung yang menerima izin analitik di banner cookie toko Anda yang dilacak (jika Anda tidak menjalankan banner izin, pelacakan mengikuti kebijakan default toko Anda sendiri). Seorang pelanggan yang menolak izin tetap bisa membeli — pesanan mereka hanya tidak akan diatributkan ke saluran mana pun, termasuk yang ini.
- **Ini tidak bersifat retroaktif.** Pelacakan pendapatan hanya mencakup kampanye yang dikirim setelah pelacakan penugasan diaktifkan untuk toko Anda. Sebuah kampanye yang dikirim sebelumnya akan menunjukkan pendapatan yang tidak teratribut di sini bahkan jika kampanye tersebut menghasilkan penjualan nyata, hanya saja Spwig tidak memiliki data klik yang dicatat untuknya.
- **Uji A/B dan kampanye berulang juga mengumpulkan pendapatan yang teratribut** — lihat [Laporan pada uji A/B](#reports-on-an-ab-test) di bawah ini.

Anda juga akan menemukan kartu **Pendapatan yang Teratribut (30d)** di dashboard Campaign Studio itu sendiri, yang menjumlahkan pendapatan yang teratribut dari email di setiap kampanye selama 30 hari terakhir — pemeriksaan cepat tanpa perlu membuka laporan individu. Untuk pandangan menyeluruh tentang toko, yang mencakup setiap saluran, bukan hanya email — pencarian organik, media sosial, afiliasi, dan lainnya — lihat dashboard [Pendapatan yang Teratribut](/help/revenue-attribution) di bawah **Insight**.

## Keterlibatan dari Waktu ke Waktu

Di bawah kartu statistik, grafik **Keterlibatan dari Waktu ke Waktu** memplotong tiga garis — **Dikirim**, **Dibuka**, dan **Diklik** — satu titik per hari, mencakup 30 hari terakhir hingga hari ini (atau kurang, jika kampanye belum mengirim sebanyak itu — grafik tidak per mai mulai lebih awal dari hari pengiriman kampanye pertama).

Beberapa hal yang perlu diketahui tentang bagaimana garis-garis ini dihitung:

- **Dibuka** dan **Diklik** menghitung setiap penerima sekali — hari pertama *pertama* kali mereka membuka atau *pertama* kali mengklik — bukan setiap kali mereka membuka ulang email atau mengklik tautan lagi. Hal ini mencegah grafik dari terdistorsi oleh sejumlah kecil orang yang membuka email yang sama secara berulang.
- Total dari grafik ini sesuai dengan kartu statistik di atasnya: **Dikirim** mencerminkan surat yang coba dikirim Spwig, sedangkan **Dibuka** dan **Diklik** diukur terhadap email yang dikirim, sama seperti kartu **tingkat pembukaan** dan **tingkat klik**.
- Grafik hanya muncul setelah kampanye memiliki setidaknya satu pengiriman yang tercatat — kampanye yang masih dalam **Rancangan** menampilkan pesan 

| Kolom | Apa yang ditampilkan |
|--------|---------------|
| **Tautan** | URL tujuan sebagaimana muncul di email Anda. |
| **Klik** | Total jumlah kali tautan tersebut diklik, termasuk klik berulang dari penerima yang sama. |
| **Unik** | Berapa banyak penerima berbeda yang mengklik tautan tertentu tersebut setidaknya sekali. |
| **CTR** | **Tingkat klik** tautan tersebut — jumlah **Unik** sebagai bagian dari email yang terkirim. Ini menggunakan penyebut yang sama dengan kartu **Tingkat klik** utama laporan, sehingga Anda dapat membandingkan daya tarik tautan tunggal secara langsung dengan kinerja klik keseluruhan kampanye. |

Jika email Anda menautkan beberapa produk atau campuran tombol ajakan bertindak, tabel ini adalah cara tercepat untuk melihat mana yang benar-benar mendapatkan klik — berguna untuk memutuskan apa yang akan ditampilkan lebih menonjol lain kali.

## Penerima

Klik **Penerima** di bagian atas laporan untuk membuka daftar lengkap yang dapat dicari dari semua orang yang dikirim kampanye ini, dengan hasil pengiriman dan keterlibatan masing-masing orang.

Dua cara untuk menyaring daftar:

- **Pencarian** — menyaring berdasarkan alamat email (cocok parsial berfungsi, jadi mengetik sebagian domain atau nama sudah cukup).
- **Keterlibatan** — menyaring ke satu status pada satu waktu: **Dibuka**, **Diklik**, **Terkirim, tidak dibuka**, atau **Memantul**. Biarkan pada **Semua** untuk melihat daftar lengkap.

Daftar menampilkan 100 penerima yang cocok terbaru pada satu waktu, yang terbaru terlebih dahulu — jumlah di atas daftar selalu mencerminkan total sebenarnya yang cocok dengan filter Anda saat ini, bahkan jika lebih besar dari yang ditampilkan. Untuk pengiriman besar, saring daftar dengan Pencarian atau Keterlibatan terlebih dahulu daripada menggulir melalui semua orang.

### Melihat garis waktu aktivitas penerima

Klik ikon aktivitas pada baris penerima mana pun untuk membuka garis waktu **Aktivitas penerima** mereka — setiap peristiwa yang dilacak untuk salinan email orang tersebut, secara berurutan: terkirim, dibuka, diklik (menyebutkan tautan mana), memantul (dengan alasan pantul), ditandai sebagai spam, atau berhenti berlangganan, masing-masing dengan stempel waktu sendiri.

Ini adalah cara tercepat untuk menjawab pertanyaan spesifik tentang satu pelanggan — misalnya, mengonfirmasi apakah pelanggan tertentu benar-benar menerima kampanye sebelum menindaklanjuti mereka melalui saluran lain, atau memeriksa tautan mana yang diklik pelanggan sebelum mereka melakukan pemesanan.

## Laporan pada uji A/B

Jika kampanye yang Anda lihat adalah wadah untuk [uji A/B](ab-testing), laporannya mengagregasi di seluruh **setiap varian** — seluruh pengujian, digabungkan, termasuk **Pendapatan yang diatribusikan** — bukan menampilkan satu varian secara terpisah. Untuk melihat bagaimana setiap varian individu berkinerja, buka halaman hasil pengujian itu sendiri, bukan laporannya. [Kampanye berulang](recurring-campaigns) bekerja dengan cara yang sama: laporannya merangkum setiap kejadian yang telah dikirim.

## Apa yang dianggap baik

Tidak ada satu angka sehat tunggal yang cocok untuk setiap toko atau daftar — audiens, industri, dan konten semua menggeser garis dasar — tetapi beberapa pola layak dipantau pada setiap kampanye:

- **Tingkat pantul** yang sebagian besar pantul lunak, dengan pantul keras yang jarang, menunjukkan daftar yang bersih dan terawat baik. Lonjakan tiba-tiba dalam pantul keras layak diselidiki sebelum pengiriman berikutnya Anda.
- **Keluhan spam** mendekati nol adalah tujuan pada setiap pengiriman. Keluhan merusak reputasi pengirim Anda lebih dari hampir hal lain — lihat [Kebersihan Daftar](list-hygiene) untuk mengapa mereka penting melampaui kampanye ini.
- **Tingkat klik-ke-buka** yang sehat relatif terhadap tingkat buka Anda memberi tahu Anda bahwa orang yang membuka menemukan konten layak untuk ditindaklanjuti — tingkat klik-ke-buka yang rendah bersamaan dengan tingkat buka yang kuat biasanya menunjukkan bahwa baris subjek bekerja lebih baik daripada konten di dalamnya.

## Tips

Simpan semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- Periksa laporan beberapa saat setelah pengiriman, bukan segera — pembukaan dan klik (serta beberapa laporan pantulan) dapat membutuhkan waktu untuk masuk dari penyedia email Anda.
- Jika **Delivered** terlihat lebih rendah dari yang diharapkan, periksa terlebih dahulu rincian lewati pada kartu **Recipients** — kumpulan lewati akibat penekanan sering kali merupakan cerita sebenarnya, bukan masalah pengiriman.
- Gunakan laporan untuk membandingkan kampanye dengan pengiriman Anda sendiri di masa lalu, bukan dengan angka industri generik — daftar, konten, dan audiens Anda adalah yang menentukan baseline realistis Anda.
- Lonjakan keluhan pada satu pengiriman tertentu layak mendapat pemeriksaan lebih dekat pada konten atau penargetan kampanye tersebut, bukan sekadar catatan untuk melanjutkannya.
- Untuk kampanye yang diuji A/B, baca laporan ini untuk hasil keseluruhan dan halaman [hasil uji A/B](ab-testing) untuk mengetahui varian mana yang sebenarnya menang dan berapa besar selisihnya.
- Gunakan tabel **Top links** untuk menemukan tautan yang paling banyak diklik, lalu periksa apakah itu sesuai dengan apa yang *Anda inginkan* agar penerima mengkliknya — jika tautan sekunder mengalahkan ajakan bertindak utama Anda, mungkin layak untuk memindahkannya lebih tinggi di email berikutnya.
- Filter **Opened** dan **Clicked** di halaman **Recipients** adalah cara cepat untuk membangun audiens tindak lanjut — misalnya, memeriksa siapa yang membuka tetapi tidak mengklik sebelum merencanakan pengiriman pengingat ke sisa daftar.
- Jika Anda membayar promosi di sekitar pengiriman — postingan sosial yang ditingkatkan, sorotan influencer, sewa daftar berbayar — catat sebagai **Spend** kampanye untuk membuka **ROAS** pada laporan.

Ini adalah cara tercepat untuk melihat jenis pengiriman mana yang sebenarnya layak diulang.