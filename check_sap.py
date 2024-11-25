import sys
from src.cli import parse_arguments, load_thresholds
from src.sap_connector import SAPConnector
from src.bapi_queries import fetch_ccms_alerts_with_metrics, fetch_disk_space_metrics
from src.result_processor import process_multiple_mtus_with_performance, process_disk_space_results