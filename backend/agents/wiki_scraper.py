import json
import requests
from strands import Agent, tool

@tool
def get_wiki_text(company: str) -> str:
    """Fetch Wikipedia content for any company searched by user."""
    try:
        # Try multiple variations of the company name
        variations = [
            company.replace(' ', '_'),
            f"{company.replace(' ', '_')}_Corporation", 
            f"{company.replace(' ', '_')}_Inc.",
            f"{company.replace(' ', '_')}_Company",
            f"{company.replace(' ', '_')}_(company)"
        ]
        
        headers = {'User-Agent': 'GrowTheory/1.0'}
        
        for variation in variations:
            url = f"https://en.wikipedia.org/wiki/{variation}"
            print(f"Trying: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✓ Found Wikipedia page at: {variation}")
                return response.text[:3000]  # Return raw content for AI processing
        
        return f"No Wikipedia page found for {company}"
        
    except Exception as e:
        return f"Error fetching Wikipedia page: {str(e)}"

def get_company_info(company_name: str) -> dict:
    """Get info for ANY company the user searches."""
    
    if not company_name or not company_name.strip():
        return {"error": "Company name is required"}
    
    try:
        print(f"Creating agent for: {company_name}")
        
        # Create agent for this specific company search
        agent = Agent(
            model="arn:aws:bedrock:us-east-1:975050287073:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0",
            tools=[get_wiki_text],
            system_prompt="""You are a company data extractor. Extract information from Wikipedia content and return as JSON:

{
    "company_name": "Full official company name",
    "founded": year_as_integer_or_null,
    "headquarters": "City, State/Country or null",
    "ceo": "Current CEO name or null", 
    "employees": employee_count_as_integer_or_null,
    "industry": "Primary business type or null",
    "description": "Brief description or null"
}

Return ONLY valid JSON. Use null for missing data."""
        )
        
        print("Agent created successfully. Processing...")
        
        # Process the user's search
        result = agent(f"Extract company information for: {company_name}")
        response = str(result)
        
        print(f"Agent response: {response[:200]}...")
        
        # Parse JSON from response
        start = response.find('{')
        end = response.rfind('}') + 1
        
        if start != -1 and end > start:
            json_str = response[start:end]
            print(f"Extracted JSON: {json_str}")
            return json.loads(json_str)
        else:
            return {"error": f"Could not extract information for {company_name}"}
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return {"error": f"Analysis failed for {company_name}: {str(e)}"}

# Test function
def test_scraper():
    """Test the scraper with user input"""
    
    print("=== GrowTheory Wikipedia Scraper Test ===")
    
    while True:
        company = input("\nEnter company name to analyze (or 'quit' to exit): ").strip()
        
        if company.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
            
        if not company:
            print("Please enter a company name.")
            continue
        
        print(f"\n🔍 Analyzing: {company}")
        print("-" * 50)
        
        result = get_company_info(company)
        
        print("\n📊 Results:")
        print(json.dumps(result, indent=2))
        print("-" * 50)

if __name__ == "__main__":
    test_scraper()