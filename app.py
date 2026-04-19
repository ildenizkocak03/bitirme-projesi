import streamlit as st
import pandas as pd
from src.analyzer import SentimentAnalyzer
from src.topic_engine import TopicEngine
from src.risk_engine import RiskEngine
from src.reporting import generate_pdf_report
import plotly.express as px
from io import BytesIO

st.set_page_config(
    page_title="Customer Review AI Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top left, rgba(82, 242, 200, 0.18), transparent 35%),
                    radial-gradient(circle at top right, rgba(255, 79, 163, 0.18), transparent 30%),
                    linear-gradient(180deg, #06131a 0%, #071821 100%) !important;
        color: #e6f7ff;
    }

    .stApp {
        overflow-x: hidden;
    }

    [data-testid="stSidebar"] > div:first-child {
        background: rgba(8, 20, 34, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: inset -1px 0 0 rgba(255,255,255,0.06);
    }

    [data-testid="stToolbar"] {
        background: transparent !important;
    }

    .css-18e3th9, .css-1d391kg, .css-1lcbmhc, .css-1v3fvcr, .css-1r6slb3 {
        background: transparent !important;
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    .hero-panel, .feature-panel, .upload-panel, .results-panel, .analytics-panel, .download-panel {
        background: rgba(15, 27, 41, 0.80);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(16px);
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
    }

    .hero-panel {
        position: relative;
        overflow: hidden;
        padding: 3rem 3.5rem;
    }

    .hero-panel::before {
        content: "";
        position: absolute;
        width: 420px;
        height: 420px;
        border-radius: 50%;
        top: -120px;
        right: -140px;
        background: radial-gradient(circle, rgba(82,242,200,0.28), transparent 55%);
        filter: blur(50px);
        pointer-events: none;
    }

    .hero-panel::after {
        content: "";
        position: absolute;
        width: 360px;
        height: 360px;
        border-radius: 50%;
        bottom: -150px;
        left: -120px;
        background: radial-gradient(circle, rgba(255,79,163,0.18), transparent 55%);
        filter: blur(60px);
        pointer-events: none;
    }

    .hero-title {
        font-size: clamp(3rem, 4.4vw, 4.8rem);
        font-weight: 900;
        margin: 0;
        line-height: 1.02;
        color: #f4f9ff;
        letter-spacing: -0.05em;
        z-index: 1;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: rgba(230, 247, 255, 0.84);
        max-width: 860px;
        margin: 1.5rem 0 2rem;
        line-height: 1.75;
        z-index: 1;
    }

    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        z-index: 1;
    }

    .hero-cta {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #52f2c8, #ff4fa3);
        color: #06131a;
        border: none;
        border-radius: 999px;
        padding: 1rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        text-decoration: none;
    }

    .hero-cta:hover {
        transform: translateY(-3px);
        box-shadow: 0 24px 40px rgba(82, 242, 200, 0.26);
    }

    .hero-secondary {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #d8f6ff;
        border-radius: 999px;
        padding: 1rem 2rem;
        font-weight: 600;
        transition: background 0.25s ease;
    }

    .hero-secondary:hover {
        background: rgba(255, 255, 255, 0.12);
    }

    h2, h3, h4, h5, h6, p {
        color: #e6f7ff;
    }

    .section-title {
        font-size: 2rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }

    .section-description {
        color: rgba(230, 247, 255, 0.72);
        margin-bottom: 1.8rem;
        line-height: 1.8;
        max-width: 920px;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 1.5rem;
    }

    .feature-card {
        background: rgba(15, 27, 41, 0.72);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 1.8rem;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.25);
        transition: transform 0.25s ease, border-color 0.25s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        border-color: rgba(82, 242, 200, 0.28);
    }

    .feature-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 3.2rem;
        height: 3.2rem;
        border-radius: 16px;
        background: rgba(82, 242, 200, 0.12);
        color: #52f2c8;
        font-size: 1.6rem;
        margin-bottom: 1rem;
    }

    .feature-title {
        margin: 0 0 0.75rem;
        font-size: 1.15rem;
        font-weight: 800;
    }

    .feature-description {
        color: rgba(230, 247, 255, 0.72);
        line-height: 1.7;
        margin: 0;
    }

    .upload-panel {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .upload-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .upload-description {
        color: rgba(230, 247, 255, 0.72);
        margin-bottom: 1.5rem;
        max-width: 760px;
    }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 1.25rem;
    }

    .kpi-card {
        background: rgba(11, 34, 48, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 1.7rem;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.24);
        transition: transform 0.25s ease;
    }

    .kpi-card:hover {
        transform: translateY(-4px);
    }

    .kpi-value {
        font-size: 2.6rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.4rem;
    }

    .kpi-label {
        color: rgba(230, 247, 255, 0.70);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.85rem;
    }

    .chart-card {
        background: rgba(15, 27, 41, 0.90);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 1.5rem;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.24);
        margin-bottom: 1.5rem;
    }

    .table-card {
        background: rgba(15, 27, 41, 0.90);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 1.5rem;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.24);
        margin-bottom: 1.5rem;
        overflow-x: auto;
    }

    .results-title {
        font-size: 2rem;
        font-weight: 900;
        margin-bottom: 0.35rem;
    }

    .results-subtitle {
        color: rgba(230, 247, 255, 0.72);
        margin-bottom: 1.6rem;
        line-height: 1.75;
    }

    .download-panel {
        padding: 2rem;
        justify-content: center;
        text-align: center;
    }

    .download-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 0.6rem;
    }

    .download-description {
        color: rgba(230, 247, 255, 0.72);
        margin-bottom: 1.4rem;
    }

    .download-buttons {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }

    .stButton>button, .stDownloadButton>button {
        border-radius: 999px !important;
        padding: 0.85rem 1.9rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        border: none !important;
        background: linear-gradient(135deg, #52f2c8, #ff4fa3) !important;
        box-shadow: 0 18px 40px rgba(82, 242, 200, 0.18) !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    }

    .stButton>button:hover, .stDownloadButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 22px 44px rgba(82, 242, 200, 0.28) !important;
    }

    .stFileUploader>div>div>div>button {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #e6f7ff !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 18px !important;
        padding: 1rem 1.2rem !important;
    }

    .stFileUploader>div>div>div>button:hover {
        background: rgba(82, 242, 200, 0.14) !important;
    }

    .stTextArea>div>div>textarea,
    .stTextInput>div>div>input,
    .stSelectbox>div>div {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #06131a !important;
        border: 1px solid rgba(82, 242, 200, 0.4) !important;
        border-radius: 16px !important;
    }

    .stTextArea>div>div>textarea::placeholder,
    .stTextInput>div>div>input::placeholder {
        color: rgba(6, 19, 26, 0.4) !important;
    }

    .stSelectbox>div>div>div>div {
        background: rgba(255, 255, 255, 0.05) !important;
    }

    .stMultiSelect>div>div>div>div {
        background: rgba(255, 255, 255, 0.05) !important;
    }

    button[role="tab"] {
        background: rgba(255, 255, 255, 0.04) !important;
        color: rgba(230, 247, 255, 0.80) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 999px !important;
        padding: 0.75rem 1.2rem !important;
        margin-right: 0.35rem;
        transition: all 0.25s ease;
    }

    button[role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(82,242,200,0.24), rgba(255,79,163,0.22));
        color: #ffffff !important;
        border-color: rgba(82, 242, 200, 0.35) !important;
        box-shadow: 0 15px 35px rgba(82, 242, 200, 0.12) !important;
    }

    .stProgress > div > div {
        background: rgba(82, 242, 200, 0.18) !important;
    }

    .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: rgba(230, 247, 255, 0.90) !important;
    }

    table {
        background: rgba(15, 27, 41, 0.95) !important;
        color: #e6f7ff !important;
        border-radius: 18px;
    }

    thead th {
        color: #ffffff !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.10) !important;
        background: rgba(255, 255, 255, 0.04) !important;
    }

    tbody tr:nth-child(odd) {
        background: rgba(255, 255, 255, 0.02) !important;
    }

    tbody tr:hover {
        background: rgba(82, 242, 200, 0.08) !important;
    }

    td, th {
        border: none !important;
        padding: 0.85rem 0.95rem !important;
    }

    .stAlert {
        border-radius: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }

    @media (max-width: 1024px) {
        .feature-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
        .kpi-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 760px) {
        .feature-grid, .kpi-grid {
            grid-template-columns: 1fr;
        }
        .hero-panel {
            padding: 2rem 1.5rem;
        }
        .hero-title {
            font-size: 2.8rem;
        }
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

sentiment_analyzer = SentimentAnalyzer()
topic_engine = TopicEngine()
risk_engine = RiskEngine()


def style_plotly(fig):
    fig.update_layout(
        plot_bgcolor='rgba(10, 19, 26, 0.8)',
        paper_bgcolor='rgba(10, 19, 26, 0)',
        font_color='#e6f7ff',
        legend=dict(
            bgcolor='rgba(10, 19, 26, 0.75)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1
        ),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    if fig.data:
        fig.update_traces(marker_line_color='rgba(255,255,255,0.08)', marker_line_width=1)
    return fig


def create_sentiment_badge(sentiment):
    if sentiment == 'positive':
        return '<span style="display:inline-block;padding:0.35rem 0.85rem;border-radius:999px;background:#052f17;color:#a7ffd5;font-weight:700;font-size:0.85rem;">Olumlu</span>'
    elif sentiment == 'negative':
        return '<span style="display:inline-block;padding:0.35rem 0.85rem;border-radius:999px;background:#45121a;color:#ffd8e8;font-weight:700;font-size:0.85rem;">Olumsuz</span>'
    else:
        return '<span style="display:inline-block;padding:0.35rem 0.85rem;border-radius:999px;background:#3a3f4d;color:#fdf6e3;font-weight:700;font-size:0.85rem;">Nötr</span>'


def create_risk_badge(risk_level):
    if risk_level == 'low':
        return '<span style="display:inline-block;padding:0.35rem 0.85rem;border-radius:999px;background:#183f1f;color:#a7ffd5;font-weight:700;font-size:0.85rem;">Düşük Risk</span>'
    elif risk_level == 'medium':
        return '<span style="display:inline-block;padding:0.35rem 0.85rem;border-radius:999px;background:#5d4b1a;color:#fff3a0;font-weight:700;font-size:0.85rem;">Orta Risk</span>'
    elif risk_level == 'high':
        return '<span style="display:inline-block;padding:0.35rem 0.85rem;border-radius:999px;background:#5a1620;color:#ffb3c7;font-weight:700;font-size:0.85rem;">Yüksek Risk</span>'
    else:
        return '<span style="display:inline-block;padding:0.35rem 0.85rem;border-radius:999px;background:#3f1226;color:#ffb3c7;font-weight:700;font-size:0.85rem;">Kritik Risk</span>'


def render_data_table(df):
    table_html = df.to_html(escape=False, index=False)
    styled_table = f"""
    <div class='table-card'>
        {table_html}
    </div>
    """
    return styled_table


def main():
    with st.sidebar:
        st.markdown(
            """
            <div style='padding: 1rem 1rem 0.5rem; margin-bottom: 1rem; background: rgba(255,255,255,0.03); border-radius: 20px; border: 1px solid rgba(255,255,255,0.08);'>
                <h2 style='margin:0; color:#f8fcff;'>AI Müşteri Yorum Analizi</h2>
                <p style='margin:0.75rem 0 0; color:rgba(230,247,255,0.72); font-size:0.95rem;'>Müşteri yorumlarınızı premium dark dashboard ile analiz edin.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("### Hakkında")
        st.markdown(
            """
            Bu uygulama, müşteri yorumlarınızı yapay zeka ile analiz eder:
            - **Duygu Analizi**: Pozitif, negatif veya nötr duygu tespiti
            - **Konu Tespiti**: Şikayet konularını belirler
            - **Risk Skoru**: Yüksek riskli geri bildirimleri öne çıkarır
            - **Görsel Raporlar**: Koyu temalı dashboard görünümü
            """
        )
        st.markdown("### Ayarlar")
        if st.checkbox("Gelişmiş Mod", key='advanced_mode'):
            st.markdown("**Gelişmiş ayarlar aktif edildi**")
            confidence_threshold = st.slider("Güven Eşiği", 0.0, 1.0, 0.7, 0.1, key='confidence_threshold')
            max_reviews = st.slider("Maksimum Yorum Sayısı", 100, 10000, 1000, 100, key='max_reviews')
        else:
            confidence_threshold = 0.7
            max_reviews = 1000
        st.markdown("---")
        st.markdown("**Version:** 2.0.0")

    st.markdown(
        """
        <div class='hero-panel'>
            <h1 class='hero-title'>Müşteri Yorum AI Analizi</h1>
            <p class='hero-subtitle'>Müşteri geri bildirimlerini gelişmiş AI destekli duygu analizi, konu tespiti ve risk değerlendirmesi ile uygulamaya dönüştürün.</p>
            <div class='hero-actions'>
                <a class='hero-cta' href='#upload'>CSV Yükle</a>
                <span class='hero-secondary'>Dark AI Dashboard</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["📋 Hakkında", "📁 CSV Yükleme", "✏️ Metin Analizi"])

    with tab1:
        st.markdown(
            """
            <div class='feature-panel'>
                <h2 class='section-title'>Premium Analiz Deneyimi</h2>
                <p class='section-description'>Koyu tema, neon vurgu ve camefektli kartlarla modern bir AI dashboard görünümü elde edin.</p>
                <div class='feature-grid'>
                    <div class='feature-card'>
                        <div class='feature-icon'>😊</div>
                        <h3 class='feature-title'>Duygu Analizi</h3>
                        <p class='feature-description'>Müşteri yorumlarını olumlu, nötr veya olumsuz olarak hızla sınıflandırın.</p>
                    </div>
                    <div class='feature-card'>
                        <div class='feature-icon'>🏷️</div>
                        <h3 class='feature-title'>Konu Tespiti</h3>
                        <p class='feature-description'>Yorumlardaki ana konuları ve şikayet kalıplarını keşfedin.</p>
                    </div>
                    <div class='feature-card'>
                        <div class='feature-icon'>⚠️</div>
                        <h3 class='feature-title'>Risk Değerlendirmesi</h3>
                        <p class='feature-description'>Hızlı risk puanlaması ile kritik yorumları önceliklendirin.</p>
                    </div>
                    <div class='feature-card'>
                        <div class='feature-icon'>📈</div>
                        <h3 class='feature-title'>Premium Raporlama</h3>
                        <p class='feature-description'>Analiz sonuçlarını şık dark dashboard görünümünde inceleyin.</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            """
            <div class='upload-panel' id='upload'>
                <h3 class='upload-title'>Upload Your Customer Reviews</h3>
                <p class='upload-description'>Start your AI-powered analysis by uploading a CSV file containing customer feedback and reviews.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader("", type=['csv'], label_visibility="collapsed", key='file_uploader')

        if uploaded_file is not None:
            try:
                try:
                    df = pd.read_csv(uploaded_file, encoding='utf-8', dtype=str)
                except Exception:
                    df = pd.read_csv(uploaded_file, encoding='latin-1', dtype=str)

                if df.empty:
                    st.error("❌ Dosya boş. Lütfen veri içeren bir dosya yükleyin.")
                else:
                    st.success(f"✅ Dosya başarıyla yüklendi! ({len(df)} satır, {len(df.columns)} sütun)")
                    st.info(f"📋 Sütunlar: {', '.join(df.columns.tolist())}")
                    st.session_state['uploaded_df'] = df
                    
                    # Analyze the CSV automatically
                    if 'review_text' in df.columns:
                        with st.spinner("🔄 CSV analiz ediliyor... Bu birkaç dakika sürebilir."):
                            try:
                                results = []
                                for idx, row in df.iterrows():
                                    review_text = str(row['review_text']).strip()
                                    if review_text:
                                        sentiment = sentiment_analyzer.analyze(review_text)
                                        topic = topic_engine.classify_topic(review_text)
                                        risk = risk_engine.assess_risk(review_text, sentiment)
                                        
                                        results.append({
                                            'review_id': row.get('review_id', idx+1),
                                            'date': row.get('date', ''),
                                            'platform': row.get('platform', ''),
                                            'rating': row.get('rating', ''),
                                            'review_text': review_text,
                                            'sentiment': sentiment['label'],
                                            'sentiment_score': sentiment['score'],
                                            'topic': topic['topic'],
                                            'topic_confidence': topic['confidence'],
                                            'risk_level': risk['level'],
                                            'risk_score': risk['score']
                                        })
                                
                                results_df = pd.DataFrame(results)
                                st.session_state['results_df'] = results_df
                                st.success(f"✅ CSV analizi tamamlandı! {len(results_df)} yorum analiz edildi.")
                            except Exception as analysis_error:
                                st.error(f"❌ Analiz sırasında hata: {analysis_error}")
                    else:
                        st.error("❌ CSV dosyasında 'review_text' sütunu bulunamadı. Lütfen yorumların bulunduğu sütunu 'review_text' olarak adlandırın.")
            except Exception as exc:
                st.error(f"❌ Dosya okunurken hata oluştu: {exc}")

    with tab3:
        st.markdown('<h2 class="section-title">✏️ Metin Analizi</h2>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class='upload-panel'>
                <h3 class='upload-title'>Doğrudan Metin Analizi</h3>
                <p class='upload-description'>CSV dosyası yüklemek yerine, doğrudan metin girerek analiz yapabilirsiniz. Her satırı ayrı bir yorum olarak değerlendirecektir.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        text_input = st.text_area(
            "Analiz edilecek metinleri girin (her satır bir yorum):",
            value="""Ürün çok kaliteli, çok memnun kaldım.
Kargo çok yavaş geldi, beklemekten bıktım.
Fiyat performans oranı mükemmel.
Müşteri hizmetleri hiç yardımcı olmadı.""",
            height=200,
            help="Her satırı ayrı bir müşteri yorumu olarak analiz edecektir.",
            key='text_analysis_input',
        )

        if st.button("🚀 Metni Analiz Et", key='text_analyze'):
            if text_input.strip():
                with st.spinner("🔄 Metin analiz ediliyor... Bu birkaç dakika sürebilir."):
                    try:
                        reviews = [line.strip() for line in text_input.split('\n') if line.strip()]
                        if not reviews:
                            st.error("❌ Geçerli yorum bulunamadı. Lütfen metin girin.")
                        else:
                            results = []
                            for idx, review_text in enumerate(reviews, start=1):
                                sentiment = sentiment_analyzer.analyze(review_text)
                                topic = topic_engine.classify_topic(review_text)
                                risk = risk_engine.assess_risk(review_text, sentiment)
                                results.append({
                                    'review_id': idx,
                                    'review_text': review_text,
                                    'sentiment': sentiment['label'],
                                    'sentiment_score': sentiment['score'],
                                    'topic': topic['topic'],
                                    'topic_confidence': topic['confidence'],
                                    'risk_level': risk['level'],
                                    'risk_score': risk['score'],
                                    'explanation': risk['explanation'],
                                })
                            st.session_state['results_df'] = pd.DataFrame(results)
                            st.success(f"✅ Metin analizi tamamlandı! {len(results)} yorum analiz edildi.")
                    except Exception as analysis_error:
                        st.error(f"❌ Analiz sırasında hata: {analysis_error}")
            else:
                st.warning("⚠️ Lütfen analiz edilecek metin girin.")

    if 'uploaded_df' in st.session_state and 'results_df' not in st.session_state:
        st.markdown("---")
        st.markdown("### CSV yüklendi, analiz için hazır.")

    if 'results_df' in st.session_state:
        results_df = st.session_state['results_df']
        st.markdown("---")
        st.markdown(
            """
            <div class='results-panel'>
                <h2 class='results-title'>Analiz Sonuçları</h2>
                <p class='results-subtitle'>Müşteri yorumlarınızdan derinlemesine içgörüler çıkarın.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Temel Metrikler")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f"""
                <div class='kpi-card'>
                    <div class='kpi-value'>{len(results_df)}</div>
                    <div class='kpi-label'>Toplam Yorum</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            neg_ratio = (results_df['sentiment'] == 'negative').mean() * 100
            neg_ratio_formatted = f"{neg_ratio:.1f}%"
            st.markdown(
                f"""
                <div class='kpi-card'>
                    <div class='kpi-value'>{neg_ratio_formatted}</div>
                    <div class='kpi-label'>Olumsuz Oran</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col3:
            high_risk_count = len(results_df[results_df['risk_level'].isin(['high', 'critical'])])
            st.markdown(
                f"""
                <div class='kpi-card'>
                    <div class='kpi-value'>{high_risk_count}</div>
                    <div class='kpi-label'>Yüksek Riskli Yorumlar</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col4:
            dominant_topic = results_df['topic'].mode().iloc[0] if not results_df.empty else "Yok"
            topic_display = dominant_topic.replace('_', ' ').title()
            st.markdown(
                f"""
                <div class='kpi-card'>
                    <div class='kpi-value'>{topic_display}</div>
                    <div class='kpi-label'>Baskın Konu</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### Görsel Analizler")
        col1, col2 = st.columns(2)
        with col1:
            fig_sentiment = px.pie(
                results_df['sentiment'].value_counts(),
                values=results_df['sentiment'].value_counts().values,
                names=results_df['sentiment'].value_counts().index,
                color_discrete_sequence=['#52f2c8', '#ff4fa3', '#7ee7ff'],
            )
            fig_sentiment.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#06131a', width=2)))
            style_plotly(fig_sentiment)
            st.plotly_chart(fig_sentiment, use_container_width=True)
        with col2:
            topic_counts = results_df['topic'].value_counts()
            fig_topic = px.bar(topic_counts, x=topic_counts.index, y=topic_counts.values, color_discrete_sequence=['#52f2c8'])
            fig_topic.update_layout(xaxis_title=None, yaxis_title=None)
            style_plotly(fig_topic)
            st.plotly_chart(fig_topic, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            risk_counts = results_df['risk_level'].value_counts()
            fig_risk = px.bar(risk_counts, x=risk_counts.index, y=risk_counts.values, color_discrete_sequence=['#ff4fa3'])
            fig_risk.update_layout(xaxis_title=None, yaxis_title=None)
            style_plotly(fig_risk)
            st.plotly_chart(fig_risk, use_container_width=True)
        with col4:
            if 'date' in results_df.columns:
                results_df['date'] = pd.to_datetime(results_df['date'], errors='coerce')
                if results_df['date'].notna().any():
                    daily_sentiment = results_df.groupby(results_df['date'].dt.date)['sentiment'].value_counts().unstack().fillna(0)
                    fig_trend = px.line(daily_sentiment, labels={'value': 'Adet', 'date': 'Tarih'}, color_discrete_sequence=['#52f2c8', '#ff4fa3', '#7ee7ff'])
                    style_plotly(fig_trend)
                    st.plotly_chart(fig_trend, use_container_width=True)
                else:
                    st.info("Tarih sütunu geçerli değil veya boş.")
            else:
                st.info("Tarih sütunu mevcut değil.")

        st.markdown("### Sonuçları Filtrele")
        col1, col2, col3 = st.columns(3)
        with col1:
            sentiment_filter = st.multiselect("Duyguya Göre Filtrele", options=results_df['sentiment'].unique(), default=results_df['sentiment'].unique(), key='sentiment_filter')
        with col2:
            topic_filter = st.multiselect("Konuya Göre Filtrele", options=results_df['topic'].unique(), default=results_df['topic'].unique(), key='topic_filter')
        with col3:
            risk_filter = st.multiselect("Risk Seviyesine Göre Filtrele", options=results_df['risk_level'].unique(), default=results_df['risk_level'].unique(), key='risk_filter')

        filtered_df = results_df[
            (results_df['sentiment'].isin(sentiment_filter)) &
            (results_df['topic'].isin(topic_filter)) &
            (results_df['risk_level'].isin(risk_filter))
        ]

        st.markdown("### Detaylı Sonuçlar")
        st.markdown(render_data_table(filtered_df.head(50)), unsafe_allow_html=True)

        st.markdown("### Yüksek Riskli Yorumlar")
        top_risky = filtered_df[filtered_df['risk_level'].isin(['high', 'critical'])].sort_values('risk_score', ascending=False).head(10)
        if not top_risky.empty:
            st.markdown(render_data_table(top_risky), unsafe_allow_html=True)
        else:
            st.info("Filtrelenmiş sonuçlarda yüksek riskli yorum bulunamadı.")

        st.markdown(
            """
            <div class='download-panel'>
                <h3 class='download-title'>Sonuçları İndirin</h3>
                <p class='download-description'>Analiz edilmiş verilerinizi CSV veya PDF formatında dışa aktarın.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            csv_bytes = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button("📄 CSV Olarak İndir", csv_bytes, "analysis_results.csv", "text/csv", key='csv_download_results')
        with col2:
            pdf_buffer = generate_pdf_report(filtered_df)
            st.download_button("📊 PDF Raporu İndir", pdf_buffer, "analysis_report.pdf", "application/pdf", key='pdf_download_results')


if __name__ == "__main__":
    main()
