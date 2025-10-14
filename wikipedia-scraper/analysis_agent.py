import json
from strands import Agent, tool
from strands.models import BedrockModel
import os

# Define tool functions at module level (required for Strands)
company_data_store = []

def load_company_data(data_file: str = "company_news_data.json") -> list:
    """Load the scraped Wikipedia data"""
    global company_data_store
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            company_data_store = json.load(f)
            return company_data_store
    except FileNotFoundError:
        print(f"Error: {data_file} not found!")
        print("Please run the scraper first: python run_scraper.py")
        return []

@tool
def get_company_info(company_name: str) -> str:
    """
    Get all available information about a specific company.
    
    Args:
        company_name: Name of the company to look up
        
    Returns:
        JSON string with company information
    """
    for company in company_data_store:
        if company_name.lower() in company.get('company', '').lower():
            return json.dumps(company, indent=2)
    
    return f"No data found for company: {company_name}"

@tool
def analyze_layoffs(company_name: str = None) -> str:
    """
    Analyze layoff information for a specific company or all companies.
    
    Args:
        company_name: Optional - specific company name, or None for all companies
        
    Returns:
        Analysis of layoff data
    """
    results = []
    
    for company in company_data_store:
        if company_name and company_name.lower() not in company.get('company', '').lower():
            continue
        
        insights = company.get('insights', {})
        layoffs = insights.get('layoffs', [])
        
        if layoffs:
            results.append({
                'company': company.get('company'),
                'layoffs': layoffs,
                'industry': insights.get('industry_sector')
            })
    
    if not results:
        return "No layoff information found."
    
    return json.dumps(results, indent=2)

@tool
def analyze_acquisitions(company_name: str = None) -> str:
    """
    Analyze acquisition and merger information.
    
    Args:
        company_name: Optional - specific company name, or None for all companies
        
    Returns:
        Analysis of acquisitions and mergers
    """
    results = []
    
    for company in company_data_store:
        if company_name and company_name.lower() not in company.get('company', '').lower():
            continue
        
        insights = company.get('insights', {})
        acquisitions = insights.get('acquisitions', [])
        mergers = insights.get('mergers', [])
        
        if acquisitions or mergers:
            results.append({
                'company': company.get('company'),
                'acquisitions': acquisitions,
                'mergers': mergers,
                'industry': insights.get('industry_sector')
            })
    
    if not results:
        return "No acquisition or merger information found."
    
    return json.dumps(results, indent=2)

@tool
def analyze_leadership_changes(company_name: str = None) -> str:
    """
    Analyze leadership and management changes.
    
    Args:
        company_name: Optional - specific company name, or None for all companies
        
    Returns:
        Leadership change information
    """
    results = []
    
    for company in company_data_store:
        if company_name and company_name.lower() not in company.get('company', '').lower():
            continue
        
        insights = company.get('insights', {})
        leadership = insights.get('leadership_changes', [])
        
        if leadership:
            results.append({
                'company': company.get('company'),
                'leadership_changes': leadership,
                'industry': insights.get('industry_sector')
            })
    
    if not results:
        return "No leadership change information found."
    
    return json.dumps(results, indent=2)

@tool
def compare_companies(company1: str, company2: str) -> str:
    """
    Compare two companies across various metrics.
    
    Args:
        company1: First company name
        company2: Second company name
        
    Returns:
        Comparison analysis
    """
    comp1_data = None
    comp2_data = None
    
    for company in company_data_store:
        if company1.lower() in company.get('company', '').lower():
            comp1_data = company
        if company2.lower() in company.get('company', '').lower():
            comp2_data = company
    
    if not comp1_data or not comp2_data:
        return "One or both companies not found in data."
    
    comparison = {
        'company1': {
            'name': comp1_data.get('company'),
            'industry': comp1_data.get('insights', {}).get('industry_sector'),
            'acquisitions_count': len(comp1_data.get('insights', {}).get('acquisitions', [])),
            'layoffs_count': len(comp1_data.get('insights', {}).get('layoffs', [])),
            'summary': comp1_data.get('summary', '')[:200] + '...'
        },
        'company2': {
            'name': comp2_data.get('company'),
            'industry': comp2_data.get('insights', {}).get('industry_sector'),
            'acquisitions_count': len(comp2_data.get('insights', {}).get('acquisitions', [])),
            'layoffs_count': len(comp2_data.get('insights', {}).get('layoffs', [])),
            'summary': comp2_data.get('summary', '')[:200] + '...'
        }
    }
    
    return json.dumps(comparison, indent=2)

@tool
def get_industry_overview() -> str:
    """
    Get an overview of all companies grouped by industry.
    
    Returns:
        Industry overview with company counts
    """
    industries = {}
    
    for company in company_data_store:
        industry = company.get('insights', {}).get('industry_sector', 'Unknown')
        if industry not in industries:
            industries[industry] = []
        
        industries[industry].append({
            'company': company.get('company'),
            'has_layoffs': len(company.get('insights', {}).get('layoffs', [])) > 0,
            'has_acquisitions': len(company.get('insights', {}).get('acquisitions', [])) > 0
        })
    
    return json.dumps(industries, indent=2)


class CompanyNewsAnalyzer:
    def __init__(self, data_file: str = "company_news_data.json"):
        """Initialize the analyzer with Wikipedia scraped data"""
        self.data_file = data_file
        
        # Load data into global store
        load_company_data(data_file)
        
        if not company_data_store:
            print("Warning: No data loaded. Agent may not function properly.")
            return
        
        # Initialize Bedrock Claude model
        self.model = BedrockModel(
            model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
            region_name="us-east-1"  # Change to your region
        )
        
        # Create the Strands agent with tools
        self.agent = Agent(
            model=self.model,
            tools=[
                get_company_info,
                analyze_layoffs,
                analyze_acquisitions,
                analyze_leadership_changes,
                compare_companies,
                get_industry_overview
            ],
            system_prompt="""You are a business intelligence analyst specializing in corporate news analysis.

Your role is to:
1. Analyze company data from Wikipedia including acquisitions, mergers, layoffs, and leadership changes
2. Provide insights on industry trends and company performance
3. Compare companies and identify patterns
4. Give strategic recommendations based on the data

Always be specific, cite the information you're analyzing, and provide actionable insights.
When discussing layoffs or negative news, be factual and professional."""
        )
    
    def analyze(self, query: str) -> str:
        """
        Main method to analyze company data based on user query.
        
        Args:
            query: User's analysis question
            
        Returns:
            Agent's analysis response
        """
        if not company_data_store:
            return "No data available. Please run the scraper first."
        
        print(f"\n🤖 Agent analyzing: {query}\n")
        print("=" * 60)
        
        response = self.agent(query)
        
        return response.message


def main():
    """Interactive analysis session"""
    print("=" * 60)
    print("Company News Analysis Agent (Powered by Strands + Bedrock)")
    print("=" * 60)
    print()
    
    # Initialize analyzer
    analyzer = CompanyNewsAnalyzer()
    
    if not company_data_store:
        return
    
    print(f"✓ Loaded data for {len(company_data_store)} companies")
    print()
    print("Example queries you can ask:")
    print("  • 'What layoffs have occurred across all companies?'")
    print("  • 'Tell me about Microsoft's acquisitions'")
    print("  • 'Compare Tesla and Amazon'")
    print("  • 'What industries are represented in the data?'")
    print("  • 'Analyze leadership changes at Meta'")
    print()
    print("Type 'quit' or 'exit' to stop")
    print("=" * 60)
    print()
    
    while True:
        try:
            query = input("Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            if not query:
                continue
            
            # Get analysis from agent
            response = analyzer.analyze(query)
            
            print(f"\n📊 Analysis:\n{response}\n")
            print("-" * 60)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()