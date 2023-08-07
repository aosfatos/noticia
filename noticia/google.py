import requests
from loguru import logger

ENDPOINT = (
    "https://content-factchecktools.googleapis.com/v1alpha1/claims:search?key={api_key}&"
    "maxAgeDays={max_days}&reviewPublisherSiteFilter={publisher}"
)


def get_claims(api_key, max_days, publisher, page_token):
    url = ENDPOINT.format(api_key=api_key, max_days=max_days, publisher=publisher)
    if page_token is not None:
        url += f"&pageToken={page_token}"

    logger.info(f"Getting claim review data {url}...")
    resp = requests.get(url)
    resp.raise_for_status()
    json_resp = resp.json()
    return json_resp["claims"], json_resp.get("nextPageToken")


def search(api_key, max_days, publisher):
    "Get last published claims from a publsiher"
    all_claims = []
    claims, page_token = get_claims(api_key, max_days, publisher, page_token=None)
    all_claims.extend(claims)
    while page_token is not None:
        claims, page_token = get_claims(api_key, max_days, publisher, page_token=page_token)
        all_claims.extend(claims)

    return all_claims
