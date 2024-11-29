import pytest
from src.result_processor import process_multiple_mtus_with_performance, process_disk_space_results

def test_process_multiple_mtus_with_performance():
    """Test processing multiple MTUs with performance data."""
    results = [
        {
            "path": "SID/hostname/Dialog/ResponseTimeDialog",
            "alerts": [
                {
                    "SEVERITY": "CRITICAL",
                    "TEXT": "Response time exceeded",
                    "VALUE": 95,
                    "WARNING_THRESHOLD": 80,
                    "CRITICAL_THRESHOLD": 90
                }
            ]
        },
        {
            "path": "SID/hostname/System/CPUUsage",
            "alerts": []
        }
    ]

    output = process_multiple_mtus_with_performance(results)

    assert "CRITICAL - MTU 'SID/hostname/Dialog/ResponseTimeDialog' - Alert: Response time exceeded" in output
    assert "alerts=95;80;90;0;100" in output
    assert "OK - No alerts for MTU 'SID/hostname/System/CPUUsage'" in output

def test_process_disk_space_results():
    """Test processing disk space results with multiple disks."""
    disks = [
        {"DISK_NAME": "C:", "FREE_SPACE": 25, "WARNING_THRESHOLD": 20, "CRITICAL_THRESHOLD": 10},
        {"DISK_NAME": "D:", "FREE_SPACE": 5, "WARNING_THRESHOLD": 20, "CRITICAL_THRESHOLD": 10},
        {"DISK_NAME": "E:", "FREE_SPACE": 15, "WARNING_THRESHOLD": 20, "CRITICAL_THRESHOLD": 10}
    ]

    status, output = process_disk_space_results(disks)

    assert status == "CRITICAL"
    assert "CRITICAL - Disk 'D:' - Free space: 5% (Warning: 20%, Critical: 10%)" in output
    assert "OK - Disk 'C:' - Free space: 25% (Warning: 20%, Critical: 10%)" in output
    assert "WARNING - Disk 'E:' - Free space: 15% (Warning: 20%, Critical: 10%)" in output
