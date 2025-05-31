"""
FastAPI application for AI News Analyzer
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
from typing import Optional, Union
import os

from app.models.schemas import AnalysisRequest, AnalysisResponse
from app.services.ai_service import AIService
from app.services.file_processor import FileProcessor
from app.utils.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI News Analyzer",
    description="Analyze news articles with AI to generate summaries and extract geopolitical entities",
    version="1.0.0"
)

# Get settings
settings = get_settings()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ai_service = AIService(settings.openai_api_key)
file_processor = FileProcessor()

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_article(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    """
    Analyze a news article and return summary and geopolitical entities
    
    Args:
        file: Optional uploaded file (.txt or .docx)
        text: Optional text content
    
    Returns:
        AnalysisResponse with summary and geopolitical entities
    """
    try:
        if not file and not text:
            raise HTTPException(
                status_code=400,
                detail="Either file or text must be provided"
            )
        
        if file:
            logger.info(f"Processing uploaded file: {file.filename}")
            
            if not file.filename.lower().endswith(('.txt', '.docx')):
                raise HTTPException(
                    status_code=400,
                    detail="Only .txt and .docx files are supported"
                )
            
            file_content = await file.read()
            article_text = await file_processor.process_file(file_content, file.filename)
            
        else:
            logger.info("Processing text input")
            article_text = text
        
        if not article_text or len(article_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Article text is too short (minimum 50 characters required)"
            )
        
        logger.info("Starting AI analysis")
        summary, geopolitical_entities = await ai_service.analyze_article(article_text)
        
        return AnalysisResponse(
            summary=summary,
            geopolitical_entities=geopolitical_entities
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing article: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the article"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=settings.environment == "development"
    )