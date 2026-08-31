---
title: Journey Builder
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/  (open any journey's builder, click Templates)
  filename: journey-builder-templates.webp
  description: The template picker with all eight starters visible (Welcome series,
    First-order onboarding, Post-purchase & review, VIP vs. standard offer, Abandoned
    cart recovery, Win-back lapsed customers, Post-delivery review request,
    Back-in-stock alert) — replaces the existing four-template screenshot at the same
    path, which is now stale.
  save-to: core/static/core/admin/img/help/journey-builder/
  viewport: 1440x900
-->

**Journey Builder** adalah kanvas visual drag-and-drop tempat Anda merancang apa yang sebenarnya dilakukan oleh [Journey](/help/triggered-journeys) — email mana yang dikirim, berapa lama menunggu di antara email, dan apakah subscriber yang berbeda harus mengikuti jalur yang berbeda. Alih-alih mengisi formulir, Anda membangun alur sebagai diagram alir: kotak-kotak yang terhubung di kanvas yang dapat Anda atur ulang, cabangkan, dan pratinjau sekilas.

## Membuka builder

Setiap journey memiliki kanvas builder-nya sendiri. Anda dapat mengaksesnya dengan dua cara:

- Membuat journey baru — isi **Name**, **Trigger**, dan audiens di halaman pengaturan lalu klik **Save** — akan langsung membawa Anda ke builder sehingga Anda dapat mulai merancang segera.
- Membuka halaman pengaturan journey yang sudah ada dan mengklik **Design journey** di bagian atas.

Builder adalah ruang kerja layar penuh dengan tiga area: **palette** jenis langkah di sebelah kiri, **canvas** di tengah, dan panel **step settings** di sebelah kanan yang muncul ketika Anda memilih sesuatu.

![Kanvas Journey Builder yang menampilkan welcome series dengan cabang Yes/No](/static/core/admin/img/help/journey-builder/journey-builder-canvas.webp)

Di bagian atas kanvas, header mengulang **Trigger** dan **audience** journey (atau "All subscribers" jika tidak ada segmen yang diatur) sehingga Anda selalu tahu untuk siapa Anda merancang tanpa harus keluar dari builder. Gunakan tombol **Back** untuk kembali ke halaman pengaturan journey.

## Jenis langkah

Seret langkah dari palette di sebelah kiri ke kanvas, atau klik item palette untuk meletakkannya secara otomatis. Empat jenis langkah tersedia:

| Langkah | Fungsinya |
|------|--------------|
| **Send email** | Mengirim salah satu campaign Anda ke subscriber. |
| **Wait** | Menunda untuk jumlah jam atau hari tertentu sebelum melanjutkan. |
| **Branch** | Membagi jalur menjadi dua — **Yes** atau **No** — berdasarkan apakah subscriber termasuk dalam segmen yang Anda pilih. |
| **Exit** | Mengakhiri journey untuk subscriber. |

Setiap journey dimulai dengan satu langkah **Entry**, yang dibuat secara otomatis pertama kali Anda membuka builder. Langkah ini menampilkan trigger journey dan tidak dapat dihapus — ini hanyalah tempat subscriber masuk ke alur.

## Menghubungkan langkah

Setiap langkah memiliki **port** kecil berbentuk lingkaran: satu di atas (input) dan satu atau lebih di bawah (output). Untuk menghubungkan dua langkah, seret dari port bawah satu langkah ke port atas langkah lainnya — garis lengkung akan muncul menghubungkannya.

Langkah **Branch** memiliki dua port output alih-alih satu: **Yes** berwarna hijau dan **No** berwarna merah. Hubungkan masing-masing ke tempat jalur tersebut harus menuju — mereka dapat bergabung kembali di langkah yang sama nanti (seperti dalam contoh di atas, di mana kedua jalur kembali ke **Exit** yang sama) atau benar-benar berjalan ke arah yang berbeda.

Untuk mengatur ulang tata letak, seret langkah melalui badannya untuk memposisikannya kembali — garis yang terhubung akan mengikuti secara otomatis. Seret bagian kosong dari latar belakang kanvas untuk berpindah, dan gunakan roda gulir untuk memperbesar atau memperkecil. Jika Anda kehilangan jejak alur, klik **Fit** di toolbar untuk memusatkan kembali dan memperbesar agar semuanya muat di layar.

## Mengonfigurasi langkah

Klik langkah mana pun untuk membuka pengaturannya di panel sebelah kanan:


{
  "Step": "Pengaturan",
  "------": "---------",
  "**Kirim email**": "Pilih **Email yang dikirim** dari daftar kampanye Anda.",
  "**Tunggu**": "Atur **Tunggu untuk** — angka ditambah **jam** atau **hari**.",
  "**Cabang**": "Pilih **Jika pelanggan termasuk dalam segment** — segment yang menentukan Ya vs. Tidak.",
  "**Keluar**": "Tidak ada pengaturan — hanya sebagai titik akhir."
}

![Panel sebelah kanan yang mengkonfigurasi langkah Cabang, dengan kanvas yang redup di belakangnya](/static/core/admin/img/help/journey-builder/journey-builder-branch-config.webp)

Perubahan disimpan secara otomatis begitu Anda memilih nilai — tidak ada tombol **Simpan** terpisah di kanvas. Setiap langkah kecuali **Masuk** memiliki tombol **Hapus langkah** di bagian bawah panel pengaturannya.

Email yang Anda pilih untuk langkah **Kirim email** adalah kampanye biasa yang Anda buat di pembuat visual biasa Campaign Studio — subjek, blok konten, semuanya. Biarkan mereka sebagai **Draf** dan pilih saja dari daftar turunan di sini; perjalanan ini akan mengirimkannya untuk Anda, Anda tidak pernah mengklik Kirim sendiri.

## Memulai dari sebuah template

Membangun alur dari kanvas kosong tidak selalu diperlukan — klik **Template** di bilah alat (atau **Jelajahi template** pada kanvas kosong) untuk membuka pemilih dengan delapan starter siap pakai:

| Template | Apa yang dibangun |
|----------|-----------------|
| **Serangkaian Selamat Datang** | Sambut pelanggan baru, bagikan apa yang Anda tawarkan, lalu dorongan pesanan pertama. |
| **Onboarding pesanan pertama** | Ubah pembeli pertama kali menjadi pelanggan berulang dengan urutan onboarding yang lembut. |
| **Pascapembelian & permintaan ulasan** | Ucapkan terima kasih setelah pesanan apa pun, lalu minta ulasan setelah pesanan tiba. |
| **Tawaran VIP vs. standar** | Setelah pesanan, cabang pada segment VIP untuk mengirim tawaran lanjutan yang sesuai kepada setiap kelompok. |
| **Pemulihan troli yang ditinggalkan** | Ingatkan pembeli yang meninggalkan barang, lalu ingatkan lanjutan sehari kemudian. |
| **Pemulihan pelanggan yang lama** | Mengaktifkan kembali pelanggan yang tidak membeli dalam waktu lama dengan alasan untuk kembali. |
| **Permintaan ulasan setelah pengiriman** | Minta ulasan beberapa hari setelah pesanan dicatat sebagai Diterima. |
| **Pemberitahuan ketersediaan ulang** | Beri tahu pembeli yang menunggu saat produk yang mereka inginkan tersedia kembali. |

Setiap template sudah terhubung dengan pengaturan yang sesuai — misalnya, menerapkan **Pemulihan pelanggan yang lama** ke perjalanan baru juga mengharapkan **Pemicu** perjalanan tersebut adalah **Pelanggan lama (pemulihan)**. Lihat [Perjalanan yang dipicu](/help/triggered-journeys) untuk mengetahui apa yang memicu setiap peristiwa ini dan bagaimana cara perilaku yang fokus pada pemulihan (jendela idle, checkout tamu, permintaan ulasan per pesanan, dan bagaimana perjalanan ketersediaan ulang menggantikan yang biasa).

![Pemilih template menunjukkan perjalanan starter siap pakai](/static/core/admin/img/help/journey-builder/journey-builder-templates.webp)

Menerapkan sebuah template **mengganti alur saat ini** di kanvas, jadi gunakan di awal desain perjalanan daripada sebelumnya. Spwig menghubungkan kembali masing-masing langkah ke email atau segment nyata di mana nama sesuai dengan sesuatu yang sudah Anda miliki; di mana pun tidak ada yang cocok, laporan header menunjukkan berapa banyak langkah yang masih membutuhkan email atau segment yang dipilih agar Anda tahu tepatnya apa yang perlu diselesaikan sebelum mengaktifkannya.

## Membagikan perjalanan

Dua tombol bilah alat memungkinkan Anda memindahkan desain perjalanan antara langkah atau antara toko:

- **Ekspor** mengunduh perjalanan sebagai file `.journey.json` — deskripsi portabel dari bentuk alur (langkah-langkahnya, menunggu, cabang, dan jalur Ya/Tidak) ditambah *nama* email dan segment yang digunakan masing-masing langkah. Tidak termasuk desain email itu sendiri atau data pelanggan apa pun.
- **Impor** memuat file `.journey.json` ke dalam perjalanan saat ini, mengganti apa pun yang ada di kanvas.

Ini berguna untuk cadangan alur yang Anda banggakan, menyerahkan rangkaian selamat datang yang terbukti ke toko Spwig lain, atau membangun kembali perjalanan setelah menyalin toko Anda ke instalasi baru.

Jaga semua format markdown, jalur gambar, blok kode, dan istilah teknis.

Seperti halnya template, Spwig kembali menghubungkan email dan segmentasi dengan nama di mana terdapat kecocokan pada toko tujuan, dan menandai segala sesuatu yang tidak dapat dicocokkan sehingga Anda dapat menyelesaikan pemasangan.

## Mengaktifkan perjalanan Anda

Ketika alur siap, gunakan kontrol status di bagian kanan atas builder. Sebuah label menunjukkan status saat ini perjalanan — **Rancangan**, **Aktif**, atau **Jeda** — di sebelah tombol **Aktifkan**.

Mengklik **Aktifkan** akan **memeriksa alur terlebih dahulu**. Jika ada sesuatu yang akan menghentikan kerja alur tersebut, aktivasi akan diblokir dan sebuah banner akan mendaftar masalahnya — misalnya, langkah **Kirim email** tanpa email yang dipilih, **Cabang** tanpa segmentasi atau jalur Ya/Tidak, email atau segmentasi yang telah dihapus, atau loop yang akan berjalan terus-menerus. Setiap masalah dapat diklik: memilihnya akan melompat ke langkah yang menyebabkan masalah, yang akan dikelilingi warna merah hingga Anda memperbaikinya. Peringatan (seperti langkah yang tidak terjangkau atau **Tunggu** tanpa penundaan yang ditetapkan) juga akan didaftar tetapi tidak menghalangi aktivasi.

![Aktivasi diblokir, dengan masalah yang tercantum dalam banner dan langkah yang menyebabkan masalah dikelilingi warna merah](/static/core/admin/img/help/journey-builder/journey-builder-activate-blocked.webp)

Setelah alur lulus, label berubah menjadi **Aktif** dan perjalanan mulai mendaftarkan pelanggan kapan pun adegan pemicunya berjalan. Tombolnya menjadi **Jeda**, yang menghentikan pendaftaran baru — pelanggan yang sudah sebagian besar menyelesaikan langkah tetap menerima langkah tersisa mereka. Lihat [Perjalanan yang Dipicu](/help/triggered-journeys) untuk bagaimana pendaftaran, masa pendinginan, dan status saling terkait.

## Melihat siapa saja yang ada dalam perjalanan

Setelah perjalanan hidup, setiap langkah menunjukkan **badge jumlah** kecil di sudutnya: jumlah pelanggan yang sedang berada di langkah tersebut saat ini. Ini adalah cara cepat untuk melihat di mana orang-orang mengalir dan di mana mereka menumpuk — jumlah besar pada langkah **Tunggu** adalah hal yang biasa, sedangkan penumpukan di sebelum email tertentu mungkin layak untuk dilihat. Jumlahnya akan diperbarui ketika Anda kembali ke tab builder.

![Kanvas dengan badge jumlah yang hidup pada langkah-langkah dan tombol Aktifkan di bilah alat](/static/core/admin/img/help/journey-builder/journey-builder-live-counts.webp)

## Tips

- Rancang alur saat masih dalam bentuk **Rancangan** — tidak ada yang mendaftar sampai Anda **Aktifkan**. Mengaktifkan dari builder akan menjalankan pemeriksaan cepat terlebih dahulu dan tidak akan membiarkan alur yang rusak berjalan, jadi tidak ada risiko perjalanan yang belum selesai mendaftarkan pelanggan.
- Mulai dari **Template** bahkan jika Anda berencana untuk mempersonalisasi secara signifikan — lebih cepat untuk mengedit alur yang sudah ada daripada membangun satu per satu, dan menunjukkan pola cabang jika Anda belum pernah menggunakannya sebelumnya.
- Setelah menerapkan template atau mengimpor file, periksa bagian atas untuk catatan langkah yang tidak cocok dan lengkapi langkah **Kirim email** atau **Cabang** yang tidak dapat dicocokkan sebelum mengaktifkannya.
- Klik **Sesuaikan** kapan pun alur menjadi lebar (terutama cabang) — ini adalah cara tercepat untuk melihat bentuk keseluruhan kembali setelah memperbesar atau menggeser layar.
- Pertahankan nama langkah yang mudah dicari dengan menempatkan setiap **Tunggu** tepat sebelum email yang ditunda, bukan mengelompokkan beberapa tunggu bersamaan.
- **Ekspor** perjalanan yang berjalan sebelum membuat perubahan besar pada perjalanan tersebut — ini adalah cara cepat untuk menjaga salinan cadangan yang dapat Anda impor kembali jika hasilnya tidak Anda sukai.