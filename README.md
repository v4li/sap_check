# sap_check
script for common monitoring engines that monitors SAP system status indicators

sap_monitoring_project/
├── config/
│   └── mtus.json                   # Configuration file for MTUs and thresholds
├── src/
│   ├── __init__.py                 # Marks this as a package
│   ├── cli.py                      # Command-line interface and configuration loading
│   ├── sap_connector.py            # SAP connection handler
│   ├── bapi_queries.py             # Queries to SAP BAPIs
│   ├── result_processor.py         # Formats results for monitoring systems
│   ├── error_handler.py            # Centralized error handling
│   └── check_sap.py                # Main entry point for the SAP monitoring program
├── tests/
│   ├── __init__.py                 # Marks this as a test package
│   ├── test_cli.py                 # Unit tests for `cli.py`
│   ├── test_check_sap.py           # Unit tests for `check_sap.py`
│   ├── test_bapi_queries.py        # Unit tests for `bapi_queries.py`
│   ├── test_result_processor.py    # Unit tests for `result_processor.py`
│   └── test_error_handler.py       # Unit tests for `error_handler.py`
├── requirements.txt                # Project dependencies
└── README.md                       # General project documentation
