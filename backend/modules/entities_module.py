import json
from fastapi import APIRouter, Body
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.chains import LLMChain
from .models import ExtractedText
from utils import safe_parse_llm_output
from main import llm

router = APIRouter()

response_schemas = [
    ResponseSchema(name="entities", description="Dictionary with date_phrase, time_phrase, department"),
    ResponseSchema(name="entities_confidence", description="Confidence score 0-1")
]
parser = StructuredOutputParser.from_response_schemas(response_schemas)

prompt = PromptTemplate(
    template="""
You are a smart appointment assistant capable of understanding casual human language.
The input is text extracted from a user message, which can be informal, abbreviated, or slightly noisy.
Your job is to extract the appointment details as structured JSON.

Input JSON:
{input_json}

Instructions:
1. Extract the following strictly as JSON:
   - entities:
       - date_phrase: any phrase describing the day or date
       - time_phrase: any phrase describing the time
       - department: type of appointment (e.g., dentist, cardiologist)
2. Provide a confidence score (0-1) indicating how confident you are about the extraction.
3. If uncertain, still provide your best guess, but reduce the confidence.
4. Handle casual phrases like:
   - "next Fri at 3pm"
   - "can I see a dentist tomorrow afternoon?"
   - "book me a cardiologist for Monday morning"
5. Return strictly valid JSON. Do not include extra commentary.

{format_instructions}
""",
    input_variables=["input_json"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)
chain = LLMChain(llm=llm, prompt=prompt)

@router.post("/extract-entities")
def extract_entities(data: ExtractedText = Body(...)):
    input_json = json.dumps({"raw_text": data.raw_text, "confidence": data.confidence})
    output_text = chain.run({"input_json": input_json})
    result = safe_parse_llm_output(parser, output_text)

    if "entities" in result and isinstance(result["entities"], str):
        try:
            result["entities"] = json.loads(result["entities"])
        except:
            result["entities"] = {}
    if "entities_confidence" in result:
        try:
            result["entities_confidence"] = float(result["entities_confidence"])
        except:
            result["entities_confidence"] = 0.0
    return result
