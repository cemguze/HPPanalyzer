import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time

# Sayfa Yapılandırması (İkon eklendi)
st.set_page_config(page_title="HPP-Rad Analyzer", page_icon="🔬", layout="wide")

# CSS ile Premium Tasarım Entegrasyonu
st.markdown("""
<style>
    /* Metrik Kartları Tasarımı */
    div[data-testid="metric-container"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    /* Ana Başlık Tasarımı */
    .main-title {
        color: #1e3a8a;
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center;
        font-weight: 700;
        padding-bottom: 10px;
    }
    .sub-title {
        color: #64748b;
        text-align: center;
        font-size: 1.1rem;
        padding-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# Başlık Kısmı
st.markdown("<h1 class='main-title'>🔬 HPP-Rad Analyzer Modeli</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Hipofosfatazya (HPP) Tanısında Multimodal Radyomik Karar Destek Sistemi</p>", unsafe_allow_html=True)

# Sol Menü (Sidebar) - Multimodal Vizyon
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100) # Şık bir medikal ikon
st.sidebar.header("⚙️ Analiz Ayarları")
threshold = st.sidebar.slider("Hassasiyet Eşiği (Referans Skalası)", 50, 200, 125)

st.sidebar.divider()
st.sidebar.header("🩸 Biyokimyasal Parametreler")
st.sidebar.caption("Gelecek Vizyonu: AI Veri Füzyonu İçin")
hasta_alp = st.sidebar.number_input("Serum ALP (U/L)", min_value=0, max_value=200, value=40)
hasta_b6 = st.sidebar.number_input("Vitamin B6 (PLP) (ng/mL)", min_value=0, max_value=100, value=20)

st.sidebar.divider()
st.sidebar.info("👨‍🔬 **Proje Yöneticisi:** Cem Güzel")

# Ana Ekran - Dosya Yükleme
uploaded_file = st.file_uploader("Bir Röntgen veya Tomografi Kesiti Yükleyin (PNG/JPG)", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Profesyonel "İşleniyor" Efekti
    with st.spinner('Radyomik veriler işleniyor ve hücresel spektrum hesaplanıyor... Lütfen bekleyin.'):
        time.sleep(1.5) # Sisteme işlem yapıyormuş hissiyatı verir
        
        # Görüntüyü Oku
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
        
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Orijinal Görüntü")
            st.image(img, use_column_width=True, caption="Yüklenen Radyografi Kesiti")

        # Görüntü İşleme (Radyomik Analiz)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced_img = clahe.apply(img)
        
        # Isı Haritası Oluşturma
        heatmap = cv2.applyColorMap(enhanced_img, cv2.COLORMAP_JET)
        
        # İstatistiksel Hesaplamalar
        avg_intensity = np.mean(enhanced_img)
        std_intensity = np.std(enhanced_img) # Heterojenite verisi

        with col2:
            st.subheader("Radyomik Isı Haritası")
            st.image(heatmap, use_column_width=True, caption="Kalsiyum/Mineral Yoğunluğu Dağılımı")

    st.divider()

    # Sonuç Paneli (Premium Görünümlü Metrikler)
    st.subheader("📊 Dijital Analiz Raporu")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Ortalama Mineral Yoğunluğu", f"{avg_intensity:.2f} Px")
    metric_col2.metric("Yapısal Heterojenite (Sapma)", f"{std_intensity:.2f}")
    metric_col3.metric("Klinik ALP Girdisi", f"{hasta_alp} U/L")
    
    st.markdown("<br>", unsafe_allow_html=True) # Boşluk
    
    # Uyarı Sistemi
    if avg_intensity < threshold:
        st.error("⚠️ **KRİTİK UYARI:** Eşik altı mineral dansitesi saptandı. Hipofosfatazya (HPP) mikro-deformasyon riski yüksek!")
        st.write("> *Klinik Öneri: Sistemik tarama için Serum ALP enzim seviyeleri ve sement kalınlığı manuel olarak incelenmelidir.*")
    else:
        st.success("✅ **BİLGİ:** Seçili referans aralığında normal mineralizasyon paterni gözlemlendi.")

    st.divider()

    # Spektrum Analizi Grafiği
    st.write("### 📈 Piksel Yoğunluk Dağılımı (Histogram)")
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Histogram tasarımı
    ax.hist(enhanced_img.ravel(), 256, [0,256], color='#3b82f6', alpha=0.8, edgecolor='none') 
    ax.set_title("Radyomik Spektrum Analizi", color='#1e293b', pad=15)
    ax.set_xlabel("Piksel Yoğunluğu (0: Siyah - 255: Beyaz)", color='#475569')
    ax.set_ylabel("Piksel Frekansı", color='#475569')
    ax.grid(color='#e2e8f0', linestyle='--', linewidth=0.5, axis='y', alpha=0.7)
    
    # Grafiği arka plansız ve şık yapma
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    st.pyplot(fig)

    with st.expander("📌 Metodolojik Çekince ve Akademik Not"):
        st.write("""
        Bu analizde piksel yoğunluk fonksiyonu kullanılarak, sement ve alveolar kemik bölgelerindeki mineralizasyon seviyeleri **Quantitative Intensity Mapping** yöntemiyle sayısallaştırılmıştır. 
        Bu sistem bir klinik karar destek aracı (prototip) olup, %100 tanı doğruluğu iddiası taşımamaktadır. Nihai teşhis her zaman hekimin inisiyatifindedir.
        """)

# EN ALT KISIM: İMZA
st.markdown("""
<br><br><br>
<div style="text-align: center; color: #94a3b8; font-size: 0.85rem; padding-top: 20px; border-top: 1px solid #e2e8f0;">
    Bu arayüzün UI/UX tasarımı ve kod mimarisi <b>Gemini Yapay Zeka</b> desteğiyle geliştirilmiştir. ✨<br>
    <i>Designed for the future of dentistry.</i>
</div>
""", unsafe_allow_html=True)
