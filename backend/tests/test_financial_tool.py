import sys
import os

# Add the repo root to Python path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, repo_root)

from backend.tools.financial_analyzer import analyze_company_finances

# Test with Microsoft
print("=== Testing Microsoft ===")
result = analyze_company_finances("MSFT")

import json
print(json.dumps(result, indent=2))

print("\n=== Testing a smaller company ===")
result2 = analyze_company_finances("SNAP")  # Snapchat
print(json.dumps(result2, indent=2))