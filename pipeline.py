import argparse
from config import API_TOKEN, QUALYS_API_URL, CROWDSTRIKE_API_URL, MONGODB_URI
from clients import QualysApiClient, CrowdstrikeApiClient
from normalization import normalize_hosts
from data_deduping import dedupe_hosts
from plot import plot_graph
from pymongo import MongoClient


def run_pipeline(skip: int = None, limit: int = None) -> None:
    """_summary_

    Args:
        skip (int, optional): _description_. Defaults to None.
        limit (int, optional): _description_. Defaults to None.
    """
    qualys_api_client = QualysApiClient(API_TOKEN, QUALYS_API_URL)
    crowdstrike_api_client = CrowdstrikeApiClient(API_TOKEN,
                                                  CROWDSTRIKE_API_URL)

    qualys_hosts = qualys_api_client.fetch_hosts(skip=skip, limit=limit)
    crowdstrike_hosts = crowdstrike_api_client.fetch_hosts(skip=skip,
                                                           limit=limit)

    normalized_hosts = normalize_hosts(qualys_hosts, 'QUALYS') \
        + normalize_hosts(crowdstrike_hosts, 'CROWDSTRIKE')
    deduped_hosts = dedupe_hosts(normalized_hosts)

    client = MongoClient(MONGODB_URI)
    db = client["hosts"]
    collection = db["hosts"]
    # Insert the deduped hosts into the collection, but only if the modifiedOn
    # timestamp is greater than that of the existing host
    for host in deduped_hosts:
        existing_host = collection.find_one({"id": host["id"]})
        if existing_host is None \
                or host["modifiedOn"] > existing_host["modifiedOn"]:
            collection.insert_one(host)
        else:
            print("Skipping.....")

    # Query the collection to get the hosts
    hosts = list(collection.find())
    plot_graph(hosts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of hosts fetched from each API")
    parser.add_argument("--skip", type=int, default=None, help="Offset the number of hosts fetched from each API")
    args = parser.parse_args()
    limit = args.limit if args.limit else 1
    skip = args.skip if args.skip else 0
    run_pipeline(skip=skip, limit=limit)
