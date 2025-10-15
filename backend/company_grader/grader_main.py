import sys, json
from datetime import datetime
from pathlib import Path
from .grader_getter import analyze, resolve_company

def print_report(r: dict):
    g, s = r.get('grade', {}), r.get('grade', {}).get('scores', {})
    print(f"\n{'='*70}\n{r.get('company','Unknown')} ({r.get('ticker','N/A')})\n{'='*70}")
    print(f"\nOVERALL: {g.get('tier','N/A')}-Tier ({g.get('composite',0)}/5.0)")
    print("\nSCORES:")
    for k, v in s.items(): print(f"  {k.title():12}: {v}/5.0")
    print(f"\n{'='*70}\n{r.get('analysis','No analysis')}\n{'='*70}\n")

def save_report(r: dict, folder="reports"):
    Path(folder).mkdir(exist_ok=True)
    f = f"{folder}/{r['ticker']}_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(f, 'w', encoding='utf-8') as o: json.dump(r, o, indent=2, ensure_ascii=False)
    print(f"Saved: {f}")

def run(company: str):
    if not resolve_company(company): return print(f"ERROR: '{company}' not found")
    print(f"\nAnalyzing {company}...")
    res = analyze(company)
    print_report(res)
    save_report(res)

def main():
    if len(sys.argv) > 1: run(' '.join(sys.argv[1:]))
    else:
        print("\nCOMPANY GRADER - Interactive Mode ('quit' to exit)\n" + "="*70)
        while True:
            try:
                c = input("Company: ").strip()
                if c.lower() in {'quit', 'q', 'exit'}: break
                if c: run(c)
            except KeyboardInterrupt: break

if __name__ == "__main__":
    main()
