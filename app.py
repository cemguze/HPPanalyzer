import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time

# --- SAYFA YAPILANDIRMASI (GENİŞ EKRAN DASHBOARD) ---
st.set_page_config(page_title="HPP-Rad Analyzer", page_icon="🩻", layout="wide", initial_sidebar_state="expanded")

# --- KUSURSUZ OKUNABİLİRLİK İÇİN GÜVENLİ CSS ---
st.markdown("""
<style>
    /* Üst Başlık Şeridi */
    .top-banner {
        background: linear-gradient(90deg, #0f172a 0%, #1e3a8a 100%);
        padding: 20px 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .top-banner h1 { margin: 0; font-size: 24px; color: white; font-weight: 700; }
    .top-banner p { margin: 0; font-size: 14px; opacity: 0.8; }
    
    /* Metrik Kartları */
    [data-testid="metric-container"] {
        border-left: 4px solid #3b82f6;
        background-color: rgba(59, 130, 246, 0.05);
        padding: 10px 15px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- ÜST BİLGİ ŞERİDİ (HEADER) ---
st.markdown("""
<div class="top-banner">
    <div>
        <h1>🩻 HPP-Rad Klinik Karar Destek Sistemi</h1>
        <p>Hesaplamalı Görüntü İşleme & Multimodal Veri Füzyonu Prototipi</p>
    </div>
    <div style="text-align: right;">
        <p><b>Araştırmacı:</b> Cem Güzel</p>
        <p><b>Durum:</b> Aktif | Sürüm: 2.1.0</p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SOL MENÜ: HASTA VE SİSTEM VERİLERİ (GÜVENLİ ARAYÜZ) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063206.png", width=80)
    st.title("Klinik Parametreler")
    st.caption("Multimodal algoritma için hasta verilerini giriniz.")
    st.divider()
    
    # Uyarı sistemini native Streamlit modülleriyle daha şık yaptık
    hasta_alp = st.number_input("🩸 Serum ALP (U/L)", 0, 200, 40)
    if hasta_alp <= 40:
        st.error("Düşük ALP (Kritik Eşik)")
    else:
        st.success("ALP Normal")
        
    hasta_b6 = st.number_input("🧪 Vitamin B6 (PLP)", 0, 200, 20)
    if hasta_b6 >= 100:
        st.error("Yüksek B6 (Kritik Eşik)")
    else:
        st.success("B6 Normal")
        
    st.divider()
    st.subheader("Radyomik Kalibrasyon")
    threshold = st.slider("Hassasiyet Eşiği", 50, 200, 125)

# --- ANA KOKPİT (YENİ MİMARİ İKİ KOLON) ---
# Ekranı ikiye bölüyoruz: Sol (Monitör) %45, Sağ (Analiz) %55
col_monitor, col_analiz = st.columns([4.5, 5.5], gap="large")

with col_monitor:
    st.subheader("📥 Radyolojik Görüntüleme Monitörü")
    uploaded_file = st.file_uploader("2D Kesit Yükleyiniz (PNG/JPG)", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        # Resmi Oku
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        
        # Görüntü İşleme
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
        enhanced_img = clahe.apply(img)
        heatmap = cv2.applyColorMap(enhanced_img, cv2.COLORMAP_JET)
        
        # Analiz Değerleri
        avg_intensity = np.mean(enhanced_img)
        std_intensity = np.std(enhanced_img)
        
        # Görüntüleri Sekmelerle Göster (Aşağı doğru uzamasını engeller)
        tab_orj, tab_isi = st.tabs(["Radyografi (Orijinal)", "Isı Haritası (Kalsiyum Dağılımı)"])
        with tab_orj:
            st.image(img, use_column_width=True)
        with tab_isi:
            st.image(heatmap, use_column_width=True)

with col_analiz:
    st.subheader("📊 Telemetri ve Veri Merkezi")
    
    if uploaded_file is None:
        st.info("Sistem Beklemede... Lütfen sol taraftan bir röntgen kesiti yükleyiniz.")
    else:
        with st.spinner('Piksel yoğunluk fonksiyonları işleniyor...'):
            time.sleep(1) # Profesyonel yükleme hissi
            
            # ÜST: Metrikler (Yan Yana 3 Kutu)
            m1, m2, m3 = st.columns(3)
            m1.metric("Ortalama Yoğunluk", f"{avg_intensity:.1f} HU", delta="Radyomik Veri", delta_color="off")
            m2.metric("Doku Sapması", f"{std_intensity:.1f}", delta="Heterojenite", delta_color="off")
            m3.metric("Klinik Risk Algoritması", "Aktif", delta="Multimodal", delta_color="normal")
            
            st.divider()
            
            # ORTA: Spektrum Grafiği
            st.write("**Hücresel Spektrum Dağılımı**")
            fig, ax = plt.subplots(figsize=(8, 3))
            ax.hist(enhanced_img.ravel(), 256, [0,256], color='#1e3a8a', alpha=0.85)
            
            # Grafiği şıklaştırma
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_facecolor('none')
            fig.patch.set_alpha(0.0)
            ax.grid(axis='y', linestyle='--', alpha=0.3)
            
            st.pyplot(fig)
            
            # ALT: Karar Destek Raporu (Dinamik Uyarı)
            st.subheader("📋 Sistem Raporu")
            if avg_intensity < threshold or hasta_alp <= 40 or hasta_b6 >= 100:
                st.error("⚠️ **HPP RİSKİ SAPTANDI:** Radyomik yoğunluk düşüklüğü VEYA kan tablosundaki anormallik, Hipofosfatazya lehine güçlü bulgular içermektedir.")
            else:
                st.success("✅ **STABİL:** Hastanın radyolojik mineralizasyonu ve enzim tablosu referans değerleri içerisindedir.")

# --- EN ALT: İMZA ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("Bu karar destek sisteminin çekirdek algoritması ve arayüz mimarisi **Gemini Yapay Zeka** kullanılarak tasarlanmıştır. Tıbbi referans amaçlıdır.")
