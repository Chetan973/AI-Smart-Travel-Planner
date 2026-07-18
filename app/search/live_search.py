# app/search/live_search.py
from __future__ import annotations
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import httpx
from app.config import settings

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class LiveSearchResult:
    title: str
    url: str
    snippet: str
    source: str
    query: str
    observed_at: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)

class LiveSearchService:
    google_endpoint = "https://www.googleapis.com/customsearch/v1"
    serper_endpoint = "https://google.serper.dev/search"

    def search(self, query: str, limit: int = 5) -> list[LiveSearchResult]:
        """Tries Google CSE first, falls back gracefully to Serper for absolute resilience."""
        if settings.google_search_api_key and settings.google_search_engine_id:
            try:
                results = self._search_google(query, limit)
                if results:
                    return results
                logger.info("Google CSE returned 0 results. Routing to Serper fallback engine.")
            except Exception as e:
                logger.warning("Primary Google Custom Search failed: %s. Trying Serper.", e)
        
        if settings.serper_api_key:
            return self._search_serper(query, limit)
            
        return []

    def _search_google(self, query: str, limit: int) -> list[LiveSearchResult]:
        with httpx.Client(timeout=10.0, follow_redirects=True) as client:
            resp = client.get(
                self.google_endpoint,
                params={
                    "key": settings.google_search_api_key,
                    "cx": settings.google_search_engine_id,
                    "q": query,
                    "num": min(limit, 10)
                }
            )
            if resp.status_code != 200:
                return []
            payload = resp.json()
            observed_at = datetime.now(timezone.utc).isoformat()
            return [
                LiveSearchResult(
                    title=item.get("title", "Live Flight Route"),
                    url=item.get("link", "https://api.aviationstack.com"),
                    snippet=item.get("snippet", ""),
                    source="google_cse",
                    query=query,
                    observed_at=observed_at
                )
                for item in payload.get("items", []) if item.get("link")
            ]

    def _search_serper(self, query: str, limit: int) -> list[LiveSearchResult]:
        with httpx.Client(timeout=10.0, follow_redirects=True) as client:
            resp = client.post(
                self.serper_endpoint,
                headers={"X-API-KEY": settings.serper_api_key or ""},
                json={"q": query, "num": min(limit, 10)}
            )
            if resp.status_code != 200:
                return []
            payload = resp.json()
            observed_at = datetime.now(timezone.utc).isoformat()
            return [
                LiveSearchResult(
                    title=item.get("title", "Live Route Option"),
                    url=item.get("link", "https://google.com"),
                    snippet=item.get("snippet", ""),
                    source="serper_fallback",
                    query=query,
                    observed_at=observed_at
                )
                for item in payload.get("organic", []) if item.get("link")
            ]