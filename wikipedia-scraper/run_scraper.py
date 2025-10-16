from wiki_scraper import WikipediaNewsScraper
import sys

def load_companies_from_file(filename: str) -> list:
    """Load company names from a text file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            companies = [line.strip() for line in f if line.strip()]
        return companies
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return []

def main():
    print("=" * 60)
    print("Wikipedia Company News Scraper")
    print("=" * 60)
    print()
    
    # Initialize scraper
    scraper = WikipediaNewsScraper()
    
    # Load companies from file
    companies = load_companies_from_file("companies.txt")
    
    if not companies:
        print("No companies found in companies.txt")
        print("Please add company names to companies.txt (one per line)")
        sys.exit(1)
    
    print(f"Found {len(companies)} companies to scrape:")
    for company in companies:
        print(f"  • {company}")
    print()
    
    # Ask for confirmation
    response = input("Start scraping? (y/n): ").lower()
    if response != 'y':
        print("Scraping cancelled.")
        sys.exit(0)
    
    print("\nStarting scrape...\n")
    
    # Scrape companies
    results = scraper.scrape_companies(companies, "company_news_data.json")
    
    print("\n" + "=" * 60)
    print("Scraping Complete!")
    print("=" * 60)
    print(f"\nData saved to: company_news_data.json")
    print(f"\nYou can now use this JSON file with Amazon Bedrock")

if __name__ == "__main__":
    main()