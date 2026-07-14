import os
import time
import urllib.request
import re

transcripts = [
    # PLTR
    {"ticker": "PLTR", "quarter": "Q3", "year": "2023", "url": "https://www.fool.com/earnings/call-transcripts/2023/11/02/palantir-technologies-pltr-q3-2023-earnings-call-t/"},
    {"ticker": "PLTR", "quarter": "Q4", "year": "2023", "url": "https://www.fool.com/earnings/call-transcripts/2024/02/05/palantir-technologies-pltr-q4-2023-earnings-call-t/"},
    {"ticker": "PLTR", "quarter": "Q1", "year": "2024", "url": "https://www.fool.com/earnings/call-transcripts/2024/05/06/palantir-technologies-pltr-q1-2024-earnings-call-t/"},
    {"ticker": "PLTR", "quarter": "Q2", "year": "2024", "url": "https://www.fool.com/earnings/call-transcripts/2024/08/05/palantir-technologies-pltr-q2-2024-earnings-call-t/"},
    {"ticker": "PLTR", "quarter": "Q3", "year": "2024", "url": "https://www.fool.com/earnings/call-transcripts/2024/11/04/palantir-technologies-pltr-q3-2024-earnings-call-t/"},
    {"ticker": "PLTR", "quarter": "Q4", "year": "2024", "url": "https://www.fool.com/earnings/call-transcripts/2025/02/04/palantir-technologies-pltr-q4-2024-earnings-call-t/"},
    {"ticker": "PLTR", "quarter": "Q1", "year": "2025", "url": "https://www.gurufocus.com/news/2831008/q1-2025-palantir-technologies-inc-earnings-call-transcript"},
    {"ticker": "PLTR", "quarter": "Q2", "year": "2025", "url": "https://www.fool.com/earnings/call-transcripts/2026/02/03/palantir-pltr-q2-2025-earnings-call-transcript/"},
    {"ticker": "PLTR", "quarter": "Q3", "year": "2025", "url": "https://www.fool.com/earnings/call-transcripts/2025/11/04/palantir-pltr-q3-2025-earnings-call-transcript/"},
    {"ticker": "PLTR", "quarter": "Q4", "year": "2025", "url": "https://www.fool.com/earnings/call-transcripts/2026/02/02/palantir-pltr-q4-2025-earnings-call-transcript/"},
    {"ticker": "PLTR", "quarter": "Q1", "year": "2026", "url": "https://www.fool.com/earnings/call-transcripts/2026/05/04/palantir-pltr-q1-2026-earnings-transcript/"},
    
    # RKLB
    {"ticker": "RKLB", "quarter": "Q3", "year": "2023", "url": "https://www.gurufocus.com/stock/RKLB/transcripts/2217066"},
    {"ticker": "RKLB", "quarter": "Q4", "year": "2023", "url": "https://www.gurufocus.com/stock/RKLB/transcripts/2359071"},
    {"ticker": "RKLB", "quarter": "Q1", "year": "2024", "url": "https://www.gurufocus.com/stock/RKLB/transcripts/2429318"},
    {"ticker": "RKLB", "quarter": "Q2", "year": "2024", "url": "https://www.gurufocus.com/stock/RKLB/transcripts/2548514"},
    {"ticker": "RKLB", "quarter": "Q3", "year": "2024", "url": "https://www.gurufocus.com/stock/RKLB/transcripts/2599164"},
    {"ticker": "RKLB", "quarter": "Q4", "year": "2024", "url": "https://www.gurufocus.com/stock/RKLB/transcripts/2721156"},
    {"ticker": "RKLB", "quarter": "Q1", "year": "2025", "url": "https://www.gurufocus.com/stock/RKLB/transcripts/2847701"},
    {"ticker": "RKLB", "quarter": "Q2", "year": "2025", "url": "https://www.fool.com/earnings/call-transcripts/2025/08/08/rocket-lab-rklb-q2-2025-earnings-call-transcript/"},
    {"ticker": "RKLB", "quarter": "Q3", "year": "2025", "url": "https://www.insidermonkey.com/blog/rocket-lab-usa-inc-nasdaqrklb-q3-2025-earnings-call-transcript-1644097/"},
    {"ticker": "RKLB", "quarter": "Q4", "year": "2025", "url": "https://www.fool.com/earnings/call-transcripts/2026/02/26/rocket-lab-rklb-q4-2025-earnings-call-transcript/"},
    {"ticker": "RKLB", "quarter": "Q1", "year": "2026", "url": "https://www.fool.com/earnings/call-transcripts/2026/05/08/rocket-lab-rklb-q1-2026-earnings-transcript/"}
]

def fetch_jina(url):
    jina_url = "https://r.jina.ai/" + url
    req = urllib.request.Request(jina_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

base_dir = "/home/amao/文档/投资/research"

for t in transcripts:
    ticker = t["ticker"]
    quarter = t["quarter"]
    year = t["year"]
    url = t["url"]
    
    file_name = f"{year}-{quarter.replace('Q', '0')}-01_{ticker}-earnings-call.md" # matching repo style a bit better, e.g. 2026-07-12_buyside-memo.md
    target_dir = os.path.join(base_dir, ticker, "data")
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, file_name)
    
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
        print(f"Skipping {file_name}, already exists.")
        continue
        
    print(f"Downloading {file_name} from {url}...")
    content = fetch_jina(url)
    
    if not content:
        print(f"Failed to download {file_name}")
        continue
        
    content = re.sub(r'The Motley Fool has positions in.*', '', content, flags=re.IGNORECASE)
    content = re.sub(r'Motley Fool.*recommends.*', '', content, flags=re.IGNORECASE)
    
    frontmatter = f"---\nticker: {ticker}\nquarter: {quarter}\nyear: {year}\nsource: {url}\ndownloaded: 2026-07-14\n---\n\n"
    final_content = frontmatter + content
    
    with open(target_path, "w") as f:
        f.write(final_content)
        
    print(f"Saved {file_name}")
    time.sleep(3)
