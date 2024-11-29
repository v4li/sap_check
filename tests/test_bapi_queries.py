import pytest
from src.bapi_queries import fetch_ccms_alerts_with_metrics, fetch_disk_space_metrics

@pytest.fixture
def mock_connection(mocker):
    """Fixture that provides a mocked SAP connection."""
    return mocker.Mock()

def test_fetch_ccms_alerts_with_metrics(mock_connection):
    """Test fetching CCMS alerts from SAP using a mocked connection."""
    mock_connection.call.return_value = {
        "ALERTS": [
            {"SEVERITY": "CRITICAL", "TEXT": "High CPU Usage", "VALUE": 95}
        ]
    }

    mtu_paths = ["SID/hostname/Dialog/ResponseTimeDialog"]
    results = fetch_ccms_alerts_with_metrics(mock_connection, mtu_paths)

    assert len(results) == 1
    assert results[0]["path"] == "SID/hostname/Dialog/ResponseTimeDialog"
    assert len(results[0]["alerts"]) == 1
    alert = results[0]["alerts"][0]
    assert alert["SEVERITY"] == "CRITICAL"
    assert alert["TEXT"] == "High CPU Usage"
    assert alert["VALUE"] == 95

def test_fetch_disk_space_metrics(mock_connection):
    """Test fetching disk space metrics from SAP using a mocked connection."""
    mock_connection.call.return_value = {
        "DISKS": [
            {"DISK_NAME": "C:", "FREE_SPACE": 25, "WARNING_THRESHOLD": 20, "CRITICAL_THRESHOLD": 10},
            {"DISK_NAME": "D:", "FREE_SPACE": 5, "WARNING_THRESHOLD": 20, "CRITICAL_THRESHOLD": 10}
        ]
    }

    mtu_path = "SID/hostname/System/DiskSpace"
    disks = fetch_disk_space_metrics(mock_connection, mtu_path)

    assert len(disks) == 2
    assert disks[0]["DISK_NAME"] == "C:"
    assert disks[0]["FREE_SPACE"] == 25
    assert disks[0]["WARNING_THRESHOLD"] == 20
    assert disks[0]["CRITICAL_THRESHOLD"] == 10

    assert disks[1]["DISK_NAME"] == "D:"
    assert disks[1]["FREE_SPACE"] == 5
    assert disks[1]["WARNING_THRESHOLD"] == 20
    assert disks[1]["CRITICAL_THRESHOLD"] == 10
