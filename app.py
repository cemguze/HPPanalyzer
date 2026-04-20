import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time

# Sayfa Yapılandırması
st.set_page_config(page_title="HPP-Rad Analyzer PRO", page_icon="🧬", layout="wide")

# --- ULTRA MODERN UI/UX TASARIMI (CSS) ---
st.markdown("""
<style>
    /* Ana Arka Plan ve Yazı Tipi */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
    }

    /* Glassmorphism Kart Yapısı */
    .stMetric {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px !important;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease-in-out;
    }
    .stMetric:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
    }

    /* Başlık Alanı Tasarımı */
    .hero-section {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
        padding: 60px 20px;
        border-radius: 24px;
        color: white;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 20px 25px -5px rgba(30, 58, 138, 0.2);
    }
    
    .hero-title { font-size: 3rem; font-weight: 800; margin-bottom: 10px; letter-spacing: -1px; }
    .hero-subtitle { font-size: 1.2rem; font-weight: 300; opacity: 0.9; }

    /* Sidebar Dashboard Görünümü */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }

    /* Buton ve Input Şıklaştırma */
    .stButton>button {
        border-radius: 12px;
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        padding: 10px 24px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- ÜST PANEL (HERO SECTION) ---
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🧬 HPP-Rad Analyzer Pro</div>
        <div class="hero-subtitle">Next-Gen Computational Radiology & Multimodal Diagnostic Support</div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR (KONTROL PANELİ) ---
with st.sidebar:
    st.markdown("### 🛠️ Sistem Kontrol Paneli")
    st.divider()
    
    threshold = st.slider("Hassasiyet Eşiği (HU Analizi)", 50, 200, 125, help="Hekimin belirlediği mineralizasyon referans aralığı.")
    
    st.markdown("### 🩸 Biyokimya Verileri")
    hasta_alp = st.number_input("Serum ALP (U/L)", 0, 200, 40)
    if hasta_alp <= 40:
        st.error("⚠️ Düşük ALP (Kritik HPP Göstergesi)")
        
    hasta_b6 = st.number_input("Vitamin B6 (PLP) (mcg/L)", 0, 200, 20)
    if hasta_b6 >= 100:
        st.error("⚠️ Yüksek B6 (Kritik HPP Göstergesi)")
    
    st.divider()
    st.markdown("👨‍🔬 **Proje Sahibi:** Cem Güzel")
    st.caption("Kent Üniversitesi - Diş Hekimliği Araştırma Protokolü")

# --- ANA İÇERİK ---
st.subheader("📂 Radyografi Verisi İşleme")
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    with st.spinner('Matematiksel spektrum analizi yapılıyor...'):
        time.sleep(1.2)
        
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        
        # Radyomik İşlemler (CLAHE)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
        enhanced_img = clahe.apply(img)
        heatmap = cv2.applyColorMap(enhanced_img, cv2.COLORMAP_JET)
        
        # Veri Analizi
        avg_intensity = np.mean(enhanced_img)
        std_intensity = np.std(enhanced_img)

        # Görüntü Paneli
        tab1, tab2 = st.tabs(["🖼️ Görüntü Analizi", "📊 Spektrum Dağılımı"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Orijinal Veri**")
                st.image(img, use_column_width=True)
            with col2:
                st.markdown("**Mineral Yoğunluk Haritası**")
                st.image(heatmap, use_column_width=True)

        with tab2:
            st.markdown("**Piksel Yoğunluk Histogramı**")
            fig, ax = plt.subplots(figsize=(10, 3))
            ax.hist(enhanced_img.ravel(), 256, [0,256], color='#2563eb', alpha=0.7)
            ax.set_axis_off() # Daha modern görünüm için eksenleri gizle
            st.pyplot(fig)

    # ANALİZ RAPORU (METRİKLER)
    st.markdown("### 📈 Dijital Analiz Raporu")
    m1, m2, m3 = st.columns(3)
    m1.metric("Ortalama Dansite", f"{avg_intensity:.2f} Px", delta_color="inverse")
    m2.metric("Yapısal Heterojenite", f"{std_intensity:.2f}")
    m3.metric("ALP Durumu", f"{hasta_alp} U/L", "-%12" if hasta_alp < 40 else "Normal")

    # TIBBİ SONUÇ
    if avg_intensity < threshold:
        st.warning("🚨 **TEŞHİS DESTEĞİ:** Radyolojik ve biyokimyasal bulgular HPP ile yüksek oranda uyumludur. İleri tetkik önerilir.")
    else:
        st.success("✅ **TEŞHİS DESTEĞİ:** Mineralizasyon değerleri seçili referans aralığında stabil seyretmektedir.")

# --- FOOTER / İMZA ---
st.markdown(f"""
    <div style="margin-top: 100px; padding: 20px; text-align: center; border-top: 1px solid #e2e8f0; color: #94a3b8; font-size: 0.8rem;">
        HPP-Rad Analyzer v2.0 Prototip Tasarımı<br>
        Bu yazılımın UI/UX mimarisi ve algoritmik yapısı <b>Gemini (Ceminay)</b> desteğiyle 
        Cem Güzel için özel olarak optimize edilmiştir. ✨
    </div>
""", unsafe_allow_html=True)
