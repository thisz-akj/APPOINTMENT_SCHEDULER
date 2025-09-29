from pydantic import BaseModel
from typing import Dict, Optional

# Input models
class TextInput(BaseModel):
    input_text: str

class ExtractedText(BaseModel):
    raw_text: str
    confidence: float

class EntitiesData(BaseModel):
    entities: dict
    entities_confidence: float

class NormalizedData(BaseModel):
    normalized: dict
    normalization_confidence: float
    raw_text: str = None

class PrepareFinalInput(BaseModel):
    normalized_output: dict
    entities_output: dict

class FinalInput(BaseModel):
    normalized: Dict
    entities: Optional[Dict] = None

class PipelineInput(BaseModel):
    input_text: str
