from fpdf import FPDF
import pandas as pd
from datetime import datetime
from io import BytesIO

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Customer Review AI Analysis Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(results_df: pd.DataFrame) -> BytesIO:
    """
    Generate a PDF report from analysis results.
    
    Args:
        results_df (pd.DataFrame): Analysis results dataframe
        
    Returns:
        BytesIO: PDF content as bytes buffer
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    # Report metadata
    pdf.cell(0, 10, f'Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1)
    pdf.ln(5)
    
    # Summary statistics
    total_reviews = len(results_df)
    sentiment_dist = results_df['sentiment'].value_counts()
    topic_dist = results_df['topic'].value_counts()
    risk_dist = results_df['risk_level'].value_counts()
    
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Executive Summary', 0, 1)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Total Reviews Analyzed: {total_reviews}', 0, 1)
    pdf.cell(0, 10, f'Positive Sentiment: {sentiment_dist.get("positive", 0)} ({sentiment_dist.get("positive", 0)/total_reviews*100:.1f}%)', 0, 1)
    pdf.cell(0, 10, f'Negative Sentiment: {sentiment_dist.get("negative", 0)} ({sentiment_dist.get("negative", 0)/total_reviews*100:.1f}%)', 0, 1)
    pdf.cell(0, 10, f'High/Critical Risk Reviews: {risk_dist.get("high", 0) + risk_dist.get("critical", 0)}', 0, 1)
    pdf.ln(5)
    
    # Top topics
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Top Complaint Topics', 0, 1)
    pdf.set_font('Arial', '', 12)
    for topic, count in topic_dist.head(5).items():
        pdf.cell(0, 10, f'{topic.replace("_", " ").title()}: {count} reviews', 0, 1)
    pdf.ln(5)
    
    # Risk assessment
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Risk Assessment', 0, 1)
    pdf.set_font('Arial', '', 12)
    for level, count in risk_dist.items():
        pdf.cell(0, 10, f'{level.title()} Risk: {count} reviews', 0, 1)
    pdf.ln(5)
    
    # Action recommendations
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Recommended Actions', 0, 1)
    pdf.set_font('Arial', '', 12)
    
    if risk_dist.get('critical', 0) > 0:
        pdf.cell(0, 10, '- Immediate attention required for critical risk reviews', 0, 1)
        pdf.cell(0, 10, '- Consider legal review for potential lawsuits or fraud claims', 0, 1)
    
    if risk_dist.get('high', 0) > 0:
        pdf.cell(0, 10, '- Prioritize resolution of high-risk customer issues', 0, 1)
        pdf.cell(0, 10, '- Review customer service processes and response times', 0, 1)
    
    top_topic = topic_dist.idxmax()
    pdf.cell(0, 10, f'- Focus improvement efforts on {top_topic.replace("_", " ")} issues', 0, 1)
    
    if sentiment_dist.get('negative', 0) / total_reviews > 0.3:
        pdf.cell(0, 10, '- Implement customer satisfaction improvement program', 0, 1)
    
    # Convert to BytesIO
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    
    return buffer