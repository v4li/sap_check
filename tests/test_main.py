import pytest
from src.main import main

def test_apply_mtu_specific_thresholds(mocker):
    mocker.patch("sys.argv", ["main.py", "--ashost", "host", "--sysnr", "00", "--client", "100", "--user", "user", "--passwd", "pass", "--mtus", "MTU1"])
    mocker.patch("src.cli.load_thresholds", return_value=(
        {"MTU1": {"warning": 10, "critical": 20}},
        {"warning": 1, "critical": 5}
    ))
    mock_fetch = mocker.patch("src.bapi_queries.fetch_ccms_alerts_with_metrics", return_value=[
        {
            "path": "MTU1",
            "alerts": [{"SEVERITY": "CRITICAL", "TEXT": "High usage", "VALUE": 15}]
        }
    ])
    mock_process = mocker.patch("src.result_processor.process_multiple_mtus_with_performance")
    mock_exit = mocker.patch("sys.exit")
    main()
    mock_fetch.assert_called_once()
    mock_process.assert_called_once()
    processed_alert = mock_process.call_args[0][0][0]["alerts"][0]
    assert processed_alert["WARNING_THRESHOLD"] == 10
    assert processed_alert["CRITICAL_THRESHOLD"] == 20
    mock_exit.assert_called_once_with(2)
