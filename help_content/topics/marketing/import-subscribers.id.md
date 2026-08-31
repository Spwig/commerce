---
title: Mengimpor Pelanggan dari CSV
---

Jika Anda sudah memiliki daftar langganan di tempat lain — alat email lama, spreadsheet daftar pendaftar newsletter, tumpukan catatan pameran — Anda tidak perlu menambahkan kontak tersebut ke Spwig satu per satu. Impor pelanggan dari Studio Kampanye membaca file CSV atau Excel dan menambahkan setiap kontak yang valid ke audiens Anda sekaligus, siap ditandai, segmentasi, dan dikirimkan email.

## Sebelum mengimpor: persetujuan

Setiap impor memerlukan kotak centang yang mengonfirmasi: **"Kontak-kontak ini setuju untuk menerima email pemasaran dari saya."** Ini bukan sekadar formalitas — hanya impor kontak yang sebenarnya sudah menyetujui email pemasaran dari Anda. Hal ini penting karena dua alasan:

- **Ini merupakan kewajiban hukum di sebagian besar tempat.** Mengirim email pemasaran ke orang-orang yang tidak pernah menyetujukannya melanggar hukum persetujuan di banyak yurisdiksi.
- **Ini melindungi pengiriman email Anda.** Mengirim email ke orang-orang yang tidak pernah menyetujukannya menghasilkan keluhan spam dan pembatalan, yang disediakan pihak penyedia email guna menentukan apakah *seluruh* email Anda — termasuk yang ditujukan ke orang-orang yang menyetujukinya — sampai ke kotak masuk.

Jika daftar tersebut tidak jelas berasal dari pendaftaran yang disetujui, jangan impor.

## Menyiapkan file Anda

Pengimpor menerima file `.csv` atau `.xlsx` dengan baris judul. Hanya satu kolom yang diperlukan:

| Kolom | Wajib? | Catatan |
|--------|-----------|-------|
| **Email** | Ya | Harus berupa alamat email yang valid. |
| **Nama depan** | Tidak | Digunakan untuk mempersonalisasi email. |
| **Nama belakang** | Tidak | Digunakan untuk mempersonalisasi email. |
| **Bahasa** | Tidak | Kode bahasa yang disukai pelanggan (misalnya `en`, `es`). |

Kolom-kolom ini secara otomatis dipasangkan dengan bidang-bidang ini berdasarkan nama judul, jadi Anda tidak perlu mengganti nama apa pun terlebih dahulu — variasi umum seperti `E-mail`, `Email Address`, `Nama Depan`, `Nama Lengkap`, `Nama Belakang`, atau `Lokal` semuanya dikenali.

Setiap impor dibatasi pada **5 MB** dan **5.000 baris**. Jika daftar Anda lebih besar dari itu, bagi menjadi file-filem yang lebih kecil dan impor satu per satu.

## Mengimpor kontak Anda

1. Buka **Studio Kampanye > Pelanggan** dan klik **Impor CSV**.
2. Pilih file `.csv` atau `.xlsx` Anda.
3. Tentukan apa yang akan terjadi **untuk kontak yang sudah ada di daftar Anda** — lihat [Penanganan duplikat](#penanganan-duplikat) di bawah ini.
4. Pilih opsi tag secara opsional di bawah **Tag kontak yang diimpor sebagai** untuk menandai semua orang dalam impor ini (misalnya, `Event 2026`) — lihat [Tag Pelanggan](/bantuan/tag-pelanggan) untuk informasi lebih lanjut tentang tag.
5. Centang **Kontak-kontak ini setuju untuk menerima email pemasaran dari saya**.
6. Klik **Lanjutkan**.

![Formulir unggah impor dengan file yang dipilih, tag yang dipilih, dan persetujuan dikonfirmasi](/static/core/admin/img/bantuan/impor-pelanggan/impor-form-unggah.webp)

Spwig kemudian menampilkan pratinjau sebelum apa pun yang diimpor:

![Pratinjau impor yang menunjukkan jumlah kontak baru, yang sudah ada, dan yang diabaikan karena tidak valid beserta alasan](/static/core/admin/img/bantuan/impor-pelanggan/impor-pratinjau.webp)

- **Kontak baru** — baris-baris yang akan menciptakan pelanggan baru.
- **Sudah ada di daftar Anda** — baris-baris yang alamat emailnya sesuai dengan pelanggan yang sudah ada.
- **Dilewati (tidak valid)** — baris-baris yang tidak dapat dibaca, masing-masing dicantumkan dengan nomor baris dan alasan (format email yang tidak valid, sel email kosong, atau duplikat dari baris sebelumnya dalam file yang sama).

Periksa jumlah ini, lalu klik **Impor sekarang** untuk mengonfirmasi impor, atau **Batal** untuk kembali tanpa mengubah apa pun.

## Menangani duplikat

Baris dianggap sebagai duplikat ketika alamat emailnya sesuai dengan pelanggan yang sudah Anda miliki. Anda memilih bagaimana Spwig menangani baris-baris ini di formulir unggah:

| Opsi | Apa yang terjadi |
|--------|----------------|
| **Biarkan mereka tetap tidak berubah** *(default)* | Nama dan bahasa pelanggan yang sudah ada tetap dipertahankan. |
| **Perbarui nama / bahasa mereka** | Nama depan, nama belakang, dan bahasa pelanggan yang sudah ada diperbarui dari file (hanya untuk bidang-bidang yang sebenarnya disediakan file tersebut). |

Tag yang Anda pilih untuk impor diterapkan ke **semua orang dalam file** — baik kontak baru maupun yang sudah ada — mana pun opsi duplikat yang Anda pilih.


Jadi, mengimpor "daftar VIP" Anda dengan tag **VIP** juga akan menandai orang-orang yang sudah Anda miliki.

Opsi duplikat hanya mengontrol apakah *nama dan bahasa* kontak yang sudah ada akan ditimpa.

## Setelah impor

Setiap kontak yang dibuat melalui impor dicatat dengan sumber **Import**, dan ditandai sebagai telah memberikan persetujuan pada saat Anda menjalankan impor (bukan tanggal sebelumnya yang mungkin mereka setujui di tempat lain). Nama depan dan nama belakang mereka — jika file menyediakannya — disimpan pada catatan pelanggan mereka, yang berarti bidang penggabungan `[[first_name]]` dan `[[last_name]]` dalam kampanye Anda sekarang akan mempersonalisasi dengan benar untuk mereka juga, meskipun mereka belum pernah membuat akun Spwig.

## Tips

- Ekspor daftar sumber Anda ke CSV atau `.xlsx` satu lembar dengan baris header yang bersih sebelum mengunggah — lembar tambahan, sel yang digabungkan, atau baris ringkasan dapat membingungkan pencocokan kolom.
- Gunakan **Tag kontak yang diimpor sebagai** untuk segera membuat audiens persis yang ingin Anda targetkan kemudian — lihat [Tag Pelanggan](/help/subscriber-tags) untuk membangun segmen darinya.
- Selalu baca alasan **Dilewati (tidak valid)** sebelum mengasumsikan impor gagal — beberapa baris yang dilewati dengan alasan yang jelas adalah hal normal untuk sebagian besar daftar dunia nyata.
- Menjalankan ulang file yang sama aman: kontak yang sudah Anda impor akan diperlakukan sebagai duplikat pada percobaan kedua, bukan dibuat ulang.
- Jika Anda mengonsolidasikan beberapa daftar kecil, beri tag setiap impor secara berbeda (misalnya `Import: Acara Jan`, `Import: Pameran Dagang`) agar Anda dapat membedakannya nanti meskipun semuanya sudah bercampur dengan audiens utama Anda.
- Untuk daftar lebih dari 5.000 baris, bagi berdasarkan batas yang jelas (alfabetis, berdasarkan sumber, atau berdasarkan tanggal pengumpulan) daripada pemotongan sewenang-wenang, agar setiap batch tetap mudah diidentifikasi kemudian.