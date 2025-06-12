import os
from typing import Any, Dict, List

import aiohttp

from app.config.constants import PROFILE_DOMAINS


async def run_web_search(search_queries: List[str]) -> Dict[str, Any]:
    api_key = os.getenv("TAVILY_API_KEY")
    all_results = []

    async with aiohttp.ClientSession() as session:
        for query in search_queries:
            payload = {
                "api_key": api_key,
                "query": query,
                "search_depth": "basic",
                "max_results": 3,
                "include_domains": PROFILE_DOMAINS
            }

            async with session.post(
                "https://api.tavily.com/search",
                headers={"Content-Type": "application/json"},
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    for result in data.get("results", []):
                        all_results.append({
                            "url": result.get("url"),
                            "title": result.get("title"),
                            "content": result.get("content")
                        })

    return {"results": all_results}
