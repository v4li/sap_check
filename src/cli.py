import argparse
import json

def load_predefined_mtus(config_path="config/mtus.json"):
    with open(config_path, "r") as file:
        config = json.load(file)
    return config.get("common_mtus", {})

def load_thresholds(config_path="config/mtus.json"):
    with open(config_path, "r") as file:
        config = json.load(file)
    return config.get("thresholds", {}), config.get("default_thresholds", {})

def parse_arguments():
    predefined_mtus = load_predefined_mtus()
    
    parser = argparse.ArgumentParser(description="SAP System Monitoring Tool with Predefined MTUs")
    parser.add_argument('--ashost', required=True, help='SAP Application Server Host')
    parser.add_argument('--sysnr', required=True, help='SAP System Number')
    parser.add_argument('--client', required=True, help='SAP Client')
    parser.add_argument('--user', required=True, help='SAP Username')
    parser.add_argument('--passwd', required=True, help='SAP Password')
    parser.add_argument('--mtus', nargs='+', required=False, help='List of MTUs or MTU paths to monitor (e.g., SID/hostname/Dialog/ResponseTimeDialog)')
    parser.add_argument('--use-predefined', nargs='+', help=f"List of predefined MTUs (available: {', '.join(predefined_mtus.keys())})")
    parser.add_argument('--warning', type=int, help='Warning threshold for alerts (default: 1)')
    parser.add_argument('--critical', type=int, help='Critical threshold for alerts (default: 5)')

    args = parser.parse_args()

    # Expand predefined MTUs
    if args.use_predefined:
        predefined_paths = [predefined_mtus[mtu] for mtu in args.use_predefined if mtu in predefined_mtus]
        if args.mtus:
            args.mtus.extend(predefined_paths)
        else:
            args.mtus = predefined_paths
    
    return args
