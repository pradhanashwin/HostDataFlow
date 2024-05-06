from typing import List, Union, Dict
from datetime import datetime

def to_camel_case(snake_str: str) -> str:
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))

def snake_to_camel(snake_str: str) -> str:
    if "_" in snake_str:
        # Convert snake case to camel case
        camel_string = to_camel_case(snake_str)
        return camel_string[0].lower() + camel_string[1:]
    else:
        # If already in camel case, return as is
        return snake_str

def convert_keys_to_camel(d: Dict[str, Union[str, Dict]]) -> Dict[str, Union[str, Dict]]:
    """
    Recursively converts dictionary keys to camelCase.

    Args:
        d (Dict[str, Union[str, Dict]]): Input dictionary.

    Returns:
        Dict[str, Union[str, Dict]]: Dictionary with keys converted to camelCase.
    """
    new_d = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = convert_keys_to_camel(v)
        new_d[snake_to_camel(k)] = v
    return new_d

def parse_timestamp(timestamp: str) -> datetime:
    try:
        # Attempt to parse with milliseconds
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        # Fallback to parsing without milliseconds
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

def normalize_hosts(hosts: List[dict], source: str) -> List[dict]:
    
    """Normalizes a list of CrowdStrike hosts by converting keys to lowercase and
    removing unnecessary information.

    Args:
        hosts (List[dict]): A list of hosts.

    Returns:
        List[dict]: A list of normalized hosts.
    """
    normalized_hosts = []
    for host in hosts:
        normalized_host = {}
        for key, value in host.items():
            new_key = snake_to_camel(key)
            if source == 'CROWDSTRIKE':
                # Normalize fields
                if new_key == 'agentLocalTime' or new_key == 'firstSeen' or new_key == 'lastSeen':
                    date_value = parse_timestamp(value)
                    normalized_host[new_key] = date_value
                elif "bios" in new_key:
                    bios_dict = normalized_host.setdefault("bios", {})
                    bios_key = new_key.replace("bios", "")
                    bios_dict[bios_key] = value
                elif "agent" in new_key:
                    agent_dict = normalized_host.setdefault("Agent", {})
                    nested_key = new_key.replace("Agent", "")
                    agent_dict[nested_key] = value
                elif new_key == "platformId":
                    normalized_host.setdefault("Platform", {})['Id'] = value
                elif new_key == "platformName":
                    normalized_host.setdefault("Platform", {})['Name'] = value
                elif new_key == "osVersion":
                    normalized_host["os"] = value
                elif "hostname" == new_key:
                    normalized_host["hostName"] = value
                elif "localIp" == new_key:
                    normalized_host["ipAddress"] = value
                elif 'modifiedTimestamp' == new_key:
                    normalized_host["modifiedOn"] = parse_timestamp(value["$date"])
                else:
                    # For other fields, just copy as is
                    normalized_host[new_key] = value
            else:
                if 'biosDescription' in new_key:
                    bios = value.split(" ")
                    normalized_host["bios"] = {
                        "manufacturer": bios[0],
                        "version": bios[1],
                        "date": bios[2] if len(bios) > 2 else ''
                    }
                elif 'created' == new_key:
                    normalized_host["firstSeen"] = parse_timestamp(value)
                elif 'lastSystemBoot' == new_key:
                    normalized_host["lastSeen"] = parse_timestamp(value)
                elif 'modified' == new_key:
                    normalized_host["modifiedOn"] = parse_timestamp(value)
                elif 'os' == new_key:
                    normalized_host["os"] = value
                elif 'volume' in new_key:
                    volumes = value['list']
                    normalized_host["volumes"] = [{
                        "Name": volume['HostAssetVolume']['name'],
                        "Size": volume['HostAssetVolume']['size'],
                        "Free": volume['HostAssetVolume']['free']
                    } for volume in volumes]
                elif 'software' in new_key:
                    software = value['list']
                    normalized_host["software"] = [{
                        "name": item['HostAssetSoftware']['name'],
                        "version": item['HostAssetSoftware']['version']
                    } for item in software]
                elif "name" == new_key:
                    normalized_host["hostName"] = value
                elif "address" == new_key:
                    normalized_host["ipAddress"] = value
                else:
                    # For other fields, just copy as is
                    normalized_host[new_key] = value
        normalized_hosts.append(convert_keys_to_camel(normalized_host))
    return normalized_hosts
