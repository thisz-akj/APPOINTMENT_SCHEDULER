import json

def safe_parse_llm_output(parser, output_text):
    """
    Parse LLM output safely and fallback to raw JSON cleaning if needed.
    """
    try:
        return parser.parse(output_text)
    except Exception:
        cleaned = output_text.strip().replace("```json", "").replace("```", "").strip()
        try:
            return json.loads(cleaned)
        except:
            return {"status": "parse_failed", "raw_output": output_text}
