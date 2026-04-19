from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class TopicEngine:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        
        # Predefined topics with example phrases
        self.topics = {
            'product_quality': [
                'quality', 'durability', 'material', 'build', 'defective', 'broken', 'poor quality',
                'kalite', 'dayanıklılık', 'malzeme', 'yapı', 'arıza', 'kırık', 'kötü kalite'
            ],
            'shipping_delivery': [
                'shipping', 'delivery', 'courier', 'package', 'late', 'delayed', 'tracking',
                'kargo', 'teslimat', 'kurye', 'paket', 'geç', 'gecikme', 'takip'
            ],
            'pricing_value': [
                'price', 'cost', 'expensive', 'cheap', 'value', 'worth', 'overpriced',
                'fiyat', 'pahalı', 'ucuz', 'değer', 'karşılaştırma', 'pahalı'
            ],
            'customer_service': [
                'service', 'support', 'help', 'response', 'staff', 'representative', 'unhelpful',
                'hizmet', 'destek', 'yardım', 'yanıt', 'personel', 'yardımcı olmamak'
            ],
            'returns_refunds': [
                'return', 'refund', 'exchange', 'policy', 'process', 'difficult', 'refunded',
                'iade', 'geri ödeme', 'değişim', 'politika', 'süreç', 'zor'
            ],
            'payment_billing': [
                'payment', 'billing', 'charge', 'transaction', 'fee', 'invoice', 'error',
                'ödeme', 'faturalandırma', 'ücret', 'işlem', 'ücret', 'fatura', 'hata'
            ],
            'app_experience': [
                'app', 'application', 'website', 'interface', 'bug', 'crash', 'slow',
                'uygulama', 'web sitesi', 'arayüz', 'hata', 'çökme', 'yavaş'
            ],
            'general': [
                'general', 'overall', 'experience', 'satisfaction', 'recommend', 'average',
                'genel', 'deneyim', 'memnuniyet', 'tavsiye', 'ortalama'
            ]
        }
        
        # Pre-compute topic embeddings
        self.topic_embeddings = {}
        for topic, phrases in self.topics.items():
            embeddings = self.model.encode(phrases)
            self.topic_embeddings[topic] = np.mean(embeddings, axis=0)
    
    def classify_topic(self, text: str) -> dict:
        """
        Classify the main topic of the review.
        
        Args:
            text (str): The review text
            
        Returns:
            dict: Contains 'topic' and 'confidence' score
        """
        if not text or not text.strip():
            return {"topic": "general", "confidence": 0.0}
        
        try:
            text_embedding = self.model.encode([text])[0]
            
            similarities = {}
            for topic, topic_embedding in self.topic_embeddings.items():
                similarity = cosine_similarity([text_embedding], [topic_embedding])[0][0]
                similarities[topic] = similarity
            
            best_topic = max(similarities, key=similarities.get)
            confidence = similarities[best_topic]
            
            return {"topic": best_topic, "confidence": float(confidence)}
        except Exception as e:
            print(f"Topic classification error: {e}")
            return {"topic": "general", "confidence": 0.0}