import json
from fastapi import APIRouter, File, UploadFile, HTTPException
from .models import ExtractedText, EntitiesData, PrepareFinalInput, FinalInput
from .ocr_module import extract_text_from_image_file
from .entities_module import chain as entities_chain, parser as entities_parser
from .normalize_module import normalize_datetime
from .final_appointment_module import prepare_final_input, final_appointment
from utils import safe_parse_llm_output

router = APIRouter()

@router.post("/pipeline/image")
async def run_image_pipeline(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="Image file must be provided")

    # STEP 1: Text Extraction 
    try:
        extracted = extract_text_from_image_file(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step 1 (OCR) failed: {e}")

    # STEP 2: Entity Extraction 
    try:
        input_json = json.dumps({
            "raw_text": extracted.get("raw_text", ""),
            "confidence": extracted.get("confidence", 0.0)
        })
        entities_output = entities_chain.run({"input_json": input_json})
        entities_result = safe_parse_llm_output(entities_parser, entities_output)

        if "entities" in entities_result and isinstance(entities_result["entities"], str):
            try:
                entities_result["entities"] = json.loads(entities_result["entities"])
            except:
                entities_result["entities"] = {}
        if "entities_confidence" in entities_result:
            try:
                entities_result["entities_confidence"] = float(entities_result["entities_confidence"])
            except:
                entities_result["entities_confidence"] = 0.0
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step 2 (Entity Extraction) failed: {e}")

    # STEP 3: Normalize Date/Time -
    try:
        normalized_result = normalize_datetime(EntitiesData(
            entities=entities_result.get("entities", {}),
            entities_confidence=entities_result.get("entities_confidence", 0.0)
        ))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step 3 (Normalization) failed: {e}")

    # STEP 4: Preparing Final Input 
    try:
        combined_input = PrepareFinalInput(
            normalized_output=normalized_result.get("normalized", {}),
            entities_output=entities_result
        )
        prepared_input = prepare_final_input(combined_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step 4 (Prepare Final Input) failed: {e}")

    # STEP 5: Final Appointment 
    try:
        final_result = final_appointment(FinalInput(
            normalized=prepared_input["normalized"],
            entities=prepared_input["entities"]
        ))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step 5 (Final Appointment) failed: {e}")

    return final_result
