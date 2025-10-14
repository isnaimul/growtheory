import wikipediaapi
import json
from datetime import datetime
import re
from typing import List, Dict

class WikipediaNewsScraper:
    def __init__(self):
        # Initialize Wikipedia API with user agent
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent='CompanyNewsScraper/1.0 (your-email@example.com)'
        )
        
    def search_company_page(self, company_name: str) -> Dict:
        """
        Fetch Wikipedia page for a company
        """
        page = self.wiki.page(company_name)
        
        if not page.exists():
            return {
                "error": f"No Wikipedia page found for '{company_name}'",
                "company": company_name,
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "company": company_name,
            "url": page.fullurl,
            "title": page.title,
            "summary": page.summary,
            "full_text": page.text,
            "sections": self.extract_sections(page),
            "timestamp": datetime.now().isoformat()
        }
    
    def extract_sections(self, page) -> Dict:
        """
        Extract relevant sections about company changes
        """
        relevant_keywords = [
            'history', 'acquisitions', 'mergers', 'layoffs', 
            'restructuring', 'leadership', 'management', 'personnel',
            'recent', 'controversy', 'criticism', 'news'
        ]
        
        sections_data = {}
        
        def process_section(section, level=0):
            section_title_lower = section.title.lower()
            
            # Check if section is relevant
            is_relevant = any(keyword in section_title_lower for keyword in relevant_keywords)
            
            if is_relevant and section.text:
                sections_data[section.title] = {
                    "level": level,
                    "text": section.text[:2000],  # Limit text length
                    "full_text": section.text
                }
            
            # Process subsections recursively
            for subsection in section.sections:
                process_section(subsection, level + 1)
        
        # Process all sections
        for section in page.sections:
            process_section(section)
        
        return sections_data
    
    def extract_company_insights(self, company_data: Dict) -> Dict:
        """
        Extract specific insights about changes, layoffs, acquisitions, etc.
        """
        insights = {
            "company": company_data.get("company", "Unknown"),
            "acquisitions": [],
            "mergers": [],
            "layoffs": [],
            "leadership_changes": [],
            "controversies": [],
            "recent_news": [],
            "industry_sector": self.extract_industry(company_data.get("summary", ""))
        }
        
        full_text = company_data.get("full_text", "")
        sections = company_data.get("sections", {})
        
        # Search for acquisitions
        acquisition_patterns = [
            r'acquired (.*?) (?:for|in) (.*?)(?:\.|,)',
            r'acquisition of (.*?)(?:\.|,)',
            r'purchased (.*?) (?:for|in) (.*?)(?:\.|,)'
        ]
        
        for pattern in acquisition_patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            insights["acquisitions"].extend([match if isinstance(match, str) else ' '.join(match) for match in matches[:5]])
        
        # Search for mergers
        merger_patterns = [
            r'merged with (.*?)(?:\.|,)',
            r'merger (?:with|between) (.*?)(?:\.|,)'
        ]
        
        for pattern in merger_patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            insights["mergers"].extend(matches[:5])
        
        # Search for layoffs
        layoff_patterns = [
            r'laid off (.*?)(?:\.|,)',
            r'layoffs? of (.*?)(?:\.|,)',
            r'(?:cut|reduced|eliminated) (.*?) (?:jobs|positions|employees)'
        ]
        
        for pattern in layoff_patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            insights["layoffs"].extend(matches[:5])
        
        # Extract leadership changes from sections
        for section_name, section_data in sections.items():
            if any(keyword in section_name.lower() for keyword in ['leadership', 'management', 'ceo', 'executive']):
                insights["leadership_changes"].append({
                    "section": section_name,
                    "text": section_data.get("text", "")
                })
        
        return insights
    
    def extract_industry(self, summary: str) -> str:
        """
        Try to identify the company's industry from the summary
        """
        industry_keywords = {
            "Technology": ["technology", "software", "tech", "computing", "IT"],
            "Finance": ["bank", "financial", "finance", "investment"],
            "Retail": ["retail", "store", "shopping", "e-commerce"],
            "Healthcare": ["healthcare", "pharmaceutical", "medical", "health"],
            "Manufacturing": ["manufacturing", "production", "industrial"],
            "Energy": ["energy", "oil", "gas", "renewable"],
            "Telecommunications": ["telecommunications", "telecom", "communications"],
            "Automotive": ["automotive", "automobile", "vehicle", "car"]
        }
        
        summary_lower = summary.lower()
        for industry, keywords in industry_keywords.items():
            if any(keyword in summary_lower for keyword in keywords):
                return industry
        
        return "Unknown"
    
    def scrape_companies(self, company_list: List[str], output_file: str = "company_data.json"):
        """
        Scrape multiple companies and save to JSON
        """
        results = []
        
        print(f"Starting scrape of {len(company_list)} companies...\n")
        
        for idx, company in enumerate(company_list, 1):
            print(f"[{idx}/{len(company_list)}] Scraping {company}...")
            
            company_data = self.search_company_page(company)
            
            if "error" not in company_data:
                insights = self.extract_company_insights(company_data)
                company_data["insights"] = insights
                print(f"  ✓ Successfully scraped {company}")
            else:
                print(f"  ✗ {company_data['error']}")
            
            results.append(company_data)
            print()
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Data saved to {output_file}")
        print(f"✓ Scraped {len([r for r in results if 'error' not in r])} companies successfully")
        
        return results


# Example usage
if __name__ == "__main__":
    scraper = WikipediaNewsScraper()
    
    # List of companies to scrape
    companies = [
        "Microsoft",
        "Amazon (company)",
        "Google",
        "Tesla, Inc.",
        "Meta Platforms"
    ]
    
    # Scrape and save to JSON
    scraper.scrape_companies(companies, "company_news_data.json")