"""
Pydantic schemas for API requests and responses
"""
from pydantic import BaseModel
from typing import List, Dict, Any

class ContentGenerationRequest(BaseModel):
    content_type: str
    dynamic_data: Dict[str, Any] = {}
    custom_ai_configs: Dict[str, Dict[str, Any]] = {}
    custom_prompts: Dict[str, str] = {}

class ContentGenerationResponse(BaseModel):
    content: str
    prompt_outputs: List[str]
    content_type: str
    metadata: Dict[str, Any]

class PromptData(BaseModel):
    step: int
    text: str
    ai_settings: Dict[str, Any]

class ContentConfigCreate(BaseModel):
    content_type: str
    description: str
    prompts: List[Dict[str, Any]]

class ContentConfigResponse(BaseModel):
    id: int
    name: str
    description: str
    prompts: List[Dict[str, Any]]
    created_at: str

class ContentTypeResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: str
