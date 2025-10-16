from analysis_agent import CompanyNewsAnalyzer
import json
from datetime import datetime

def run_batch_analysis():
    """Run a batch of predefined analyses and save results"""
    
    print("=" * 60)
    print("Running Batch Analysis")
    print("=" * 60)
    print()
    
    analyzer = CompanyNewsAnalyzer()
    
    if not analyzer.company_data:
        print("No data available. Run the scraper first.")
        return
    
    # Define analysis queries
    analyses = [
        "Summarize all layoffs across the companies in the dataset",
        "What are the major acquisitions that have occurred?",
        "Give me an industry overview of all companies",
        "Which companies have had leadership changes recently?",
        "Identify any patterns or trends across these companies"
    ]
    
    results = {
        "analysis_date": datetime.now().isoformat(),
        "companies_analyzed": len(analyzer.company_data),
        "analyses": []
    }
    
    for idx, query in enumerate(analyses, 1):
        print(f"\n[{idx}/{len(analyses)}] Analyzing: {query}")
        print("-" * 60)
        
        try:
            response = analyzer.analyze(query)
            
            results["analyses"].append({
                "query": query,
                "response": response,
                "status": "success"
            })
            
            print(f"✓ Complete\n")
            
        except Exception as e:
            print(f"✗ Error: {e}\n")
            results["analyses"].append({
                "query": query,
                "error": str(e),
                "status": "failed"
            })
    
    # Save results
    output_file = "batch_analysis_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print(f"✓ Batch analysis complete!")
    print(f"✓ Results saved to: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    run_batch_analysis()