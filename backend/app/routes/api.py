from fastapi import APIRouter, HTTPException
from typing import List

# Use absolute imports
from app.models.recipe_models import CookingRequest, QuestionRequest
from app.services.ai_service import ai_service
from app.services.speech_service import speech_service
from app.services.recipe_service import recipe_service

router = APIRouter()

@router.post("/cooking-instructions")
async def get_cooking_instructions(request: CookingRequest):
    """Get AI-generated cooking instructions"""
    result = await ai_service.get_cooking_instructions(
        request.recipe_name, 
        request.ingredients
    )
    
    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)
    
    return result

@router.post("/ask-question")
async def answer_cooking_question(request: QuestionRequest):
    """Answer cooking questions"""
    result = await ai_service.answer_cooking_question(
        request.question,
        request.context
    )
    
    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)
    
    return result

@router.post("/text-to-speech")
async def convert_text_to_speech(text: str):
    """Convert text to speech"""
    audio_data = await speech_service.text_to_speech(text)
    
    if audio_data:
        return {"audio_data": "audio_data_available"}  # Simplified
    else:
        return {"message": "Use frontend TTS"}

@router.get("/recipes")
async def get_saved_recipes():
    """Get saved recipes"""
    return {"recipes": []}