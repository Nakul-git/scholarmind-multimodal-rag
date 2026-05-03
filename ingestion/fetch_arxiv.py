import os
import re
import arxiv
import requests
import certifi


RAW_DIR = "data/raw_papers"


def safe_filename(text: str) -> str:
    text = re.sub(r'[\\/*?:"<>|]', "_", text)
    return text[:80]


def download_pdf_with_requests(pdf_url: str, pdf_path: str):
    """
    Download PDF using requests + certifi to avoid Windows SSL certificate issues.
    """

    headers = {
        "User-Agent": "arxiv-rag-project/1.0"
    }

    response = requests.get(
        pdf_url,
        headers=headers,
        timeout=60,
        verify=certifi.where()
    )

    response.raise_for_status()

    with open(pdf_path, "wb") as f:
        f.write(response.content)


def fetch_arxiv_papers(query: str, max_results: int = 3):
    """
    Search arXiv and download PDFs safely.
    """

    os.makedirs(RAW_DIR, exist_ok=True)

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    downloaded_papers = []
    client = arxiv.Client()

    for result in client.results(search):
        paper_id = result.entry_id.split("/")[-1]
        safe_title = safe_filename(result.title)

        pdf_path = os.path.join(RAW_DIR, f"{paper_id}.pdf")

        print(f"📥 Downloading: {result.title}")

        pdf_url = result.pdf_url

        try:
            download_pdf_with_requests(pdf_url, pdf_path)

            downloaded_papers.append({
                "paper_id": paper_id,
                "title": result.title,
                "summary": result.summary,
                "authors": [author.name for author in result.authors],
                "published": str(result.published),
                "pdf_path": pdf_path,
                "safe_title": safe_title
            })

            print(f"✅ Saved PDF: {pdf_path}")

        except Exception as e:
            print(f"❌ Failed to download {result.title}")
            print(f"Reason: {e}")

    return downloaded_papers