import sys
from src.cli import parse_arguments, load_thresholds
from src.sap_connector import SAPConnector
from src.bapi_queries import fetch_ccms_alerts_with_metrics, fetch_disk_space_metrics
from src.result_processor import process_multiple_mtus_with_performance, process_disk_space_results
from src.error_handler import handle_error

def main():
    try:
        args = parse_arguments()
        thresholds, default_thresholds = load_thresholds()
        sap = SAPConnector(args)
        connection = sap.connect()

        mtu_results = fetch_ccms_alerts_with_metrics(connection, args.mtus)
        overall_status = "OK"
        outputs = []

        for result in mtu_results:
            if "DiskSpace" in result["path"]:
                disks = fetch_disk_space_metrics(connection, result["path"])
                status, output = process_disk_space_results(disks)
                outputs.append(output)
                if status == "CRITICAL":
                    overall_status = "CRITICAL"
                elif status == "WARNING" and overall_status != "CRITICAL":
                    overall_status = "WARNING"
            else:
                output = process_multiple_mtus_with_performance([result])
                outputs.append(output)
                if "CRITICAL" in output:
                    overall_status = "CRITICAL"
                elif "WARNING" in output and overall_status != "CRITICAL":
                    overall_status = "WARNING"

        print("\n".join(outputs))
        sys.exit(0 if overall_status == "OK" else 2 if overall_status == "CRITICAL" else 1)

    except Exception as e:
        handle_error(e)

if __name__ == "__main__":
    main()
