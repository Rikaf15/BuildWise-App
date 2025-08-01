# 🏗️ BuildWise - Cek Kelayakan Bangunan

**BuildWise** adalah aplikasi berbasis Streamlit yang dirancang untuk membantu pengguna mengevaluasi kelayakan struktur bangunan secara sederhana dan interaktif.

---

## 🚀 Fitur Utama

- **Input Data Bangunan**  
  Masukkan panjang, lebar, jumlah lantai, dan jenis struktur.

- **Hasil Analisis**  
  Menampilkan luas, volume, estimasi beban, dan estimasi biaya bangunan.

- **Visualisasi**  
  Grafik distribusi beban dan skema bangunan untuk memudahkan pemahaman.

- **Panduan Penggunaan**  
  Penjelasan langkah-langkah penggunaan aplikasi bagi pengguna umum maupun mahasiswa teknik sipil.

- **Saran AI**  
  Menggunakan model AI (via OpenRouter) untuk memberikan rekomendasi teknis berdasarkan deskripsi bangunan.

---


## -----------------------
# Buat dan aktifkan virtual environment (opsional tapi disarankan):
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate    # macOS/Linux


## -----------------------
# Install dependensi:
- **pip install -r requirements.txt**


## -----------------------
# Buat file secrets.toml di .streamlit/:
# [openrouter]
- **api_key = "ISI_API_KEY"**


## -----------------------
# Jalankan Aplikasi
- **streamlit run app.py**


## -----------------------
# buildwise/
│
├── app.py                  # File utama aplikasi
├── calculations.py         # Logika perhitungan beban dan biaya
├── requirements.txt        # Daftar pustaka yang dibutuhkan
├── README.md               # Dokumen ini
├── .streamlit/
│   └── secrets.toml        # API Key untuk OpenRouter
└── data/
    └── (opsional) file CSV / input lainnya



