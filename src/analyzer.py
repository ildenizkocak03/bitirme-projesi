from transformers import pipeline
import torch

class SentimentAnalyzer:
    def __init__(self):
        # Use multilingual sentiment model
        self.model = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment",
            tokenizer="nlptown/bert-base-multilingual-uncased-sentiment",
            device=0 if torch.cuda.is_available() else -1
        )
    
    def analyze(self, text: str) -> dict:
        """
        Analyze sentiment of the given text.
        
        Args:
            text (str): The review text to analyze
            
        Returns:
            dict: Contains 'label' (positive/neutral/negative) and 'score' (confidence)
        """
        if not text or not text.strip():
            return {"label": "neutral", "score": 0.0}
        
        try:
            result = self.model(text)[0]
            label = result['label']
            score = result['score']
            
            # Map star ratings to sentiment labels
            if label in ['1 star', '2 stars']:
                sentiment = 'negative'
            elif label in ['4 stars', '5 stars']:
                sentiment = 'positive'
            else:
                sentiment = 'neutral'
            
            return {"label": sentiment, "score": score}
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {"label": "neutral", "score": 0.0}