# Program-Pengolahan-Citra

Peningkatan kualitas citra digital menggunakan Python dengan berbagai fitur canggih.

## 🎯 Fitur Utama

### 1. Histogram Operations
- **Histogram Equalization**: Pemerataan histogram menggunakan OpenCV untuk meningkatkan kontras
- **Histogram Specification (Grayscale)**: Histogram matching untuk gambar grayscale
- **Histogram Specification (Color HSV)**: Mempertahankan warna dengan HSV color space
- **Histogram Specification (Color LAB)**: Mempertahankan warna dengan LAB color space
- **CLAHE (Adaptive Histogram)**: Contrast Limited Adaptive Histogram Equalization untuk enhancement lokal

### 2. Convolution (Mask Processing)
- **Smoothing**: Menghaluskan gambar dengan filter rata-rata 5x5 untuk mengurangi noise
- **Gaussian**: Menghaluskan gambar dengan filter Gaussian untuk hasil yang lebih natural
- **Sharpening**: Mempertajam detail gambar untuk meningkatkan ketajaman
- **Sobel Edge**: Mendeteksi tepi menggunakan operator Sobel
- **Laplacian**: Deteksi tepi menggunakan operator Laplacian untuk edge enhancement

### 3. Real-time Adjustments (Slider Interaktif)
- **Brightness**: Pengaturan kecerahan (-100 hingga +100)
- **Contrast**: Pengaturan kontras (0.5x hingga 3.0x)
- **Gamma Correction**: Koreksi gamma (0.1 hingga 3.0) untuk penyesuaian luminance
- Semua slider bekerja real-time tanpa perlu klik tombol

## 📦 Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Dependencies yang dibutuhkan:
- numpy (untuk operasi array dan matematika)
- opencv-python (untuk pemrosesan citra)
- Pillow (untuk manipulasi gambar)
- customtkinter (untuk GUI modern)

## 🚀 Cara Menggunakan

```bash
python image_enhancement_advanced.py
```

## 📖 Panduan Penggunaan

### 1. Load Image
Klik tombol **"📁 Load"** untuk memuat gambar dari komputer Anda.

### 2. Pilih Operasi Enhancement

#### Histogram Operations:
- **Equalization**: Untuk foto dengan kontras rendah
- **Spec (Gray)**: Histogram specification mode grayscale
- **Spec (HSV)**: Histogram specification dengan mempertahankan warna (HSV)
- **Spec (LAB)**: Histogram specification dengan mempertahankan warna (LAB)
- **CLAHE**: Untuk enhancement adaptif lokal

#### Convolution Filters:
- **Smoothing**: Untuk mengurangi noise pada foto
- **Gaussian**: Untuk blur yang lebih halus dan natural
- **Sharpening**: Untuk mempertajam detail foto
- **Sobel Edge**: Untuk deteksi tepi horizontal dan vertikal
- **Laplacian**: Untuk deteksi tepi semua arah

### 3. Real-time Adjustments
Gerakkan slider untuk menyesuaikan:
- **Brightness**: Membuat foto lebih terang atau gelap
- **Contrast**: Meningkatkan atau mengurangi perbedaan warna
- **Gamma**: Menyesuaikan kurva luminance

### 4. Save & Reset
- **💾 Save**: Simpan hasil pemrosesan
- **🔄 Reset**: Kembali ke gambar original

## 🎛️ Fitur Real-time Slider

- Gerakkan slider Brightness, Contrast, atau Gamma
- Hasil langsung terlihat tanpa perlu klik tombol
- Bisa dikombinasikan dengan operasi lain
- Reset otomatis saat apply operasi baru

## 💡 Tips Penggunaan

### Untuk Foto Gelap:
1. Gunakan **Histogram Equalization** atau **CLAHE**
2. Atau adjust **Brightness** slider ke kanan (+)
3. Tingkatkan **Contrast** sedikit untuk hasil lebih tajam

### Untuk Foto Blur:
1. Gunakan **Sharpening** filter
2. Jangan over-sharpen (bisa menimbulkan noise)

### Untuk Foto Noisy:
1. Gunakan **Smoothing** atau **Gaussian** filter
2. Adjust **Contrast** untuk mengembalikan detail

### Untuk Deteksi Tepi:
1. Gunakan **Sobel Edge** untuk tepi directional
2. Gunakan **Laplacian** untuk tepi semua arah

### Untuk Fine-tuning:
1. Apply operasi dasar (Histogram/Convolution)
2. Gunakan slider untuk penyesuaian detail
3. Kombinasikan Brightness, Contrast, dan Gamma sesuai kebutuhan

## 📝 Format Gambar yang Didukung
- JPG/JPEG
- PNG
- BMP
- TIFF

## ⚡ Performa & Optimasi

- **Lightweight**: Tidak menggunakan matplotlib, hanya Canvas native Tkinter
- **Fast Rendering**: Update real-time yang smooth untuk slider
- **Memory Efficient**: Semua proses in-memory tanpa database
- **No Crash**: Validasi input untuk mencegah error
- **Responsive**: GUI tidak freeze saat processing

## 🎓 Penjelasan Teknis

### Histogram Specification
Teknik untuk mengubah distribusi histogram gambar agar sesuai dengan target tertentu. Program ini menggunakan uniform distribution sebagai target.

### CLAHE (Contrast Limited Adaptive Histogram Equalization)
Berbeda dengan histogram equalization biasa, CLAHE membagi gambar menjadi tile-tile kecil dan melakukan equalization pada setiap tile, menghasilkan enhancement yang lebih natural.

### Convolution
Operasi matematika yang mengaplikasikan kernel/mask pada gambar untuk berbagai efek seperti blur, sharpen, atau edge detection.

### Gamma Correction
Mengubah kurva luminance gambar menggunakan fungsi power law untuk menyesuaikan brightness non-linear.

## 📊 Perbedaan Color Space

- **HSV**: Hue, Saturation, Value - Memisahkan warna dari intensitas
- **LAB**: Lightness, A (green-red), B (blue-yellow) - Perceptually uniform
- **RGB**: Red, Green, Blue - Color space standar untuk display

## 🐛 Troubleshooting

### Program tidak bisa dibuka:
```bash
pip install --upgrade customtkinter
```

### Error saat load gambar:
- Pastikan format gambar didukung (JPG, PNG, BMP, TIFF)
- Cek ukuran file tidak terlalu besar (>50MB)

### Slider tidak smooth:
- Gunakan gambar dengan resolusi lebih kecil
- Close aplikasi lain untuk free up memory

### Hasil terlalu gelap/terang:
- Reset dulu dengan tombol 🔄 Reset
- Apply operasi lagi dengan parameter berbeda

## 📄 Lisensi

Program ini dibuat untuk keperluan edukasi dan pembelajaran pengolahan citra digital.

## 👨‍💻 Pengembangan

Dibuat dengan:
- Python 3.7+
- OpenCV untuk image processing
- CustomTkinter untuk modern GUI
- NumPy untuk operasi array
