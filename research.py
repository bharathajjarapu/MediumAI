import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import PyPDF2
from io import BytesIO

def fetch_content(url: str, headers: dict) -> str:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        if response.encoding is None:
            response.encoding = 'utf-8'
        content = response.content.decode(response.encoding, errors='ignore')
        if url.endswith('.pdf'):
            return extract_pdf_text(response.content)
        else:
            return extract_html_text(content)
    except requests.HTTPError:
        return ""
    except Exception as e:
        return ""

def extract_html_text(content: str) -> str:
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text(separator='\n').strip()
    return ' '.join(text.split())

def extract_pdf_text(content: bytes) -> str:
    with BytesIO(content) as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = "".join(page.extract_text() for page in reader.pages)
        return text.strip()

def research_link(query: str) -> str:
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        ddgs = DDGS()
        query = f"{query} site:bbc.com OR site:cnn.com OR site:nytimes.com OR site:techcrunch.com OR site:theverge.com OR site:reuters.com OR site:wired.com OR site:forbes.com OR site:wsj.com OR site:washingtonpost.com"
        results = [fetch_content(result['href'], headers) for result in ddgs.text(query, max_results=5)]
        summaries = [result for result in results if result]
        summaries = ["\n".join(result.split("\n")[:3]) for result in summaries]
        return "\n\n".join(summaries)
    except Exception as e:
        return "Error during research."