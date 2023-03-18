import re

import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}


def get_latest_recschedule_url(
    recschedule_pattern: str = r".*\d{1,2}.\d{1,2}.\d{1,2}-\d{1,2}.\d{1,2}.\d{1,2}.pdf",
    openrec_url: str = "https://www.mitrecsports.com/work-out/open-recreation/",
) -> str:
    """
    Determine the URL for the latest recschedule by scraping the MIT Open Rec page
    and matching against a regex pattern.
    """
    # Need to inject some headers to make the request look like a browser otherwise get a 403
    response = requests.get(openrec_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Match pattern against hrefs and filter for .pdf files
    hrefs = set(a["href"] for a in soup.find_all("a", href=True))
    pdfs = set(href for href in hrefs if href.endswith(".pdf"))
    matched_pdfs = set(pdf for pdf in pdfs if re.match(recschedule_pattern, pdf))

    if len(matched_pdfs) == 0:
        raise ValueError(
            f"No recschedule PDF found with regex pattern '{recschedule_pattern}' at {openrec_url}"
        )
    elif len(matched_pdfs) > 1:
        raise ValueError(
            f"Multiple recschedule PDFs {matched_pdfs} found with regex pattern "
            f"'{recschedule_pattern}' at {openrec_url}"
        )
    else:
        return matched_pdfs.pop()


if __name__ == "__main__":
    print(get_latest_recschedule_url())
