# AI News Analyzer

A full-stack web application that analyzes news articles using AI to provide summaries and extract mentioned nationalities/countries.

## Project Structure

```
ai-news-backend/
├── app/			# FastAPI Python application
└── README.md
```

## Technology Stack

### Backend
- **FastAPI**: 0.115.12
- **Python**: 3.13+
- **OpenAI**: 1.3.7
- **python-multipart**: 0.0.6
- **python-docx**: 1.1.0
- **uvicorn**: 0.24.0

### Cloud Infrastructure
- **AWS Elastic Beanstalk** (Backend)

## Setup Instructions

### Prerequisites
- Python 3.13+
- OpenAI API key

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd ai-news-backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment configuration:**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

4. **Run development server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Deployment

### Backend Deployment (AWS Elastic Beanstalk)

1. **Prepare Your Application:**
   ```bash
	ai-news-backend/
	├── app/	
	├──── main.py         		 # FastAPI app
	├── requirements.txt         # list of Python dependencies
	├── Procfile                 # tell EB how to run your app
   ```

2. **Create a Procfile:**
   ```bash
   web: uvicorn app.main:app --host=0.0.0.0 --port=8000
   ```

3. **Zip Your Application Files:**
   ```bash
   Select all files and folders inside your project root (not the root folder itself)
   Compress them into a single zip file, e.g., myapp.zip.
   ```

4. **Upload and Deploy Zip File:**
   ```bash
   Log in to AWS Management Console.
   Navigate to Elastic Beanstalk service.
   In your environment dashboard, click Upload and deploy.
   Click Deploy.
   ```

## API Documentation

### POST /analyze

Analyzes a news article and returns summary and nationalities.

**Request:**
- Content-Type: `multipart/form-data` or `application/json`
- Body: 
  - File upload: `file` (text/docx)
  - Text input: `{"text": "article content"}`

**Response:**
```json
{
  "summary": "Brief summary of the article...",
  "geopolitical_entities": {
		"countries": ["United States", "China"],
		"nationalities": ["American", "Chinese"],
		"people": ["Joe Biden", "Xi Jinping"],
		"organizations": ["U.S. Trade Representative", "Ministry of Commerce"]
	}
}
```

**Error Response:**
```json
{
  "detail": "Error message"
}
```

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=XXX
CORS_ORIGINS=http://localhost:3000,https://main.dlimtlzxpr8ax.amplifyapp.com/
```

## Enhancement Considerations

- Implement rate limiting for the API
- Add authentication
- Implement caching for repeated analyses