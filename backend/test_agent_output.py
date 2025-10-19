import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.company_analyst import company_agent
import json

def test_agent(company_name):
    """Test the agent and show structured output"""
    print(f"\n{'='*80}")
    print(f"Testing Agent Output for: {company_name}")
    print(f"{'='*80}\n")
    
    try:
        # Call the agent
        result = company_agent(f"Analyze {company_name} for job seekers")
        response_text = result.content if hasattr(result, "content") else str(result)
        
        print("RAW AGENT RESPONSE:")
        print("-" * 80)
        print(response_text)
        print("-" * 80)
        
        # Try to extract the JSON metadata
        import re
        json_match = re.search(r'```json\s*(\{[^`]+\})\s*```', response_text, re.DOTALL)
        
        if json_match:
            print("\n✅ EXTRACTED JSON METADATA:")
            metadata = json.loads(json_match.group(1))
            print(json.dumps(metadata, indent=2))
        else:
            print("\n⚠️ No JSON metadata found in response")
        
        # Check if financial data might be embedded in the text
        print("\n📊 CHECKING FOR FINANCIAL DATA IN RESPONSE:")
        financial_keywords = ['revenue', 'market cap', 'employees', 'profit margin']
        for keyword in financial_keywords:
            if keyword.lower() in response_text.lower():
                print(f"  ✓ Found mention of '{keyword}'")
            else:
                print(f"  ✗ No mention of '{keyword}'")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


def interactive_test():
    """Interactive testing mode"""
    print("\n" + "="*80)
    print("AGENT OUTPUT TESTING - Check Financial Data")
    print("="*80)
    
    while True:
        company = input("\nEnter company name (or 'quit'): ").strip()
        
        if company.lower() in ['quit', 'exit', 'q']:
            break
        
        if not company:
            continue
        
        test_agent(company)
        print("\n" + "="*80)


if __name__ == "__main__":
    # You can test specific company or run interactive mode
    
    # Option 1: Test a specific company
    # test_agent("Microsoft")
    
    # Option 2: Interactive mode
    interactive_test()