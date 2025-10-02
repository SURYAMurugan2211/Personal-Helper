import logging
import requests
import urllib.parse
from livekit.agents import function_tool, RunContext

API_KEY = "pub_7378013b94660c4bf4653fd6de805df908c0e"
BASE_URL = "https://newsdata.io/api/1/news"

@function_tool()
async def get_news(context: RunContext, query: str = "world", country: str = "", language: str = "en") -> str:
    """
    Get the latest detailed news.
    - query: topic (e.g., 'world', 'technology', 'sports', 'new york')
    - country: optional 2-letter country code (e.g., 'us', 'in')
    - language: default 'en' for English
    """

    try:
        encoded_query = urllib.parse.quote(query)

        params = {
            "apikey": API_KEY,
            "q": encoded_query,
            "language": language
        }

        if country:
            params["country"] = country

        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                # Take top 3 articles for detailed explanation
                articles = data["results"][:3]

                detailed_news = []
                for article in articles:
                    title = article.get("title", "No title")
                    description = article.get("description", "No description available")
                    link = article.get("link", "")
                    source = article.get("source_id", "Unknown source")
                    pub_date = article.get("pubDate", "Unknown date")

                    detailed_news.append(
                        f"📰 **{title}**\n"
                        f"📅 Published: {pub_date}\n"
                        f"🏢 Source: {source}\n"
                        f"📖 {description}\n"
                        f"🔗 Read more: {link}\n"
                    )

                return f"Here are the top detailed news results for '{query}':\n\n" + "\n".join(detailed_news)

            else:
                return f"No news found for '{query}'."

        elif response.status_code == 422:
            logging.warning(f"No valid results for query '{query}'.")
            return f"No valid news results found for '{query}'. Try another search term."

        else:
            logging.error(f"Failed to get news (status: {response.status_code})")
            return f"Could not retrieve news (status: {response.status_code})."

    except Exception as e:
        logging.error(f"Error retrieving news for '{query}': {e}")
        return f"An error occurred while retrieving news for '{query}'."
