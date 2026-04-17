import pandas as pd
from typing import List, Dict, Any

def validate_csv_columns(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """
    Validate that required columns exist in the dataframe.
    
    Args:
        df (pd.DataFrame): Input dataframe
        required_columns (List[str]): List of required column names
        
    Returns:
        bool: True if all required columns exist
    """
    return all(col in df.columns for col in required_columns)

def clean_text(text: str) -> str:
    """
    Clean and preprocess text data.
    
    Args:
        text (str): Input text
        
    Returns:
        str: Cleaned text
    """
    if not isinstance(text, str):
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text.strip()

def calculate_summary_stats(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate summary statistics from analysis results.
    
    Args:
        results (List[Dict[str, Any]]): List of analysis result dictionaries
        
    Returns:
        Dict[str, Any]: Summary statistics
    """
    if not results:
        return {}
    
    df = pd.DataFrame(results)
    
    stats = {
        'total_reviews': len(df),
        'sentiment_distribution': df['sentiment'].value_counts().to_dict(),
        'topic_distribution': df['topic'].value_counts().to_dict(),
        'risk_distribution': df['risk_level'].value_counts().to_dict(),
        'avg_sentiment_score': df['sentiment_score'].mean(),
        'avg_risk_score': df['risk_score'].mean(),
        'high_risk_percentage': ((df['risk_level'] == 'high') | (df['risk_level'] == 'critical')).mean() * 100
    }
    
    return stats