"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AnalysisRequest(BaseModel):
    """Request model for article analysis"""
    text: str = Field(..., min_length=50, description="Article text content")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Breaking news: The United States and China have reached a new trade agreement..."
            }
        }

class AnalysisResponse(BaseModel):
    """Response model for article analysis"""
    summary: str = Field(..., description="AI-generated summary of the article")
    nationalities: List[str] = Field(..., description="List of nationalities/countries mentioned")
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "The United States and China have finalized a comprehensive trade agreement that will reduce tariffs and increase bilateral trade volume.",
                "nationalities": ["American", "Chinese"]
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str = Field(..., description="Error message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "An error occurred while processing the request"
            }
        }