"""
AI Service for article analysis using OpenAI GPT
"""
import openai
import asyncio
import logging
from typing import Tuple, List
import json
import re

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI-powered article analysis"""
    
    def __init__(self, api_key: str):
        """Initialize AI service with OpenAI API key"""
        self.client = openai.AsyncOpenAI(api_key=api_key)
        
    async def analyze_article(self, article_text: str) -> Tuple[str, List[str]]:
        """
        Analyze article to generate summary and extract nationalities
        
        Args:
            article_text: The news article text
            
        Returns:
            Tuple of (summary, list of nationalities)
        """
        try:
            # Run both analyses concurrently for better performance
            summary_task = self._generate_summary(article_text)
            nationalities_task = self._extract_nationalities(article_text)
            
            summary, nationalities = await asyncio.gather(
                summary_task, 
                nationalities_task
            )
            
            return summary, nationalities
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            raise
    
    async def _generate_summary(self, article_text: str) -> str:
        """Generate a concise summary of the article"""
        
        prompt = f"""
        Please provide a concise and informative summary of the following news article. 
        The summary should:
        - Be 2 to 3 sentences long
        - Capture the main points and key information
        - Be written in clear, professional language
        - Focus on the most important facts and developments
        
        Article:
        {article_text}
        
        Summary:
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional news summarizer. Provide clear, concise, and accurate summaries of news articles."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info(f"Generated summary: {summary[:100]}...")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise
    
    async def _extract_nationalities(self, article_text: str) -> List[str]:
        """Extract nationalities and countries mentioned in the article"""
        
        prompt = f"""
        Analyze the following news article and extract the following entities with a focus on geopolitical and named entity recognition
        
        - Countries mentioned explicitly or implicitly in the article
        - Nationality adjectives, peoples, or demonyms referenced (e.g., 'French', 'Syrian', 'Kurds')
        - People mentioned by name (e.g., political leaders, public figures, spokespersons)
        - Organizations involved or referenced (e.g., United Nations, Red Cross, Ministère de l’Intérieur)
        - The input article may be written in English, French, or a combination of both. Your extraction must support multilingual content and apply language-aware parsing and named entity recognition to accurately identify relevant countries, nationalities, people, and organizations.
        - Use standardized country/nationality names
        - If no nationalities are found, return an empty array
        
        Article:
        {article_text}
        
        Response format: ["Country1", "Country2", "Nationality1"]
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert information extractor for international news articles. Your job is to analyze a news article (in English, French, or both), and extract geopolitical and entity data. Return only valid JSON arrays."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            
            try:
                # Try to parse as JSON directly
                nationalities = json.loads(content)
                if isinstance(nationalities, list):
                    nationalities = list(set([n.strip() for n in nationalities if n.strip()]))
                    return nationalities
                else:
                    logger.warning("Invalid response format, returning empty list")
                    return []
                    
            except json.JSONDecodeError:
                logger.warning("Could not parse nationalities from AI response")
                return []
            
        except Exception as e:
            logger.error(f"Error extracting nationalities: {str(e)}")
            return []