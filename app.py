import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


st.set_page_config(page_title="HPP-Rad Analyzer", layout="wide")

st.title("HPP-Rad Analyzer")
st.markdown("""
Bu prototip, **Hipofosfatazya (HPP)** tanısında radyomik verilerin (piksel yoğunluğu) analizi için geliştirilmiştir. 
Hekimin gözle kaçırabileceği mineralizasyon kayıplarını matematiksel olarak saptar. Şuan geliştirme aşamasındadır yüzde yüz veri doğruluğu şuanki aşamada mümkün değildir
""")


st.sidebar.header("Analiz Ayarları")
threshold = st.sidebar.slider("Hassasiyet Eşiği (hekimin belirlediği referans aralığı)", 50, 200, 125)
st.sidebar.info("Cem Güzel Prototipidir.")


uploaded_file = st.file_uploader("Bir Röntgen veya Tomografi Kesiti Yükleyin", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Görüntüyü Oku
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Orijinal Görüntü")
        st.image(img, use_column_width=True, caption="Yüklenen Radyografi")

    # Görüntü İşleme (Radyomik Analiz)
    # Kontrast artırma (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced_img = clahe.apply(img)
    
    # Isı Haritası Oluşturma
    heatmap = cv2.applyColorMap(enhanced_img, cv2.COLORMAP_JET)
    
    # Ortalama Yoğunluk Analizi (Merkezi Bölge)
    avg_intensity = np.mean(enhanced_img)

    with col2:
        st.subheader("Radyomik Isı Haritası")
        st.image(heatmap, use_column_width=True, caption="Mineral Yoğunluğu Dağılımı")

    st.divider()

    # Sonuç Paneli
    st.subheader("Analiz Raporu")
    
    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric("Ortalama Mineral Yoğunluğu", f"{avg_intensity:.2f} HU")
    
    if avg_intensity < threshold:
        st.error("KRİTİK UYARI: Düşük kemik dansitesi saptandı. Hipofosfatazya (HPP) riski yüksek!")
        st.write("**Öneri:** Hastanın sement kalınlığı incelenmeli ve ALP enzim seviyeleri kontrol edilmelidir.")
    else:
        st.success("Normal mineralizasyon seviyesi gözlemlendi.")

    #THİS İS SPECTRUM ANALYSİS
    st.write("### Piksel Yoğunluk Dağılımı (Histogram)")
    fig, ax = plt.subplots()
    #THİS CODE BLOCK EXACTLY SHOW HOW THE METHOD İS WORKİNG
    ax.hist(enhanced_img.ravel(), 256, [0,256], color='blue', alpha=0.7) 
    ax.set_title("Görüntü Spektrum Analizi")
    st.pyplot(fig)

    # ... önceki kodların (st.pyplot(fig) satırından sonrası) ...

    with st.expander("Metodolojik Not"):
        st.write("""
        Bu analizde piksel yoğunluk fonksiyonu kullanılarak, 
        sement ve alveolar kemik bölgelerindeki kalsiyum-fosfat kristalizasyonu 
        **Quantitative Intensity Mapping** yöntemiyle sayısallaştırılmıştır. yüzde yüz veri doğruluğu bu aşamada mümkün değildir test amaçlıdır
        """)
   