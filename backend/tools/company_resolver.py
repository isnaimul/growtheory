import json
import re

def resolve_company(company_input: str) -> dict:
    """
    Resolve a company name/ticker input to official company information.
    
    This tool identifies the actual company from user input (which may contain typos,
    abbreviations, or informal names) and returns structured company data.
    
    Args:
        company_input: The company name or ticker as provided by the user
        
    Returns:
        dict with keys:
        - status: "found" or "not_found"
        - official_name: Official company name (e.g., "Microsoft Corporation")
        - ticker: Stock ticker symbol (e.g., "MSFT") or "PRIVATE" for private companies
        - confidence: "high" or "low" based on match quality
    
    Examples:
        resolve_company("Gogle") -> 
            {"status": "found", "official_name": "Alphabet Inc.", "ticker": "GOOGL", "confidence": "high"}
        
        resolve_company("Boston Consulting") -> 
            {"status": "found", "official_name": "Boston Consulting Group", "ticker": "PRIVATE", "confidence": "high"}
        
        resolve_company("asdfasdf") -> 
            {"status": "not_found", "official_name": null, "ticker": null, "confidence": null}
    """
    
    from strands.models.bedrock import BedrockModel
    from strands import Agent
    
    # Resolution prompt
    resolution_prompt = f"""You are a company identifier. Identify the actual company from this input: "{company_input}"

Return ONLY a valid JSON object with this exact structure (no other text, no markdown):
{{
  "status": "found" or "not_found",
  "official_name": "Official Company Name",
  "ticker": "TICKER" or "PRIVATE" or null,
  "confidence": "high" or "low"
}}

Rules:
- For publicly traded US companies, provide the stock ticker symbol in UPPERCASE
- For private companies or non-profits, set ticker to "PRIVATE"
- If you cannot identify the company with reasonable confidence, set status to "not_found"
- Be generous with typos and abbreviations - if 70%+ confident, mark as "found"
- Use official SEC/legal company names when possible

Examples:
- "Gogle" or "Google" → {{"status": "found", "official_name": "Alphabet Inc.", "ticker": "GOOGL", "confidence": "high"}}
- "Msft" or "Microsoft" → {{"status": "found", "official_name": "Microsoft Corporation", "ticker": "MSFT", "confidence": "high"}}
- "Boston Consulting" → {{"status": "found", "official_name": "Boston Consulting Group", "ticker": "PRIVATE", "confidence": "high"}}
- "BCG" → {{"status": "found", "official_name": "Boston Consulting Group", "ticker": "PRIVATE", "confidence": "high"}}
- "xyzabc123" → {{"status": "not_found", "official_name": null, "ticker": null, "confidence": null}}

Return ONLY the JSON object, nothing else."""

    try:
        # Create a simple resolver agent (no tools needed)
        model = BedrockModel(model_id="arn:aws:bedrock:us-east-1:975050287073:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0", region_name="us-east-1")
        resolver = Agent(model=model, system_prompt="You are a precise company identifier. Return only valid JSON.", tools=[])
        
        # Call the resolver
        result = resolver(resolution_prompt)
        response_text = result.content if hasattr(result, "content") else str(result)
        
        # Extract JSON from response
        json_match = re.search(r'\{[^{}]*"status"[^{}]*\}', response_text, re.DOTALL)
        if json_match:
            resolution_data = json.loads(json_match.group(0))
        else:
            # Try parsing entire response
            resolution_data = json.loads(response_text)
        
        # Validate the structure
        required_keys = ["status", "official_name", "ticker", "confidence"]
        if not all(key in resolution_data for key in required_keys):
            raise ValueError("Missing required keys in resolution response")
        
        return resolution_data
        
    except Exception as e:
        print(f"Error in resolve_company tool: {e}")
        # Return a safe default
        return {
            "status": "not_found",
            "official_name": None,
            "ticker": None,
            "confidence": None,
            "error": str(e)
        }