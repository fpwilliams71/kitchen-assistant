import openai
import os
import logging
from typing import Dict, List, Optional

# Use absolute import
from app.models.recipe_models import AIResponse

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment")
        
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
    
    async def get_cooking_instructions(self, recipe_name: str, user_ingredients: List[str]) -> AIResponse:
        """Get AI-powered cooking instructions"""
        if not self.client:
            return AIResponse(
                success=False,
                error="OpenAI API key not configured"
            )
        
        try:
            prompt = f"""
            Provide detailed cooking instructions for {recipe_name} using these ingredients: {', '.join(user_ingredients)}.
            Format the response as:
            - Preparation steps
            - Cooking steps  
            - Estimated time
            - Difficulty level
            - Tips and variations
            
            Be conversational and encouraging.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional chef assistant helping home cooks."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return AIResponse(
                success=True,
                instructions=response.choices[0].message.content
            )
            
        except Exception as e:
            logger.error(f"AI service error: {str(e)}")
            return AIResponse(success=False, error=str(e))
    
    async def answer_cooking_question(self, question: str, context: str = "") -> AIResponse:
        """Answer cooking-related questions"""
        if not self.client:
            return AIResponse(
                success=False,
                error="OpenAI API key not configured"
            )
            
        try:
            prompt = f"""
            Context: {context}
            Question: {question}
            
            Answer this cooking question helpfully and accurately. If it's about technique, explain clearly.
            If you need more information, ask follow-up questions.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable cooking assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
            
            return AIResponse(
                success=True,
                answer=response.choices[0].message.content
            )
            
        except Exception as e:
            return AIResponse(success=False, error=str(e))

ai_service = AIService()