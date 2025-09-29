import json
from fastapi import APIRouter, Body
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.chains import LLMChain
from .models import FinalInput, PrepareFinalInput
from utils import safe_parse_llm_output
from main import llm

router = APIRouter()

response_schemas = [
    ResponseSchema(name="appointment", description="Final appointment JSON"),
    ResponseSchema(name="status", description="Status of appointment")
]
parser = StructuredOutputParser.from_response_schemas(response_schemas)

prompt = PromptTemplate(
    template="""
You are a final appointment agent.

Input JSON from normalization step:
{input_json}

Combine information strictly into JSON:
- appointment: must be a proper JSON object (not a string) with fields:
    - department
    - date
    - time
    - tz
- status: "ok"

Example output:
{{
  "appointment": {{
    "department": "dentist",
    "date": "2025-09-29",
    "time": "21:00",
    "tz": "Asia/Kolkata"
  }},
  "status": "ok"
}}

Return strictly as JSON (do NOT put the appointment inside quotes).

{format_instructions}
""",
    input_variables=["input_json"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = LLMChain(llm=llm, prompt=prompt)

@router.post("/prepare-final-input")
def prepare_final_input(data: PrepareFinalInput = Body(...)):
    return {"normalized": data.normalized_output, "entities": data.entities_output}

@router.post("/final-appointment")
def final_appointment(data: FinalInput = Body(...)):
    input_dict = data.normalized.copy()
    if data.entities and "entities" in data.entities:
        dept = data.entities.get("entities", {}).get("department")
        if dept:
            input_dict["department"] = dept
    output_text = chain.run({"input_json": json.dumps(input_dict)})
    return safe_parse_llm_output(parser, output_text)
