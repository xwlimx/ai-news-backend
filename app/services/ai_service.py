"""
AI Service for article analysis using OpenAI GPT
"""
import openai
import asyncio
import logging
import json
import re

logger = logging.getLogger(__name__)


class AIService:
    """Service for AI-powered article analysis"""
    
    def __init__(self, api_key: str):
        """Initialize AI service with OpenAI API key"""
        self.client = openai.AsyncOpenAI(api_key=api_key)
        
    async def analyze_article(self, article_text: str) -> tuple[str, list[str]]:
        """
        Analyze article to generate summary and extract geopolitical entities
        
        Args:
            article_text: The news article text
            
        Returns:
            tuple of (summary, list of geopolitical entities)
        """
        try:
            # Run both analyses concurrently for better performance
            summary_task = self._generate_summary(article_text)
            geopolitical_entities = self._extract_geopolitical_entities(article_text)
            
            summary, geopolitical_entities = await asyncio.gather(
                summary_task, 
                geopolitical_entities
            )
            
            return summary, geopolitical_entities
            
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
            logger.info(f"Analysis complete - Summary: {len(summary)} chars, {summary[:100]}...")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise
    
    async def _extract_geopolitical_entities(self, article_text: str) -> dict[str, list[str]]:
        """Extract countries, nationalities, people, and organizations from article"""
        
        # Default empty structure
        default_entities = {
            "countries": [],
            "nationalities": [],
            "people": [],
            "organizations": []
        }
        
        prompt = f"""
        Analyze the following news article and extract the following entities with a focus on geopolitical and named entity recognition
        
        - Countries mentioned explicitly or implicitly in the article
        - Nationality adjectives, peoples, or demonyms referenced (e.g., 'French', 'Syrian', 'Kurds')
        - People mentioned by name (e.g., political leaders, public figures, spokespersons)
        - Organizations involved or referenced this should include only actual entities such as:
            - Government bodies
            - International organizations
            - Non-governmental organizations (NGOs)
            - Sports federations and official associations (e.g., "Asian Athletics Association", not just the event "Asian Athletics Championships")
            - Companies or official groups
            - Do not include names of competitions, events, or locations unless they are also the name of the organizing body
        - The input article may be written in English, French, or a combination of both. Your extraction must support multilingual content and apply language-aware parsing and named entity recognition to accurately identify relevant countries, nationalities, people, and organizations.
        - Use standardized country/nationality names
        - If no nationalities are found, return an empty array
        
        Article:
        {article_text}
        
        Response format (valid JSON only): {{
            "countries": ["Country1", "Country2"],
            "nationalities": ["Nationality1", "Nationality2"],
            "people": ["Person1", "Person2"],
            "organizations": ["Organization1", "Organization2"]
        }}
        """
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4.1",
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
                raw_entities = json.loads(content)
                if isinstance(raw_entities, dict):
                    # Clean and deduplicate each category
                    for category in default_entities.keys():
                        if category in raw_entities and isinstance(raw_entities[category], list):
                            cleaned_list = list(set([
                                item.strip() 
                                for item in raw_entities[category] 
                                if item and item.strip()
                            ]))
                            default_entities[category] = cleaned_list
                    
                    entity_counts = {category: len(entities) for category, entities in default_entities.items()}
                    total_entities = sum(entity_counts.values())
                    
                    logger.info(
                        f"Analysis complete - "
                        f"Entities: {total_entities} in total, "
                        f"countries: {entity_counts['countries']}, "
                        f"nationalities: {entity_counts['nationalities']}, "
                        f"people: {entity_counts['people']}, "
                        f"organizations: {entity_counts['organizations']}"
                    )
                    return default_entities
                else:
                    logger.warning("Invalid response format, returning empty list")
                    return default_entities
                    
            except json.JSONDecodeError:
                logger.warning("Could not parse geopolitical entities from AI response")
                return default_entities
            
        except Exception as e:
            logger.error(f"Error extracting geopolitical entities: {str(e)}")
            return default_entities