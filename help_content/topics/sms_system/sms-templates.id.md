---
title: Sms Templates
---

Sms templates mengontrol teks dari setiap notifikasi yang toko Anda kirim ke pelanggan melalui pesan teks. Setiap template sesuai dengan acara tertentu — seperti konfirmasi pesanan atau pembaruan pengiriman — dan menggunakan variabel tempat penampungan yang diganti oleh Spwig dengan detail pesanan yang sebenarnya saat pesan dikirim.

Navigasikan ke **Sistem SMS > Sms Templates** untuk melihat dan mengedit template Anda.

![Daftar template SMS](/static/core/admin/img/help/sms-templates/templates-list.webp)

## Jenis template yang tersedia

Spwig menyertakan jenis template berikut yang sudah dibangun:

| Jenis Template | Saat dikirim |
|---------------|-----------------|
| Konfirmasi Pesanan | Saat pelanggan memesan |
| Pembaruan Pengiriman | Saat status pelacakan pesanan berubah |
| Pemberitahuan Pengiriman | Saat pesanan ditandai sebagai terkirim |
| Reset Kata Sandi | Saat pelanggan meminta reset kata sandi |
| Kode Verifikasi | Saat diperlukan kode satu kali untuk verifikasi akun |
| Struk POS | Saat penjualan diproses di terminal POS |
| Pemasaran | Untuk kampanye promosi (memerlukan persetujuan terpisah) |
| Kustom | Untuk setiap notifikasi lain yang Anda buat |

## Mengedit template

1. Navigasikan ke **Sistem SMS > Sms Templates**
2. Klik template yang ingin Anda edit
3. Perbarui bidang **Pesan** dengan teks yang diinginkan
4. Gunakan placeholder `{variabel}` untuk menyertakan informasi pesanan tertentu (lihat variabel di bawah)
5. Centang **Aktif** untuk mengaktifkan template — template tidak aktif tidak dikirim
6. Klik **Simpan**

![Mengedit template SMS](/static/core/admin/img/help/sms-templates/template-edit.webp)

## Menggunakan variabel

Variabel adalah placeholder yang ditulis dalam kurung kurawal — contohnya, `{nama}` atau `{nomor_pesanan}`. Saat Spwig mengirim pesan, ia mengganti setiap placeholder dengan nilai sebenarnya untuk pelanggan atau pesanan tersebut.

### Variabel umum

| Variabel | Diganti dengan |
|----------|---------------|
| `{nama}` | Nama depan pelanggan |
| `{nomor_pesanan}` | Nomor referensi pesanan |
| `{total}` | Jumlah total pesanan |
| `{nomor_pelacakan}` | Nomor pelacakan pengiriman |
| `{nama_toko}` | Nama toko Anda |
| `{kode}` | Kode verifikasi atau reset |

**Contoh pesan:**

```
Halo {nama}, pesanan Anda #{nomor_pesanan} telah dikonfirmasi. Total: {total}. Kami akan memperbarui Anda saat dikirim. - {nama_toko}
```

Saat dikirim, ini menjadi:

```
Halo Sarah, pesanan Anda #10045 telah dikonfirmasi. Total: $89.00. Kami akan memperbarui Anda saat dikirim. - The Garden Shop
```

> Hanya sertakan variabel yang tersedia untuk jenis template tertentu. Contohnya, `{nomor_pelacakan}` tersedia dalam template Pembaruan Pengiriman tetapi tidak dalam template Reset Kata Sandi. Jika Anda menggunakan variabel yang tidak tersedia, variabel tersebut akan muncul seperti itu (tidak diganti) dalam pesan.

## Batas karakter dan panjang pesan

Pesan SMS standar dibatasi hingga **160 karakter** untuk satu segmen. Pesan yang lebih panjang dibagi menjadi beberapa segmen dan dikirim sebagai satu (SMS yang dikaitkan), tetapi penyedia layanan menghitung setiap segmen secara terpisah untuk keperluan pembayaran.

**Tips untuk tetap berada dalam batas:**
- Pertahankan pesan singkat — satu tujuan per pesan
- Singkatkan frasa umum secara alami (misalnya, "Ord" alih-alih "Order")
- Hindari kata pengisi yang tidak perlu

Spwig tidak menerapkan batas karakter keras di editor, jadi hitung karakter Anda (termasuk nilai variabel) sebelum menyimpan.

## Mengaktifkan dan menonaktifkan template

Toggle **Aktif** pada setiap template mengontrol apakah jenis notifikasi tersebut dikirim. Jika template tidak aktif, Spwig akan melewatkan pengiriman notifikasi tersebut sepenuhnya — pesan akan muncul sebagai **Dilewati** di Kotak Keluar SMS dengan alasan `template_inactive`.

Untuk mengaktifkan template:
1. Buka template
2. Centang kotak **Aktif**
3. Simpan

Untuk menonaktifkan (berhenti mengirim jenis notifikasi tanpa menghapus template):
1. Buka template
2. Nonaktifkan **Aktif**
3. Simpan

## Tips

Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis.

- Tulis pesan dengan nada yang sama dengan merek Anda — SMS adalah saluran langsung dan pribadi, jadi nada yang ramah bekerja dengan baik
- Selalu sertakan nama toko Anda dalam pesan agar pelanggan tahu siapa yang mengirimkan pesan mereka
- Pertahankan pesan konfirmasi pesanan agar singkat: nomor pesanan, total, dan catatan tentang langkah selanjutnya sudah cukup
- Uji pesan dengan menempatkan pesanan uji di toko Anda sendiri (menggunakan nomor telepon yang Anda kendalikan) untuk melihat pesan apa yang diterima pelanggan
- Jika notifikasi menghasilkan kebingungan atau keluhan, nonaktifkan template tersebut dan perbarui daripada menghapusnya — dengan demikian Anda dapat mengaktifkannya kembali setelah diperbarui
- Template pemasaran hanya boleh dikirimkan kepada pelanggan yang secara eksplisit telah mendaftar untuk pemasaran SMS, sesuai dengan regulasi telekomunikasi di sebagian besar negara