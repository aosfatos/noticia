import requests

ENDPOINT = (
    "https://content-factchecktools.googleapis.com/v1alpha1/claims:search?key={api_key}&"
    "maxAgeDays={max_days}&reviewPublisherSiteFilter={publisher}"
)


def search(api_key, max_days, publisher):
    "Get last published claims from a publsiher"
    url = ENDPOINT.format(api_key=api_key, max_days=max_days, publisher=publisher)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json().get("claims", [])
