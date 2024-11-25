def fetch_ccms_alerts_with_metrics(connection, mtu_paths):
    results = []
    try:
        for path in mtu_paths:
            response = connection.call('BAPI_ALERT_GETLIST', MONITOR_NAME=path)
            alerts = response.get("ALERTS", [])
            enriched_alerts = [
                {
                    "SEVERITY": alert["SEVERITY"],
                    "TEXT": alert["TEXT"],
                    "VALUE": alert.get("VALUE", 0),
                    "WARNING_THRESHOLD": alert.get("WARNING_THRESHOLD", 1),
                    "CRITICAL_THRESHOLD": alert.get("CRITICAL_THRESHOLD", 5)
                }
                for alert in alerts
            ]
            results.append({
                "path": path,
                "alerts": enriched_alerts
            })
    except Exception as e:
        raise RuntimeError(f"Failed to fetch CCMS alerts for MTU path '{path}': {e}")
    return results

def fetch_disk_space_metrics(connection, mtu_path):
    try:
        response = connection.call('BAPI_DISK_SPACE_GETLIST', MONITOR_NAME=mtu_path)
        disks = response.get("DISKS", [])
        return [
            {
                "DISK_NAME": disk["DISK_NAME"],
                "FREE_SPACE": disk["FREE_SPACE"],
                "WARNING_THRESHOLD": disk.get("WARNING_THRESHOLD", 20),
                "CRITICAL_THRESHOLD": disk.get("CRITICAL_THRESHOLD", 10)
            }
            for disk in disks
        ]
    except Exception as e:
        raise RuntimeError(f"Failed to fetch disk space metrics for MTU path '{mtu_path}': {e}")
