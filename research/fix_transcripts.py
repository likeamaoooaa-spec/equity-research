import os
import time
import subprocess

base_dir = "/home/amao/文档/投资/research"

to_fix = [
    {"ticker": "PLTR", "year": "2025", "quarter": "1", "filename": "2025-01-01_PLTR-earnings-call.md"},
    {"ticker": "RKLB", "year": "2023", "quarter": "3", "filename": "2023-03-01_RKLB-earnings-call.md"},
    {"ticker": "RKLB", "year": "2023", "quarter": "4", "filename": "2023-04-01_RKLB-earnings-call.md"},
    {"ticker": "RKLB", "year": "2024", "quarter": "1", "filename": "2024-01-01_RKLB-earnings-call.md"},
    {"ticker": "RKLB", "year": "2024", "quarter": "2", "filename": "2024-02-01_RKLB-earnings-call.md"},
    {"ticker": "RKLB", "year": "2024", "quarter": "3", "filename": "2024-03-01_RKLB-earnings-call.md"},
    {"ticker": "RKLB", "year": "2024", "quarter": "4", "filename": "2024-04-01_RKLB-earnings-call.md"},
    {"ticker": "RKLB", "year": "2025", "quarter": "1", "filename": "2025-01-01_RKLB-earnings-call.md"},
    {"ticker": "RKLB", "year": "2025", "quarter": "3", "filename": "2025-03-01_RKLB-earnings-call.md"},
]

for item in to_fix:
    ticker = item["ticker"]
    year = item["year"]
    q = item["quarter"]
    filename = item["filename"]
    
    url = f"https://roic.ai/quote/{ticker}/transcripts/{year}-year/{q}-quarter"
    jina_url = f"https://r.jina.ai/{url}"
    
    target_path = os.path.join(base_dir, ticker, "data", "transcripts", filename)
    print(f"Downloading {filename} from {url}...")
    
    try:
        result = subprocess.run(["curl", "-sL", jina_url], capture_output=True, text=True, check=True)
        content = result.stdout
        
        # Keep only the transcript text
        # usually after "Markdown Content:" and before "About ROIC.AI" or "Toggle navigation menu"
        lines = content.split('\n')
        clean_lines = []
        in_content = False
        for line in lines:
            if "Markdown Content:" in line:
                in_content = True
                continue
            if in_content:
                if "Toggle navigation menu" in line or "About ROIC.AI" in line or "[Roic AI](https://roic.ai/)" in line or "1.   [United States" in line:
                    continue
                clean_lines.append(line)
                
        # Join lines and remove leading trailing whitespace
        clean_content = '\n'.join(clean_lines).strip()
        
        if not clean_content:
            print(f"Failed to extract content for {filename}. Raw length: {len(content)}")
            clean_content = content # fallback
            
        frontmatter = f"""---
ticker: {ticker}
quarter: Q{q}
year: {year}
source: {url}
downloaded: 2026-07-14
---

"""
        with open(target_path, "w") as f:
            f.write(frontmatter + clean_content)
        print(f"Saved {filename}")
        
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        
    time.sleep(3)
