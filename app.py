import streamlit as st
import pandas as pd
from src.analyzer import SentimentAnalyzer
from src.topic_engine import TopicEngine
from src.risk_engine import RiskEngine
from src.reporting import generate_pdf_report
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Müşteri Yorum Analizi Platformu",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    .feature-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-weight: 600;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }
    .upload-section {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border: 2px dashed #cbd5e1;
        text-align: center;
        margin: 2rem 0;
    }
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        text-align: center;
        margin: 0.5rem;
    }
    .chart-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin: 0.5rem;
    }
    .download-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin: 0.5rem;
    }
    .sentiment-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    .sentiment-positive { background-color: #dcfce7; color: #166534; }
    .sentiment-neutral { background-color: #fef3c7; color: #92400e; }
    .sentiment-negative { background-color: #fee2e2; color: #991b1b; }
    .risk-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    .risk-low { background-color: #f0fdf4; color: #166534; }
    .risk-medium { background-color: #fef3c7; color: #92400e; }
    .risk-high { background-color: #fed7d7; color: #c53030; }
    .risk-critical { background-color: #feb2b2; color: #9b2c2c; }
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e3a8a;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    }
    .stFileUploader>div>div>div>button {
        background: #f1f5f9;
        color: #475569;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize analyzers
sentiment_analyzer = SentimentAnalyzer()
topic_engine = TopicEngine()
risk_engine = RiskEngine()

def create_sentiment_badge(sentiment):
    if sentiment == 'positive':
        return f'<span class="sentiment-badge sentiment-positive">Olumlu</span>'
    elif sentiment == 'negative':
        return f'<span class="sentiment-badge sentiment-negative">Olumsuz</span>'
    else:
        return f'<span class="sentiment-badge sentiment-neutral">Nötr</span>'

def create_risk_badge(risk_level):
    if risk_level == 'low':
        return f'<span class="risk-badge risk-low">Düşük Risk</span>'
    elif risk_level == 'medium':
        return f'<span class="risk-badge risk-medium">Orta Risk</span>'
    elif risk_level == 'high':
        return f'<span class="risk-badge risk-high">Yüksek Risk</span>'
    else:
        return f'<span class="risk-badge risk-critical">Kritik Risk</span>'

def main():
    # Sidebar
    with st.sidebar:
        st.title("📊 Hakkında")
        st.markdown("""
        **Müşteri Yorum Analizi Platformu**
        
        Gelişmiş AI kullanarak müşteri geri bildirimlerini analiz eder:
        - Duygu tespiti (olumlu/nötr/olumsuz)
        - Şikayet konularını belirleme
        - Risk seviyelerini değerlendirme
        - İşletme için uygulanabilir içgörüler üretme
        
        **Kullanım:**
        1. Müşteri yorumlarını içeren CSV dosyasını yükleyin
        2. Metin sütununu seçin
        3. "Analizi Başlat" butonuna tıklayın
        4. Sonuçları görüntüleyin ve raporları indirin
        """)
        
        st.markdown("---")
        st.markdown("**Teknolojiler:** Streamlit, Transformers, Plotly")
    
    # Hero Section
    st.markdown('<h1 class="main-header">Müşteri Yorum & Şikayet Analiz Platformu</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Müşteri geri bildirimlerini analiz edin, riskleri tespit edin, şikayet konularını belirleyin ve yüklenen CSV dosyalarından işletme için uygulanabilir içgörüler üretin.</p>', unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">😊</div>
            <div class="feature-title">Duygu Analizi</div>
            <p>Gelişmiş NLP modelleri kullanarak yorumları olumlu, nötr veya olumsuz olarak sınıflandırın.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏷️</div>
            <div class="feature-title">Konu Tespiti</div>
            <p>Kargo, kalite, hizmet ve fiyatlandırma gibi ana şikayet kategorilerini belirleyin.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚠️</div>
            <div class="feature-title">Risk Puanlama</div>
            <p>İçerik analizi ve duyguya göre düşükten kritik seviyeye kadar riskleri değerlendirin.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📈</div>
            <div class="feature-title">Uygulanabilir İçgörüler</div>
            <p>Öneriler ve trend analizi ile işletme zekası raporları üretin.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Upload Section
    st.markdown("---")
    st.markdown('<h2 class="section-title">📁 Verilerinizi Yükleyin</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="upload-section">
        <h3>CSV Dosyası Yükleyin</h3>
        <p>AI destekli analizi başlatmak için müşteri yorumlarını veya şikayetlerini içeren bir veri seti yükleyin.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("", type=['csv'], label_visibility="collapsed")
    
    if uploaded_file is not None:
        try:
            # Try reading with different encodings
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8', dtype=str)
            except:
                df = pd.read_csv(uploaded_file, encoding='latin-1', dtype=str)
            
            if df.empty:
                st.error("❌ CSV dosyası boş. Lütfen veriler içeren bir dosya yükleyin.")
            else:
                st.success(f"✅ Dosya başarıyla yüklendi! ({len(df)} satır, {len(df.columns)} sütun)")
                st.info(f"📋 Sütunlar: {', '.join(df.columns.tolist())}")
                
                # Column selection
                st.markdown("---")
                st.markdown('<h3 class="section-title">⚙️ Analizi Yapılandırın</h3>', unsafe_allow_html=True)
                
                text_columns = list(df.columns)
                
                if not text_columns:
                    st.error("❌ Sütun bulunamadı. CSV dosyanız okunamadı.")
                else:
                    selected_text_col = st.selectbox("Yorum metni sütununu seçin", text_columns)
                    
                    date_columns = [col for col in df.columns if col.lower().find('date') != -1 or col.lower().find('tarih') != -1]
                    if not date_columns:
                        date_columns = list(df.columns)
                    
                    selected_date_col = st.selectbox("Tarih sütununu seçin (opsiyonel)", ['Yok'] + date_columns)
                    if selected_date_col == 'Yok':
                        selected_date_col = None
                    
                    if st.button("🚀 Analizi Başlat", type="primary"):
                        with st.spinner("🔄 Yorumlar analiz ediliyor... Bu birkaç dakika sürebilir."):
                            try:
                                # Perform analysis
                                results = []
                                for idx, row in df.iterrows():
                                    text = str(row[selected_text_col]).strip()
                                    if not text or text.lower() == 'nan':
                                        continue
                                    
                                    sentiment = sentiment_analyzer.analyze(text)
                                    topic = topic_engine.classify_topic(text)
                                    risk = risk_engine.assess_risk(text, sentiment)
                                    
                                    result = {
                                        'review_id': idx + 1,
                                        'review_text': text,
                                        'sentiment': sentiment['label'],
                                        'sentiment_score': sentiment['score'],
                                        'topic': topic['topic'],
                                        'topic_confidence': topic['confidence'],
                                        'risk_level': risk['level'],
                                        'risk_score': risk['score'],
                                        'explanation': risk['explanation']
                                    }
                                    if selected_date_col:
                                        try:
                                            result['date'] = row[selected_date_col]
                                        except:
                                            pass
                                    results.append(result)
                                
                                if results:
                                    results_df = pd.DataFrame(results)
                                    
                                    # Store in session state
                                    st.session_state['results_df'] = results_df
                                    st.session_state['original_df'] = df
                                    st.success(f"✅ Analiz tamamlandı! {len(results_df)} yorum analiz edildi.")
                                else:
                                    st.warning("⚠️ Analiz edilecek geçerli yorum bulunamadı.")
                            except Exception as analysis_error:
                                st.error(f"❌ Analiz sırasında hata: {str(analysis_error)}")
                    
        except Exception as e:
            error_msg = str(e) if str(e) else "Dosya işlenirken bilinmeyen bir hata oluştu"
            st.error(f"❌ Dosya işlenirken hata: {error_msg}\n\nÖnerileri:\n- CSV dosyasının UTF-8 encoding ile kaydedildiğini kontrol edin\n- Dosyada satır başında/sonunda boşluk olup olmadığını kontrol edin")
    
    # Display results if available
    if 'results_df' in st.session_state:
        results_df = st.session_state['results_df']
        
        st.markdown("---")
        st.markdown('<h2 class="section-title">📊 Analiz Sonuçları</h2>', unsafe_allow_html=True)
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <h3>{len(results_df)}</h3>
                <p>Toplam Yorum</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            neg_ratio = (results_df['sentiment'] == 'negative').mean() * 100
            st.markdown(f"""
            <div class="kpi-card">
                <h3>{neg_ratio:.1f}%</h3>
                <p>Olumsuz Oran</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            high_risk_count = len(results_df[results_df['risk_level'].isin(['high', 'critical'])])
            st.markdown(f"""
            <div class="kpi-card">
                <h3>{high_risk_count}</h3>
                <p>Yüksek Riskli Yorumlar</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            dominant_topic = results_df['topic'].mode().iloc[0] if not results_df.empty else "Yok"
            st.markdown(f"""
            <div class="kpi-card">
                <h3>{dominant_topic.replace('_', ' ').title()}</h3>
                <p>Baskın Konu</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts
        st.markdown('<h3 class="section-title">📈 Görselleştirmeler</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            sentiment_counts = results_df['sentiment'].value_counts()
            fig_sentiment = px.pie(sentiment_counts, values=sentiment_counts.values, names=sentiment_counts.index, title="Duygu Dağılımı")
            st.plotly_chart(fig_sentiment, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            topic_counts = results_df['topic'].value_counts()
            fig_topic = px.bar(topic_counts, x=topic_counts.index, y=topic_counts.values, title="Konu Dağılımı")
            st.plotly_chart(fig_topic, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            risk_counts = results_df['risk_level'].value_counts()
            fig_risk = px.bar(risk_counts, x=risk_counts.index, y=risk_counts.values, title="Risk Dağılımı")
            st.plotly_chart(fig_risk, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            if 'date' in results_df.columns:
                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                results_df['date'] = pd.to_datetime(results_df['date'])
                daily_sentiment = results_df.groupby(results_df['date'].dt.date)['sentiment'].value_counts().unstack().fillna(0)
                fig_trend = px.line(daily_sentiment, title="Zaman İçinde Duygu Trendi")
                st.plotly_chart(fig_trend, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Tarih sütunu seçilmediği için zaman çizelgesi analizi mevcut değil")
        
        # Filters
        st.markdown('<h3 class="section-title">🔍 Sonuçları Filtrele</h3>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            sentiment_filter = st.multiselect("Duyguya Göre Filtrele", options=results_df['sentiment'].unique(), default=results_df['sentiment'].unique())
        with col2:
            topic_filter = st.multiselect("Konuya Göre Filtrele", options=results_df['topic'].unique(), default=results_df['topic'].unique())
        with col3:
            risk_filter = st.multiselect("Risk Seviyesine Göre Filtrele", options=results_df['risk_level'].unique(), default=results_df['risk_level'].unique())
        
        filtered_df = results_df[
            (results_df['sentiment'].isin(sentiment_filter)) &
            (results_df['topic'].isin(topic_filter)) &
            (results_df['risk_level'].isin(risk_filter))
        ]
        
        # Detailed Table
        st.markdown('<h3 class="section-title">📋 Detaylı Sonuçlar</h3>', unsafe_allow_html=True)
        
        # Create table with badges
        table_data = []
        for _, row in filtered_df.head(50).iterrows():
            table_data.append({
                'ID': row['review_id'],
                'Yorum Metni': row['review_text'][:100] + "..." if len(row['review_text']) > 100 else row['review_text'],
                'Duygu': create_sentiment_badge(row['sentiment']),
                'Konu': row['topic'].replace('_', ' ').title(),
                'Risk Seviyesi': create_risk_badge(row['risk_level']),
                'Açıklama': row['explanation']
            })
        
        table_df = pd.DataFrame(table_data)
        st.markdown(table_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        # Top Risky Reviews
        st.markdown('<h3 class="section-title">⚠️ En Riskli Yorumlar</h3>', unsafe_allow_html=True)
        top_risky = filtered_df[filtered_df['risk_level'].isin(['high', 'critical'])].sort_values('risk_score', ascending=False).head(10)
        
        if not top_risky.empty:
            risky_data = []
            for _, row in top_risky.iterrows():
                risky_data.append({
                    'ID': row['review_id'],
                    'Yorum Metni': row['review_text'][:150] + "..." if len(row['review_text']) > 150 else row['review_text'],
                    'Duygu': create_sentiment_badge(row['sentiment']),
                    'Konu': row['topic'].replace('_', ' ').title(),
                    'Risk Seviyesi': create_risk_badge(row['risk_level']),
                    'Risk Skoru': f"{row['risk_score']:.2f}"
                })
            
            risky_df = pd.DataFrame(risky_data)
            st.markdown(risky_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.info("Filtrelenmiş sonuçlarda yüksek riskli yorum bulunamadı")
        
        # Downloads
        st.markdown('<h3 class="section-title">💾 Sonuçları İndir</h3>', unsafe_allow_html=True)
        
        st.markdown('<div class="download-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            csv = filtered_df.to_csv(index=False)
            st.download_button("📄 Analiz Edilmiş CSV'yi İndir", csv, "analysis_results.csv", "text/csv", use_container_width=True)
        
        with col2:
            pdf_buffer = generate_pdf_report(filtered_df)
            st.download_button("📊 PDF Raporu İndir", pdf_buffer, "analysis_report.pdf", "application/pdf", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()