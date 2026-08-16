---
title: Penentuan Pendapatan
---

Penentuan pendapatan menunjukkan kepada Anda di mana penjualan sebenarnya berasal — bukan hanya tautan terakhir yang diklik pelanggan sebelum membeli, tetapi setiap saluran yang berkontribusi dalam mendatangkan mereka. Jika seorang pelanggan membaca artikel blog yang Anda bagikan di media sosial, kemudian kembali seminggu kemudian melalui pencarian Google, lalu akhirnya membeli setelah mengklik tautan dalam email, ketiga sentuhan tersebut berkontribusi terhadap penjualan ini. Dashboard ini memberi semua kontribusi tersebut, menggunakan model yang Anda pilih, sehingga Anda dapat melihat pemasaran Anda seperti yang sebenarnya bekerja, bukan seperti yang 

| Model | Yang Diberikan | Paling Cocok Untuk |
|-------|---------------|----------|
| **Satu Sentuhan Terakhir** | Memberikan seluruh kredit kepada saluran terakhir sebelum pesanan, mengabaikan sentuhan sebelumnya (kecuali kunjungan langsung murni, yang dilewati demi sumber terakhir nyata) | Pandangan yang cepat dan familiar — bagaimana alat analitik dasar melaporkan pendapatan |
| **Sentuhan Pertama** | Memberikan seluruh kredit kepada saluran mana pun yang pertama kali membawa pelanggan ke toko Anda | Memahami apa yang mendorong penemuan pelanggan baru dan pertumbuhan di bagian atas funnel |
| **Linear** | Membagi kredit secara merata di setiap sentuhan dalam perjalanan | Pandangan yang seimbang, tanpa pendirian ketika Anda tidak ingin satu saluran diunggulkan |
| **Penurunan Waktu** | Memberikan lebih banyak kredit kepada sentuhan yang lebih dekat dengan pesanan, dan sedikit untuk sentuhan yang lebih jauh |
| **Posisi 40/20/40** | Memberikan 40% kredit kepada sentuhan pertama, 40% kepada sentuhan terakhir, dan membagi 20% tersisa di antara semuanya | Mengakui baik "siapa yang menemukan kami" dan "siapa yang menyelesaikan penjualan" sambil tetap memberi kredit pada bagian tengah perjalanan |

Tidak ada model "yang benar" — masing-masing menjawab pertanyaan yang berbeda. Pendekatan umum adalah memeriksa **Sentuhan Pertama** untuk melihat apa yang mendorong penemuan, lalu **Satu Sentuhan Terakhir** atau **Posisi 40/20/40** untuk melihat apa yang mendorong konversi, dan menggunakan kedua pandangan ini bersamaan daripada memilih satu dan mengabaikan yang lain.

## Membaca Strip KPI

Di bawah pengganti model, empat angka menyimpulkan periode yang dipilih dan modelnya:

- **Pendapatan yang Ditetapkan** — total pendapatan yang diberi kredit di seluruh saluran untuk model saat ini. Ini memiliki label **Mengimbangi ke pendapatan bersih** ketika angka-angka tersebut sesuai dengan pendapatan bersih toko Anda untuk periode tersebut — dengan kata lain, model ini membagi pendapatan nyata antara saluran, bukan menciptakan atau kehilangan salah satu darinya.
- **Pesanan** — berapa banyak pesanan yang masuk dalam rentang tanggal yang dipilih.
- **Rata-rata sentuhan / pesanan** — jumlah rata-rata sentuhan yang dicatat per pesanan. Angka di atas 1 memastikan bahwa sebagian besar perjalanan pelanggan Anda melibatkan lebih dari satu kunjungan, itulah sebabnya penilaian multi-sentuh penting bagi toko Anda.
- **Saluran Utama** — saluran mana pun yang saat ini memiliki bagian terbesar dari pendapatan yang ditetapkan di bawah model yang dipilih, dengan persentase bagiannya dan pendapatannya.

## Pendapatan Berdasarkan Saluran

Kartu **Pendapatan Berdasarkan Saluran** menunjukkan batang horizontal untuk setiap saluran, yang ukurannya didasarkan pada pendapatan yang ditetapkan. Alihkan model penilaian dan lihat batang-batang tersebut secara halus berpindah sesuai peringkat — ini adalah pendapatan yang sama, hanya saja dibagi ulang berdasarkan aturan yang berbeda, jadi saluran yang terlihat kuat di bawah **Satu Sentuhan Terakhir** mungkin akan turun beberapa tempat di bawah **Sentuhan Pertama** jika sebagian besar perannya hanya sebagai pendukung.

## Pendapatan dari Waktu ke Waktu

Grafik **Pendapatan dari Waktu ke Waktu** menumpuk pendapatan yang ditetapkan berdasarkan saluran di setiap hari dalam rentang yang dipilih, sehingga Anda dapat melihat tidak hanya seberapa besar masing-masing saluran tetapi juga kapan saluran tersebut berkontribusi. Gunakan untuk menemukan pola musiman, memastikan dampak kampanye jatuh pada hari-hari yang Anda harapkan, atau memeriksa apakah kontribusi saluran tersebut tumbuh atau menghilang sepanjang periode tersebut.

## Bagaimana Pelanggan Sebenarnya Datang

Panel **Bagaimana Pelanggan Sebenarnya Datang** adalah peta alur yang menghubungkan saluran yang pertama kali membawa pelanggan masuk (di sebelah kiri) dengan saluran yang ada saat mereka melakukan konversi (di sebelah kanan). Pita yang lebih tebal berarti pendapatan yang lebih banyak mengalir melalui jalur tersebut. Ini adalah cara yang paling jelas untuk melihat perjalanan multi-langkah secara sekilas — misalnya, pita yang tebal dari Pencarian Organik ke Email memberi tahu Anda bahwa pencarian menarik orang, tetapi pemasaran email Anda yang membawa mereka kembali untuk membeli.

![Grafik alur pelanggan, dengan lensa yang dipilih, menunjukkan saluran sentuhan pertama di sebelah kiri yang mengalir ke saluran di mana setiap pesanan selesai](/static/core/admin/img/help/revenue-attribution/journey-flow-sankey.webp)

Gunakan tombol **Ditetapkan** / **Dipengaruhi** di atas grafik untuk beralih antara lensa:

- **Ditandatangani** membagi pendapatan setiap pesanan di sepanjang model yang Anda pilih, sehingga totalnya menjadi 100% dari pendapatan yang ditandatangani — angka yang sama yang ditampilkan di bagian lain dari dashboard.
- **Dipengaruhi** memberi *setiap* saluran yang menyentuh pesanan dengan *seluruh* nilai pesanan tersebut, dihitung sekali per pesanan.

Ini secara sengaja tidak menambahkan hingga 100% — sebuah saluran dapat "dipengaruhi" oleh pendapatan yang juga dihitung penuh untuk saluran lainnya.

Tujuannya adalah untuk menunjukkan jangkauan saluran yang sebenarnya, yang sepenuhnya disembunyikan oleh pelacakan klik terakhir, seperti artikel blog atau bagian share media sosial yang membuat seseorang tertarik meskipun mereka tidak mengkliknya pada kunjungan terakhir mereka.

## Kampanye

Tabel **Kampanye** ini menjelaskan pendapatan, pesanan, dan nilai rata-rata pesanan (AOV) untuk setiap kampanye yang Anda tandai — tautan atau kode yang telah Anda beri nama kampanye, termasuk kode voucher yang ditandai kampanye (lihat [Ide Kampanye Voucher](/bantuan/ide-kampanye-voucher)). Gunakan untuk membandingkan bagaimana promosi individu, kode influencer, atau dorongan pemasaran masing-masing berkinerja satu sama lain, terlepas dari saluran mana yang membawanya.

## Rentang tanggal dan mengekspor data Anda

Gunakan pengatur rentang tanggal di sebelah kanan atas untuk beralih antara **7 hari terakhir**, **14 hari terakhir**, **30 hari terakhir**, **90 hari terakhir**, dan **Bulan ini**. Seluruh dashboard akan memperbarui untuk periode baru.

Klik **Ekspor CSV** untuk mengunduh pembagian saluran untuk model dan rentang tanggal yang saat ini dipilih — berguna untuk menarik angka ke spreadsheet atau berbagi dengan agen mitra.

## Bagaimana sentuhan tercatat

Spwig secara otomatis menangkap sentuhan setiap kali pengunjung tiba di toko Anda dengan membawa sinyal sumber yang dapat dikenali, dan hanya ketika pengunjung telah memberi **izin Analitik** di banner cookie toko Anda (jika Anda tidak menjalankan banner izin, pelacakan diaktifkan secara default, sesuai dengan kebijakan toko Anda sendiri). Hal ini menjaga atribusi pendapatan pada tingkat privasi yang sama dengan bagian lain dari analitik toko Anda.

Beberapa sumber ditandai secara otomatis, tanpa perlu penyiapan apapun:

| Saluran | Cara pengidentifikasi |
|---------|----------------------|
| **Email** | Tautan dalam email pemasaran Anda (bukan email pesanan atau pengiriman) |
| **Pencarian Organik / Berbayar** | Referrer mesin pencari, atau nilai `utm_medium` yang menandai kampanye pencarian berbayar |
| **Media Sosial Organik / Berbayar** | Referrer jejaring sosial, atau nilai `utm_medium` media sosial |
| **Afiliasi** | Tautan yang dihasilkan melalui program Afiliasi Anda |
| **Undang Teman** | Tautan yang dihasilkan melalui program undangan pelanggan Anda |
| **Kampanye** | Tautan atau kode apa pun yang membawa tag kampanye, termasuk kode voucher yang ditandai kampanye |
| **Tautan Eksternal** | Tautan masuk dari situs web lain yang tidak lain dikategorikan |
| **Langsung** | Tidak ada sinyal sumber yang hadir — pengunjung mengetik alamat Anda, menggunakan tanda buku, atau tiba dari aplikasi tanpa referrer |

Postingan blog yang secara otomatis dibagikan ke akun media sosial terkait Anda secara otomatis ditandai, sehingga lalu lintas yang dihasilkannya muncul di saluran media sosial yang benar, bukan hilang ke Saluran Langsung atau Tautan Eksternal.

Anda juga dapat menandai tautan Anda sendiri secara manual dengan menggunakan parameter standar `utm_source`, `utm_medium`, dan `utm_campaign` pada URL mana pun yang menuju toko Anda — berguna untuk bahan cetak, newsletter mitra, atau saluran apa pun yang tidak ditandai otomatis oleh Spwig.

## Batasan yang perlu diperhatikan

- **Atribusi mengikuti browser, bukan seseorang.** Jika seorang pelanggan mencari di ponsel mereka dan membeli di laptop mereka, itu adalah dua perjalanan terpisah dari segi pelacakan — tidak ada cara untuk menghubungkan aktivitas di perangkat berbeda.


Ini berarti beberapa kredit yang 'seharusnya' diberikan ke sentuhan sebelumnya di perangkat lain akan mendarat di Direct.
- **Direct adalah tempat di mana pendapatan yang tidak terlacak berada.** Persentase Direct yang tinggi tidak selalu berarti seseorang mengetik URL Anda dari ingatan — bisa juga berarti sentuhan awal pelanggan terjadi di perangkat berbeda, atau tautan yang digunakan tidak diberi label.
- **Tolak izin berarti tidak ada sentuhan yang dicatat.** Pengunjung yang menolak izin analitik di banner cookie Anda tidak dilacak, jadi pesanan mereka akan muncul sebagai Direct bahkan jika mereka tiba melalui saluran yang biasanya Anda kenali.

## Tips

- Periksa lebih dari satu model sebelum menarik kesimpulan — saluran yang tampak lemah di bawah **Satu Sentuhan Terakhir** bisa menjadi pengemudi penemuan terkuat di bawah **Satu Sentuhan Pertama**.
- Jika **Direct** menyumbang bagian besar pendapatan Anda, lihat apakah lebih banyak tautan pemasaran Anda yang bisa diberi label `utm_source`/`utm_medium`/`utm_campaign` — lalu lintas yang tidak diberi label tidak punya tempat lain untuk mendarat.
- Gunakan lensa **Dipengaruhi** pada diagram alur perjalanan saat Anda memutuskan apakah akan terus berinvestasi di saluran seperti pencarian organik atau konten blog yang jarang mendapatkan klik terakhir tetapi secara konsisten memulai perjalanan.
- Bandingkan **Rata-rata sentuhan / pesanan** seiring waktu — jumlah yang meningkat biasanya berarti pelanggan menghabiskan waktu lebih lama untuk memutuskan, yang merupakan sinyal yang berguna saat merencanakan email lanjutan atau penargetan ulang.
- Ekspor CSV untuk model dan periode yang Anda laporkan sebelum Anda beralih kembali ke model lain, karena ekspor mencerminkan model mana pun yang dipilih saat Anda menekan **Ekspor CSV**.