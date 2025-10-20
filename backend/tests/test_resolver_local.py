#!/usr/bin/env python3
"""
Local test script for the resolve_company tool integration - INTERACTIVE MODE
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.company_analyst import company_agent

def test_company_analysis(company_input):
    """Test the full analysis with resolver tool"""
    print(f"\n{'='*80}")
    print(f"Testing: {company_input}")
    print(f"{'='*80}\n")
    
    try:
        # Call the agent
        result = company_agent(f"Analyze {company_input} for job seekers")
        
        # Extract response
        response_text = result.content if hasattr(result, "content") else str(result)
        
        print("AGENT RESPONSE:")
        print("-" * 80)
        print(response_text)
        print("-" * 80)
        
        return response_text
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Interactive testing mode"""
    
    print("\n" + "="*80)
    print("COMPANY RESOLVER + ANALYST INTEGRATION TEST - INTERACTIVE MODE")
    print("="*80)
    print("\nType company names to test (or 'quit' to exit)")
    print("Try these examples: Gogle, Microsoft, Boston Consulting, asdfasdf, BCG, Stripe\n")
    
    while True:
        # Get user input
        user_input = input("\nEnter company name to analyze (or 'quit'): ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Exiting test suite")
            break
        
        if not user_input:
            print("⚠️  Please enter a company name")
            continue
        
        # Run the test
        response = test_company_analysis(user_input)
        
        if response:
            # Quick validation
            if "Analyzing" in response:
                print("\n✅ SUCCESS: Found 'Analyzing' header with company name")
            else:
                print("\n⚠️  WARNING: No 'Analyzing' header found")
    
    print("\n" + "="*80)
    print("TEST SESSION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()