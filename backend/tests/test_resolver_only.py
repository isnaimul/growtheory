#!/usr/bin/env python3
"""
Test just the resolve_company tool in isolation
"""

import sys
import os

# Add the backend directory to path (go up one level from tests/)
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from tools.company_resolver import resolve_company

def test_resolver(company_input):
    """Test resolver with a single input"""
    print(f"\nTesting: '{company_input}'")
    result = resolve_company(company_input)
    print(f"Result: {result}")
    return result

def main():
    test_cases = [
        "Gogle",
        "Microsoft",
        "Boston Consulting",
        "asdfasdf",
        "AAPL",
        "BCG"
    ]
    
    print("="*60)
    print("RESOLVER TOOL STANDALONE TEST")
    print("="*60)
    
    for test in test_cases:
        test_resolver(test)
    
    print("\n" + "="*60)
    print("DONE")
    print("="*60)

if __name__ == "__main__":
    main()