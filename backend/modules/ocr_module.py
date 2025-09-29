import io, json
from fastapi import APIRouter, Body, File, UploadFile, HTTPException
from PIL import Image
import easyocr
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.chains import LLMChain
from .models import TextInput
from utils import safe_parse_llm_output
from main import llm

router = APIRouter()

# Initialize EasyOCR reader (English, GPU if available)
reader = easyocr.Reader(['en'], gpu=True)  # set gpu=False if no GPU

# Schema + Parser
response_schemas = [
    ResponseSchema(name="raw_text", description="Extracted text from input"),
    ResponseSchema(name="confidence", description="Confidence score (0.0-1.0)")
]
parser = StructuredOutputParser.from_response_schemas(response_schemas)

# Prompt + Chain
prompt = PromptTemplate(
    template="""
You are an OCR/Text extraction assistant.

Your job:
1. Extract the text from the input.
2. Correct common human mistakes/typos to proper words (e.g., "nxt" → "next", "dentst" → "dentist", "3 pm" → "3pm","@"->"at").
3. Keep meaning intact, do not hallucinate new words.
4. Return strictly valid JSON with:
   - raw_text: corrected text as a string
   - confidence: float 0–1 representing confidence

Input: {input_text}

Return JSON:
{format_instructions}
""",
    input_variables=["input_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
chain = LLMChain(llm=llm, prompt=prompt)

# ----------------- Helper -----------------
def extract_text_from_image_file(file: UploadFile):
    try:
        # Read image bytes
        image_bytes = file.file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')

        # OCR using EasyOCR
        ocr_results = reader.readtext(image_bytes)
        raw_text = " ".join([text[1] for text in ocr_results]).strip()

        if not raw_text:
            raw_text = "No clear text found in image."

        # Feed raw text to LLM for structured extraction
        output_text = chain.run({"input_text": raw_text})
        result = safe_parse_llm_output(parser, output_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"LLM OCR failed: {e}")

# ----------------- Endpoints -----------------
@router.post("/extract-text")
def extract_text(data: TextInput = Body(...)):
    output_text = chain.run({"input_text": data.input_text})
    return safe_parse_llm_output(parser, output_text)

@router.post("/extract-text-from-image")
async def extract_text_from_image_endpoint(file: UploadFile = File(...)):
    """
    Accepts an image file and returns structured OCR text with confidence.
    """
    result = extract_text_from_image_file(file)
    return result
