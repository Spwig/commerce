---
title: Kemasan Pengiriman
---

Kemasan pengiriman mendefinisikan ukuran kotak dan amplop yang ditetapkan sebelumnya untuk perhitungan tarif dan pengemasan otomatis—tentukan dimensi internal (ruang yang dapat digunakan), ketebalan dinding (dimensi eksternal untuk API penyedia pengiriman), batas berat, dan biaya pengemasan. Penyedia pengiriman menggunakan dimensi eksternal untuk menghitung berat dimensi agar mendapatkan kutipan tarif yang akurat. Kemasan memiliki urutan prioritas untuk algoritma pengemasan otomatis yang memilih kombinasi kemasan optimal untuk menampung barang di keranjang.

Konfigurasikan kemasan saat menggunakan API penyedia pengiriman untuk tarif real-time atau saat Anda membutuhkan perhitungan berat dimensi yang akurat.

## Konfigurasi Kemasan

Setiap kemasan mendefinisikan:

**Dimensi**:
- **Panjang Internal**: Ruang yang dapat digunakan di dalam (cm)
- **Lebar Internal**: Ruang yang dapat digunakan di dalam (cm)
- **Tinggi Internal**: Ruang yang dapat digunakan di dalam (cm)
- **Ketebalan Dinding**: Ketebalan bahan pengemasan (cm)

**Dimensi Eksternal** (dihitung otomatis):
```
Panjang Eksternal = Panjang Internal + (2 × Ketebalan Dinding)
Lebar Eksternal = Lebar Internal + (2 × Ketebalan Dinding)
Tinggi Eksternal = Tinggi Internal + (2 × Ketebalan Dinding)
```

**Berat & Biaya**:
- **Berat Kosong**: Berat kemasan kosong (gram)
- **Berat Maksimal**: Kapasitas beban maksimal (gram)
- **Biaya**: Biaya bahan pengemasan (untuk optimasi biaya)

**Properti**:
- **Nama**: Identifier kemasan (contoh, "Small Box", "Large Envelope")
- **Jenis**: Kotak atau Amplop
- **Prioritas**: Urutan pemilihan pengemasan otomatis (angka lebih kecil = prioritas lebih tinggi)
- **Aktif**: Toggle ketersediaan

---

## Mengapa Dimensi Eksternal Penting

Penyedia pengiriman menghitung **berat dimensi** dari dimensi eksternal:

**Rumus Berat Dimensi**:
```
Berat Dimensi = (Panjang × Lebar × Tinggi) / Pembagi

Pembagi Umum:
- DHL: 5000
- FedEx/UPS: 5000 (domestik), 6000 (internasional)
```

**Contoh**:
```
Kotak Kecil:
Internal: 20cm × 15cm × 10cm
Ketebalan Dinding: 0.5cm
Eksternal: 21cm × 16cm × 11cm

Berat Dimensi = (21 × 16 × 11) / 5000 = 0.74kg

Jika berat aktual = 0.5kg → Penyedia pengiriman menagih berdasarkan 0.74kg (berat dimensi lebih tinggi)
```

**Mengapa Akurasi Penting**: Dimensi tidak akurat → kutipan tarif tidak akurat → pelanggan dikenai biaya berlebihan atau terlalu rendah.

---

## Ukuran Kemasan Umum

### Lembaran Dengan Busa Kecil

```
Internal: 25cm × 18cm × 2cm
Ketebalan Dinding: 0.3cm
Berat Maksimal: 500g
Jenis: Amplop
Penggunaan: Dokumen, buku, perhiasan
```

### Kotak Kecil

```
Internal: 20cm × 15cm × 10cm
Ketebalan Dinding: 0.5cm
Berat Maksimal: 5kg
Jenis: Kotak
Penggunaan: Elektronik kecil, kosmetik, aksesori
```

### Kotak Sedang

```
Internal: 30cm × 25cm × 20cm
Ketebalan Dinding: 0.5cm
Berat Maksimal: 15kg
Jenis: Kotak
Penggunaan: Pakaian, sepatu, peralatan dapur
```

### Kotak Besar

```
Internal: 45cm × 35cm × 30cm
Ketebalan Dinding: 0.6cm
Berat Maksimal: 30kg
Jenis: Kotak
Penggunaan: Barang dalam jumlah besar, produk banyak, elektronik besar
```

---

## Algoritma Pengemasan Otomatis

Sistem secara otomatis memilih kemasan untuk barang di keranjang:

**Cara Kerjanya**:
1. Hitung total volume barang di keranjang
2. Urutkan kemasan berdasarkan prioritas (angka terkecil terlebih dahulu)
3. Coba masukkan barang ke dalam satu kemasan
4. Jika tidak cocok, coba ukuran kemasan berikutnya
5. Jika tidak ada satu kemasan yang cocok, gabungkan beberapa kemasan
6. Optimalkan berdasarkan pengaturan `optimize_for`

**Mode Optimasi**:
- **Biaya**: Minimalkan biaya pengemasan
- **Volume**: Minimalkan ruang yang terbuang
- **Jumlah**: Minimalkan jumlah kemasan

**Contoh**:
```
Barang di Keranjang:
- Item A: 10cm × 8cm × 5cm, 200g
- Item B: 15cm × 12cm × 8cm, 400g

Kemasan (berdasarkan prioritas):
1. Kotak Kecil (20×15×10, prioritas=1)
2. Kotak Sedang (30×25×20, prioritas=2)

Algoritma:
Coba Kotak Kecil: Kedua item cocok
Hasil: 1× Kotak Kecil (dioptimalkan untuk jumlah)
```

---

## Prioritas Kemasan

**Prioritas menentukan urutan pengemasan**:

Prioritas 1 (tertinggi): Kemasan kecil dicoba terlebih dahulu
Prioritas 10: Kemasan besar sebagai pilihan terakhir

**Strategi**:
- Kemasan kecil = angka prioritas rendah (1-3)
- Kemasan sedang = prioritas sedang (4-6)
- Kemasan besar = angka prioritas tinggi (7-10)

**Mengapa**: Mulai dengan kemasan terkecil, tingkatkan ukuran jika diperlukan → meminimalkan biaya pengiriman.

---

## Akurasi Ketebalan Dinding

Ukur kemasan sebenarnya:

**Cara Mengukur**:
1. Dapatkan kotak kosong
2. Ukur dimensi internal (dalam)
3. Ukur dimensi eksternal (luar)
4. Hitung: `(Eksternal - Internal) / 2 = Ketebalan Dinding`

**Contoh**:
```
Lebar Internal: 20cm
Lebar Eksternal: 21cm
Ketebalan Dinding: (21 - 20) / 2 = 0.5cm
```

**Ketebalan Umum**:
- Lembaran dengan busa: 0.2-0.4cm
- Karton satu dinding: 0.4-0.6cm
- Karton dua dinding: 0.8-1.0cm

---

## Membuat Preset Kemasan

**Langkah demi Langkah**:

1. Pengaturan > Pengiriman > Kemasan Pengiriman
2. Klik "Tambahkan Kemasan Pengiriman"
3. Masukkan nama (contoh, "Kotak Sedang")
4. Pilih jenis (Kotak atau Amplop)
5. Masukkan dimensi internal (L × W × H dalam cm)
6. Masukkan ketebalan dinding (cm)
7. Sistem menghitung otomatis dimensi eksternal
8. Masukkan berat kosong (berat kemasan kosong dalam gram)
9. Masukkan berat maksimal (kapasitas beban dalam gram)
10. Opsional: Masukkan biaya (untuk optimasi biaya)
11. Atur prioritas (1-10)
12. Toggle aktif = Ya
13. Simpan

---

## Uji Pemilihan Kemasan

**Uji Manual**:
1. Tambahkan produk ke keranjang uji
2. Lanjutkan ke checkout
3. Pilih metode pengiriman real-time (menggunakan kemasan)
4. Verifikasi kutipan tarif yang masuk akal
5. Periksa respons penyedia pengiriman (log API menunjukkan kemasan yang dipilih)

**Preview Pengemasan Otomatis**:
- Beberapa akun penyedia pengiriman menampilkan pemecahan kemasan
- Lihat kemasan yang dipilih untuk keranjang
- Verifikasi pengemasan optimal

---

## Tips

- **Ukur secara akurat** - Dimensi tidak akurat → kutipan tarif penyedia pengiriman tidak akurat
- **Sertakan ketebalan dinding** - Penting untuk berat dimensi
- **Mulai dengan 3-4 ukuran** - Ukuran kecil, sedang, besar menutupi kebanyakan skenario
- **Atur berat maksimal yang realistis** - Kapasitas kotak, bukan batas teoretis
- **Gunakan prioritas secara bijak** - Kotak kecil prioritas 1, kotak besar prioritas 10
- **Uji dengan produk nyata** - Verifikasi pengemasan otomatis memilih ukuran yang benar
- **Perbarui saat pengemasan berubah** - Supplier baru = ukur ulang dimensi
- **Pertimbangkan item khusus** - Item rapuh mungkin memerlukan ukuran kotak tertentu
- **Jaga kemasan aktif minimal** - Terlalu banyak opsi memperlambat algoritma pengemasan otomatis
- **Dokumentasikan pengemasan** - Catat produk mana yang cocok dengan kemasan mana

Ingat: Hanya kembalikan objek JSON dengan bidang "title" dan "content". Pertahankan semua format markdown, jalur gambar, blok kode, dan istilah teknis secara eksak seperti yang ditunjukkan di atas.