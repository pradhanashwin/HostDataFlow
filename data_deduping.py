from typing import List
import logging
logger = logging.getLogger(__name__)

def dedupe_hosts(hosts: List[dict]) -> List[dict]:
    """Merges duplicate hosts based on their IP address.

    Args:
        hosts (List[dict]): A list of normalized hosts.

    Returns:
        List[dict]: A list of deduplicated hosts.
    """
    logger.info("Data deduping started")

    deduped_hosts = []
    ip_to_hosts = {}
    for host in hosts:
        ip_address = host["hostName"]
        if ip_address not in ip_to_hosts:
            ip_to_hosts[ip_address] = []
        ip_to_hosts[ip_address].append(host)
    for ip_address, hosts_at_ip in ip_to_hosts.items():
        if len(hosts_at_ip) > 1:
            # Merge hosts at this IP address
            merged_host = {}
            for host in hosts_at_ip:
                for key, value in host.items():
                    if key not in merged_host:
                        merged_host[key] = value
                    elif isinstance(value, list) and isinstance(merged_host[key], list):
                        merged_host[key] += value
                    elif isinstance(value, dict) and isinstance(merged_host[key], dict):
                        merged_host[key].update(value)
            deduped_hosts.append(merged_host)
        else:
            deduped_hosts.append(hosts_at_ip[0])
    logger.info("Data deduping completed")
    return deduped_hosts