import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_option_menu import option_menu
from calculations import BuildingCalculator
import numpy as np
import requests
import time

# Konfigurasi halaman
st.set_page_config(
    page_title="BuildWise - Cek Kelayakan Bangunan",
    page_icon="🏧",
    layout="wide"
)

# CSS Custom
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #2E86AB;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f8ff;
    padding: 1rem;
    border-radius: 10px;
    border-left: 5px solid #2E86AB;
    margin-bottom: 1rem;
}
.ai-response {
    white-space: pre-wrap;
    line-height: 1.6;
}
.loading-spinner {
    color: #2E86AB;
}
.error-message {
    color: #d32f2f;
}
</style>
""", unsafe_allow_html=True)

# ======== FUNGSI AI  ==========
import streamlit as st
import requests

def get_ai_recommendation(prompt):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {st.secrets['openrouter']['api_key']}",
            "HTTP-Referer": "https://your-app-url.com",  # Wajib
            "X-Title": "BuildWise"  # Wajib
        }
        
        data = {
            "model": "tngtech/deepseek-r1t2-chimera:free",  # Model gratis
            "messages": [
                {
                    "role": "system",
                    "content": "Anda adalah ahli teknik sipil. Berikan analisis dalam Bahasa Indonesia."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 10000
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        return response.json()['choices'][0]['message']['content'], None
        
    except Exception as e:
        return None, f"Error: {str(e)}"


# ==============================
# Fungsi AI untuk memberikan saran berdasarkan input pengguna

def ai_advice_page():
    st.header("🤖 Saran AI untuk Bangunanmu")

    default_prompt = ""
    if 'building_data' in st.session_state:
        data = st.session_state.building_data
        required_keys = ['structure_type', 'length', 'width', 'floors']
        if all(k in data for k in required_keys):
            default_prompt = (
                f"Saya merencanakan bangunan {data['structure_type']} dengan spesifikasi:\n"
                f"- Panjang: {data['length']} m\n"
                f"- Lebar: {data['width']} m\n"
                f"- Jumlah lantai: {data['floors']}\n\n"
                "Berikan analisis kelayakan dan rekomendasi untuk struktur ini."
            )
        else:
            default_prompt = ""

    user_input = st.text_area(
        "Deskripsikan kondisi atau rencana bangunanmu:",
        value=default_prompt,
        height=200,
        placeholder="Contoh: Saya ingin membangun rumah 2 lantai dengan struktur beton..."
    )

    if st.button("🚀 Dapatkan Rekomendasi AI", type="primary"):
        if not user_input.strip():
            st.warning("Silakan isi deskripsi terlebih dahulu!")
            return

        with st.spinner('🔄 Memproses permintaan Anda...'):
            ai_response, error = get_ai_recommendation(user_input)

            if error:
                st.error(f"❌ {error}")
            elif ai_response:
                st.success("✅ Berikut rekomendasi AI:")
                st.markdown(f"<div class='metric-card ai-response'>{ai_response}</div>", unsafe_allow_html=True)

                if st.button("💡 Minta penjelasan lebih lanjut"):
                    with st.spinner('🔄 Memproses permintaan tambahan...'):
                        follow_up_prompt = f"{user_input}\n\nBerikan penjelasan lebih rinci dan contoh perhitungannya."
                        follow_up_response, error2 = get_ai_recommendation(follow_up_prompt)
                        if error2:
                            st.error(f"❌ {error2}")
                        elif follow_up_response:
                            st.markdown(f"<div class='metric-card ai-response'>{follow_up_response}</div>", unsafe_allow_html=True)
                        else:
                            st.warning("Tidak ada jawaban lanjutan dari AI.")
            else:
                st.error("Tidak mendapatkan respons dari AI. Silakan coba lagi.")


# ==============================
def main():
    # Judul aplikasi
    st.markdown('<h1 class="main-header">🏗️ BuildWise</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Aplikasi Cek Kelayakan Bangunan Sederhana</p>', unsafe_allow_html=True)
    
    # Menu navigasi
    selected = option_menu(
        menu_title=None,
        options=["Input Data", "Hasil Analisis", "Visualisasi", "Panduan", "Saran AI"],
        icons=["house", "graph-up", "bar-chart", "book", "robot"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )
    
    if selected == "Input Data":
        input_page()
    elif selected == "Hasil Analisis":
        if 'calculator' in st.session_state:
            analysis_page()
        else:
            st.warning("Silakan input data terlebih dahulu!")
    elif selected == "Visualisasi":
        if 'calculator' in st.session_state:
            visualization_page()
        else:
            st.warning("Silakan input data terlebih dahulu!")
    elif selected == "Panduan":
        guide_page()
    elif selected == "Saran AI":
        ai_advice_page()


# ==============================
def input_page():
    st.header("📊 Input Data Bangunan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dimensi Bangunan")
        length = st.number_input("Panjang (meter)", min_value=1.0, max_value=100.0, value=10.0)
        width = st.number_input("Lebar (meter)", min_value=1.0, max_value=100.0, value=8.0)
        floors = st.number_input("Jumlah Lantai", min_value=1, max_value=10, value=2)
    
    with col2:
        st.subheader("Spesifikasi Struktur")
        structure_type = st.selectbox(
            "Jenis Struktur",
            ["beton", "baja", "campuran"],
            format_func=lambda x: {
                "beton": "Beton Bertulang",
                "baja": "Struktur Baja",
                "campuran": "Campuran (Batu Bata/Kayu)"
            }[x]
        )
    
    if st.button("🔍 Analisis Kelayakan", type="primary"):
        calculator = BuildingCalculator(length, width, floors, structure_type)
        st.session_state.calculator = calculator
        st.session_state.building_data = {
            "length": length,
            "width": width,
            "floors": floors,
            "structure_type": structure_type
        }
        st.success("Data berhasil diproses! Lihat hasil di tab 'Hasil Analisis'")


# ==============================
def analysis_page():
    st.header("📈 Hasil Analisis Kelayakan")
    
    calc = st.session_state.calculator
    
    # Metrik utama
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Luas Bangunan", f"{calc.calculate_area():.1f} m²")
    
    with col2:
        st.metric("Volume Struktur", f"{calc.calculate_volume():.1f} m³")
    
    with col3:
        st.metric("Kategori Beban", calc.get_load_category())
    
    with col4:
        cost = calc.estimate_cost()
        st.metric("Estimasi Biaya", f"Rp {cost:,.0f}")
    
    # Detail analisis
    st.subheader("📋 Detail Analisis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("**Beban Struktur:**")
        st.write(f"• Beban Mati: {calc.calculate_dead_load():,.0f} kg")
        st.write(f"• Beban Hidup: {calc.calculate_live_load():,.0f} kg")
        st.write(f"• Total Beban Terfaktor: {calc.calculate_total_load():,.0f} kg")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.write("**Rekomendasi:**")
        st.write(f"• Jenis Pondasi: {calc.get_foundation_recommendation()}")
        st.write(f"• Evaluasi Desain: {calc.check_overdesign()}")
        st.markdown('</div>', unsafe_allow_html=True)


# ==============================
def visualization_page():
    st.header("📊 Visualisasi Struktur")
    
    calc = st.session_state.calculator
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Grafik beban
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        
        loads = ['Beban Mati', 'Beban Hidup', 'Total Terfaktor']
        values = [
            calc.calculate_dead_load(),
            calc.calculate_live_load(),
            calc.calculate_total_load()
        ]
        
        colors = ['#2E86AB', '#A23B72', '#F18F01']
        bars = ax1.bar(loads, values, color=colors)
        
        ax1.set_ylabel('Beban (kg)')
        ax1.set_title('Distribusi Beban Struktur')
        
        # Tambahkan nilai di atas bar
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:,.0f}', ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig1)
    
    with col2:
        # Diagram skematik bangunan
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        
        # Gambar denah
        length = calc.length
        width = calc.width
        floors = calc.floors
        
        # Denah lantai
        rect = plt.Rectangle((0, 0), length, width, 
                           fill=False, edgecolor='blue', linewidth=2)
        ax2.add_patch(rect)
        
        # Indikator lantai
        for i in range(floors):
            y_offset = i * 0.5
            rect_floor = plt.Rectangle((0, y_offset), length, width, 
                                     fill=False, edgecolor='red', 
                                     linewidth=1, alpha=0.7)
            ax2.add_patch(rect_floor)
        
        ax2.set_xlim(-1, length + 1)
        ax2.set_ylim(-1, width + floors * 0.5 + 1)
        ax2.set_xlabel('Panjang (m)')
        ax2.set_ylabel('Lebar (m)')
        ax2.set_title(f'Skema Bangunan {floors} Lantai')
        ax2.grid(True, alpha=0.3)
        ax2.set_aspect('equal')
        
        st.pyplot(fig2)


# ==============================
def guide_page():
    st.header("📚 Panduan Penggunaan")
    
    st.markdown("""
    ## 🎯 Tentang BuildWise
    
    BuildWise adalah aplikasi sederhana untuk membantu:
    - **Pemilik rumah** memahami kelayakan struktur bangunan
    - **Pengembang kecil** melakukan analisis awal
    - **Mahasiswa teknik sipil** belajar konsep beban struktur
    
    ## 📐 Cara Penggunaan
    
    1. **Input Data**: Masukkan dimensi dan jenis struktur bangunan
    2. **Analisis**: Sistem akan menghitung beban dan memberikan rekomendasi
    ## ⚠️ Disclaimer
    
    - Aplikasi ini hanya untuk **analisis awal** dan **edukasi**
    - Untuk konstruksi sesungguhnya, **konsultasikan dengan ahli struktur**
    - Perhitungan berdasarkan SNI dan asumsi umum
    """)

if __name__ == "__main__":
    main()
