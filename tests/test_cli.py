import pytest
from src.cli import parse_arguments, load_predefined_mtus

@pytest.fixture
def mock_args(mocker):
    """Fixture to mock sys.argv."""
    def _mock_args(args_list):
        mocker.patch("sys.argv", ["cli.py"] + args_list)
    return _mock_args

def test_parse_arguments_with_predefined_mtus(mock_args):
    """Test parsing arguments with predefined MTUs."""
    mock_args(["--ashost", "sap.example.com", "--sysnr", "00", "--client", "100",
               "--user", "user", "--passwd", "pass", "--use-predefined", "CPU Usage", "Disk Space"])

    args = parse_arguments()
    assert args.ashost == "sap.example.com"
    assert args.sysnr == "00"
    assert args.client == "100"
    assert args.user == "user"
    assert args.passwd == "pass"
    assert "CPU Usage" in args.use_predefined
    assert "Disk Space" in args.use_predefined

def test_parse_arguments_with_custom_mtus(mock_args):
    """Test parsing arguments with custom MTU paths."""
    mock_args(["--ashost", "sap.example.com", "--sysnr", "00", "--client", "100",
               "--user", "user", "--passwd", "pass", "--mtus", "MTU1", "MTU2"])

    args = parse_arguments()
    assert args.mtus == ["MTU1", "MTU2"]

def test_load_predefined_mtus(mocker):
    """Test loading predefined MTUs from the configuration file."""
    mocker.patch("builtins.open", mocker.mock_open(read_data='{"common_mtus": {"Test MTU": "Path/To/MTU"}}'))
    
    mtus = load_predefined_mtus("dummy/path.json")
    assert "Test MTU" in mtus
    assert mtus["Test MTU"] == "Path/To/MTU"
