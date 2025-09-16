import json
import logging
from typing import List, Dict, Any, Optional
import requests
from config import settings

auth_key = settings.AUTH_KEY

class FetchBooks:
    BASE_REC = "http://data4library.kr/api/recommandList"
    BASE_USAGE = "https://data4library.kr/api/usageAnalysisList"

    def __init__(self, auth_key: str, logger: Optional[logging.Logger] = None):
        self.auth_key = auth_key
        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def get_json(self, url: str, fallback_data: Any = None) -> Any:
        try:
            resp = requests.get(url, timeout=8)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            self.logger.warning(f"JSON API failed: {url} -> {e}")
            return fallback_data

    def get_avid_reader_recommendations(self) -> List[Dict[str, Any]]:
        isbn_multi = "9788983922571;9788983921475;9788983921994"
        url = (
            f"{self.BASE_REC}"
            f"?authKey={self.auth_key}"
            f"&isbn13={isbn_multi}"
            f"&type=reader"
            f"&format=json"
        )
        res = self.get_json(url, fallback_data={}) or {}
        docs = (res.get("response") or {}).get("docs") or []
        parsed: List[Dict[str, Any]] = []
        for item in docs[:10]:
            book_data = item.get("book") or {}
            parsed.append({
                "title": book_data.get("bookname"),
                "isbn13": book_data.get("isbn13"),
                "author": book_data.get("authors"),
                "cover": book_data.get("bookImageURL"),
            })
        return parsed

    def get_description(self, isbn13: str) -> List[Dict[str, str]]:
        url = (
            f"{self.BASE_USAGE}"
            f"?authKey={self.auth_key}"
            f"&isbn13={isbn13}"
            f"&format=json"
            f"&loanInfoYN=N"
        )
        res = self.get_json(url, fallback_data={}) or {}
        data: Dict[str, Any] = (res.get("response") or {}).get("book") or {}
        book_desc = [{
            "title": data.get("bookname", "N/A"),
            "authors": data.get("authors", "N/A"),
            "isbn13": data.get("isbn13", "N/A"),
            "description": data.get("description", "N/A"),
            "cover": data.get("bookImageURL", "N/A"),
        }]
        return book_desc
