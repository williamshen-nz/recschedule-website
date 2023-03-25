import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}


def get_latest_recschedule_url(
    openrec_url: str = "https://www.mitrecsports.com/work-out/open-recreation/",
) -> str:
    """
    Determine the URL for the latest recschedule by scraping the MIT Open Rec page
    and finding the anchor href that matches the Open Rec text.
    """
    # Need to inject some headers to make the request look like a browser otherwise get a 403
    response = requests.get(openrec_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get anchors and filter for .pdf files
    anchors = set(a for a in soup.find_all("a", href=True) if a["href"].endswith(".pdf"))
    anchors = list(anchors)
    match = ["view open rec schedule" in a.text.lower() for a in anchors]
    if sum(match) == 0:
        raise ValueError(f"No recschedule PDF found at {openrec_url}")
    elif sum(match) > 1:
        raise ValueError(f"Multiple recschedule PDFs found at {openrec_url}")

    idx = match.index(True)
    return anchors[idx]["href"]


if __name__ == "__main__":
    print(get_latest_recschedule_url())
