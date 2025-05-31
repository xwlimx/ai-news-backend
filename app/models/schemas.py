"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
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
    geopolitical_entities: dict[str, list[str]] = Field(
        ..., 
        description="Categorized geopolitical entities including countries, nationalities, people, and organizations"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "The United States and China have finalized a comprehensive trade agreement that will reduce tariffs and increase bilateral trade volume.",
                "geopolitical_entities": {
                    "countries": ["United States", "China"],
                    "nationalities": ["American", "Chinese"],
                    "people": ["Joe Biden", "Xi Jinping"],
                    "organizations": ["U.S. Trade Representative", "Ministry of Commerce"]
                }
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