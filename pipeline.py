import os
from config import API_TOKEN, QUALYS_API_URL, CROWDSTRIKE_API_URL, MONGODB_URI
from clients import QualysApiClient, CrowdstrikeApiClient
from normalization import normalize_hosts
from data_deduping import dedupe_hosts
from pymongo import MongoClient
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def run_pipeline():
    qualys_api_client = QualysApiClient(API_TOKEN, QUALYS_API_URL)
    crowdstrike_api_client = CrowdstrikeApiClient(API_TOKEN, CROWDSTRIKE_API_URL)

    qualys_hosts = qualys_api_client.fetch_hosts()
    crowdstrike_hosts = crowdstrike_api_client.fetch_hosts()

    normalized_hosts = normalize_hosts(qualys_hosts, 'QUALYS') + normalize_hosts(crowdstrike_hosts, 'CROWDSTRIKE')
    deduped_hosts = dedupe_hosts(normalized_hosts)

    client = MongoClient(MONGODB_URI)
    db = client["hosts"]
    collection = db["hosts"]
    # Insert the deduped hosts into the collection, but only if the modifiedOn timestamp is greater than that of the existing host
    for host in deduped_hosts:
        existing_host = collection.find_one({"id": host["id"]})
        if existing_host is None or host["modifiedOn"] > existing_host["modifiedOn"]:
            collection.insert_one(host)
        else:
            print("Skipping.....")

    # Query the collection to get the hosts
    hosts = list(collection.find())

    # Distribution of host by operating system
    os_distribution = {}
    for host in hosts:
        os_name = host["os"]
        if os_name not in os_distribution:
            os_distribution[os_name] = 0
        os_distribution[os_name] += 1
    plt.bar(os_distribution.keys(), os_distribution.values())
    plt.xlabel("Operating System")
    plt.ylabel("Count")
    plt.title("Distribution of Hosts by Operating System")
    plt.tight_layout()
    plt.savefig("os_distribution.png")

    # Old hosts (last seen more than 30 days ago) vs newly discovered hosts
    current_date = datetime.now()
    old_hosts = [host for host in hosts if (current_date - host["lastSeen"]).days > 30]
    new_hosts = [host for host in hosts if (current_date - host["lastSeen"]).days <= 30]
    plt.bar(["Old Hosts", "New Hosts"], [len(old_hosts), len(new_hosts)])
    plt.xlabel("Host Type")
    plt.ylabel("Count")
    plt.title("Old vs New Hosts")
    plt.tight_layout()
    plt.savefig("old_vs_new_hosts.png")

if __name__ == "__main__":
    run_pipeline()
