import pytest
import sys
from src.error_handler import handle_error

def test_handle_error_exits_with_error_code(mocker):
    """Test that handle_error prints the error message and exits with code 2."""
    # Mock sys.exit to prevent actual exit
    mock_exit = mocker.patch("sys.exit")
    
    # Mock sys.stderr to capture error message output
    mock_stderr = mocker.patch("sys.stderr", mocker.Mock())

    error_message = "Test error occurred"
    handle_error(Exception(error_message))

    # Verify sys.exit was called with exit code 2
    mock_exit.assert_called_once_with(2)

    # Verify error message was written to stderr
    mock_stderr.write.assert_any_call(f"ERROR: {error_message}\n")
