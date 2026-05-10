import os
import re

from tavily import TavilyClient
from dotenv import load_dotenv


load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_claim_online(claim):

    try:

        response = client.search(
            query=claim,
            search_depth="advanced",
            max_results=3
        )

        results = []

        for item in response.get(
            "results",
            []
        ):

            results.append({
                "title": item.get("title"),
                "content": item.get("content"),
                "url": item.get("url")
            })

        return results

    except Exception as e:

        return [{
            "title": "Error",
            "content": str(e),
            "url": ""
        }]


def classify_claim(claim, results):

    claim_numbers = re.findall(
        r'\d+',
        claim
    )

    combined_content = " ".join(
        [
            result["content"]
            for result in results
        ]
    )

    matched = 0

    for number in claim_numbers:

        if number in combined_content:
            matched += 1

    if len(claim_numbers) == 0:

        return (
            "Needs Review",
            50
        )

    confidence = int(
        (matched / len(claim_numbers)) * 100
    )

    if matched == len(claim_numbers):

        return (
            "Verified",
            confidence
        )

    elif matched > 0:

        return (
            "Inaccurate",
            confidence
        )

    else:

        return (
            "False",
            confidence
        )