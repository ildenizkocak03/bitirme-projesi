import re

class RiskEngine:
    def __init__(self):
        # High-risk keywords (Turkish and English)
        self.high_risk_keywords = [
            'dava', 'lawsuit', 'şikayet', 'complaint', 'rezalet', 'scandal', 'mağdur', 'victim',
            'aldatmaca', 'deception', 'dolandırıcılık', 'fraud', 'sahte', 'fake', 'threat',
            'tehdit', 'boycott', 'boykot', 'social media', 'sosyal medya', 'viral', 'skandal'
        ]
        
        # Medium-risk keywords
        self.medium_risk_keywords = [
            'iptal', 'cancel', 'iade', 'return', 'şikayetçi', 'complainer', 'şikayet',
            'refund', 'geri ödeme', 'müşteri hizmetleri', 'customer service', 'bekleme',
            'waiting', 'gecikme', 'delay', 'kırık', 'broken', 'arıza', 'defect'
        ]
    
    def assess_risk(self, text: str, sentiment: dict) -> dict:
        """
        Assess risk level based on text content and sentiment.
        
        Args:
            text (str): The review text
            sentiment (dict): Sentiment analysis result
            
        Returns:
            dict: Contains 'level', 'score', and 'explanation'
        """
        if not text or not text.strip():
            return {"level": "low", "score": 0.0, "explanation": "No content to analyze"}
        
        try:
            text_lower = text.lower()
            score = 0.0
            
            # Sentiment-based scoring
            if sentiment['label'] == 'negative':
                score += 0.4
            elif sentiment['label'] == 'neutral':
                score += 0.1
            
            # Keyword-based scoring
            high_risk_count = sum(1 for keyword in self.high_risk_keywords if keyword in text_lower)
            medium_risk_count = sum(1 for keyword in self.medium_risk_keywords if keyword in text_lower)
            
            score += high_risk_count * 0.3
            score += medium_risk_count * 0.15
            
            # Length factor (longer complaints might be more serious)
            if len(text.split()) > 50:
                score += 0.1
            
            # Cap score at 1.0
            score = min(score, 1.0)
            
            # Determine risk level
            if score >= 0.8:
                level = "critical"
                explanation = "High-risk complaint with potential legal or reputational impact"
            elif score >= 0.5:
                level = "high"
                explanation = "Significant risk requiring immediate attention"
            elif score >= 0.3:
                level = "medium"
                explanation = "Moderate risk that should be monitored"
            else:
                level = "low"
                explanation = "Low risk, standard customer feedback"
            
            return {"level": level, "score": score, "explanation": explanation}
        except Exception as e:
            print(f"Risk assessment error: {e}")
            return {"level": "low", "score": 0.0, "explanation": "Analysis failed"}