# Customer Review AI Platform

## Project Overview

This is a comprehensive NLP-based platform for analyzing customer reviews and complaints. It provides sentiment analysis, topic classification, risk assessment, and actionable insights for businesses to understand customer feedback and improve their services.

## Features

- **Sentiment Analysis**: Classifies reviews as positive, neutral, or negative using multilingual BERT models
- **Topic Classification**: Identifies main topics like product quality, shipping, pricing, customer service, etc.
- **Risk Assessment**: Evaluates risk levels (low, medium, high, critical) based on sentiment and content analysis
- **Interactive Dashboard**: Real-time visualizations with KPIs, charts, and filtering capabilities
- **PDF Report Generation**: Automated report creation with summaries and recommendations
- **REST API**: FastAPI backend for programmatic access
- **Multilingual Support**: Works with both Turkish and English reviews
- **File Upload**: CSV upload with flexible column selection

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **NLP**: Transformers, Sentence Transformers
- **Data Processing**: Pandas, Scikit-learn
- **Visualization**: Plotly
- **PDF Generation**: FPDF
- **Deployment**: Ready for Streamlit Cloud and GitHub

## Project Structure

```
customer_review_ai/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .gitignore               # Git ignore file
├── data/
│   └── sample_reviews.csv   # Sample dataset
├── api/
│   ├── __init__.py
│   └── main.py              # FastAPI application
├── src/
│   ├── __init__.py
│   ├── analyzer.py          # Sentiment analysis module
│   ├── topic_engine.py      # Topic classification engine
│   ├── risk_engine.py       # Risk assessment engine
│   ├── reporting.py         # PDF report generation
│   ├── utils.py             # Utility functions
│   └── config.py            # Configuration settings
└── assets/
    └── optional_logo_or_placeholder.txt
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/customer_review_ai.git
   cd customer_review_ai
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Local Development

### Running Streamlit App

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Running FastAPI Backend

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## Usage

1. Upload a CSV file containing customer reviews
2. Select the text column containing reviews
3. Optionally select a date column for trend analysis
4. Click "Start Analysis" to process the data
5. View results in the dashboard with charts and tables
6. Download CSV results or PDF report

## API Endpoints

- `GET /health` - Health check
- `POST /analyze` - Analyze single review
- `POST /analyze-batch` - Analyze multiple reviews

## Sample Data

The `data/sample_reviews.csv` file contains 30 sample reviews in Turkish and English covering various scenarios including positive feedback, complaints about shipping, customer service issues, product quality problems, and high-risk situations.

## GitHub Upload

1. Initialize git repository:
   ```bash
   git init
   ```

2. Add files:
   ```bash
   git add .
   ```

3. Commit:
   ```bash
   git commit -m "Initial commit"
   ```

4. Create repository on GitHub and push:
   ```bash
   git remote add origin https://github.com/yourusername/customer_review_ai.git
   git push -u origin main
   ```

## Streamlit Cloud Deployment

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select the repository and main file path (`app.py`)
5. Deploy!

## Example Workflow

1. User uploads CSV with customer reviews
2. System processes each review through NLP pipeline
3. Sentiment analysis classifies emotional tone
4. Topic engine identifies main complaint areas
5. Risk assessment flags critical issues
6. Dashboard displays aggregated insights
7. PDF report generated with executive summary

## Future Enhancements

- Integration with CRM systems
- Real-time review monitoring
- Advanced topic modeling with BERTopic
- Multi-language support expansion
- Automated email alerts for high-risk reviews
- Integration with social media APIs

## Business Value

This platform helps companies:
- Identify customer pain points quickly
- Prioritize complaint resolution
- Monitor brand reputation
- Reduce customer churn
- Improve product and service quality
- Make data-driven decisions

## Real-world Use Cases

- E-commerce companies analyzing product reviews
- Hotels processing guest feedback
- Restaurants monitoring online reviews
- Customer service teams triaging complaints
- Product teams identifying feature requests

---

Built with ❤️ for better customer understanding