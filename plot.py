from typing import List
import textwrap
import matplotlib.pyplot as plt
from datetime import datetime


def plot_graph(hosts: List) -> None:
    """_summary_

    Args:
        hosts (List): list of host collection from mongodb
    """
    # Distribution of host by operating system
    os_distribution = {}
    for host in hosts:
        os_name = textwrap.fill(host["os"], 20)
        if os_name not in os_distribution:
            os_distribution[os_name] = 0
        os_distribution[os_name] += 1

    plt.bar(os_distribution.keys(), os_distribution.values())
    plt.xlabel("Operating System")
    plt.ylabel("Count")
    plt.title("Distribution of Hosts by Operating System")
    plt.xticks(rotation=0, ha='right')  # Rotate and align the x-axis labels
    plt.subplots_adjust(bottom=0.3)  # Adjust the bottom margin
    plt.savefig("os_distribution.png")

    # Old hosts (last seen more than 30 days ago) vs newly discovered hosts
    current_date = datetime.now()
    labels = ["Old Hosts", "New Hosts"]
    old_hosts = [host for host in hosts if (current_date - host["lastSeen"]).days > 30]
    new_hosts = [host for host in hosts if (current_date - host["lastSeen"]).days <= 30]
    plt.clf()
    plt.bar(labels, [len(old_hosts), len(new_hosts)])
    plt.xlabel("Host Type")
    plt.ylabel("Count")
    plt.title("Old vs New Hosts")
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.3)  # Adjust the bottom margin
    plt.savefig("old_vs_new_hosts.png")
