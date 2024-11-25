def process_multiple_mtus_with_performance(results):
    output = []
    for result in results:
        path = result["path"]
        alerts = result["alerts"]

        if not alerts:
            output.append(f"OK - No alerts for MTU '{path}' | alerts=0;1;5;0;100")
        else:
            for alert in alerts:
                severity = alert["SEVERITY"]
                text = alert["TEXT"]
                value = alert.get("VALUE", 0)
                warning = alert["WARNING_THRESHOLD"]
                critical = alert["CRITICAL_THRESHOLD"]
                performance_data = f"alerts={value};{warning};{critical};0;100"
                output.append(f"{severity} - MTU '{path}' - Alert: {text} | {performance_data}")
    return "\n".join(output)

def process_disk_space_results(disks):
    output_lines = []
    overall_status = "OK"

    for disk in disks:
        disk_name = disk["DISK_NAME"]
        free_space = disk["FREE_SPACE"]
        warning = disk["WARNING_THRESHOLD"]
        critical = disk["CRITICAL_THRESHOLD"]

        if free_space < critical:
            status = "CRITICAL"
            overall_status = "CRITICAL"
        elif free_space < warning:
            status = "WARNING"
            if overall_status != "CRITICAL":
                overall_status = "WARNING"
        else:
            status = "OK"

        output_lines.append(f"{status} - Disk '{disk_name}' - Free space: {free_space}% (Warning: {warning}%, Critical: {critical}%)")

    return overall_status, "\n".join(output_lines)
