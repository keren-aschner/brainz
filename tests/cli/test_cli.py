import pytest
from click.testing import CliRunner

from brainz.cli.__main__ import cli

HOST = "1.2.3.4"
PORT = 5678
ADDRESS = f"{HOST}:{PORT}"
DEFAULT_ADDRESS = "127.0.0.1:5000"
OUTPUT = {"a": "b"}

METHODS = [
    pytest.param("users", ["get-users"], id="get_users"),
    pytest.param("users/17", ["get-user", "17"], id="get_user"),
    pytest.param("users/17/snapshots", ["get-snapshots", "17"], id="get_snapshots"),
    pytest.param("users/17/snapshots/8", ["get-snapshot", "17", "8"], id="get_snapshot"),
    pytest.param("users/17/snapshots/8/pose", ["get-result", "17", "8", "pose"], id="get_result"),
]


@pytest.mark.parametrize("path,args", METHODS)
def test_cli(requests_mock, path, args):
    requests_mock.get(f"http://{DEFAULT_ADDRESS}/{path}", json=OUTPUT)
    runner = CliRunner()
    result = runner.invoke(cli, args)
    assert result.output == str(OUTPUT) + "\n"


@pytest.mark.parametrize("path,args", METHODS)
def test_cli_with_address(requests_mock, path, args):
    args.extend(["-h", HOST, "-p", PORT])
    requests_mock.get(f"http://{ADDRESS}/{path}", json=OUTPUT)
    runner = CliRunner()
    result = runner.invoke(cli, args)
    assert result.output == str(OUTPUT) + "\n"


def test_save_result(requests_mock):
    content = "content"
    filename = "filename"
    requests_mock.get(f"http://{DEFAULT_ADDRESS}/users/17/snapshots/8/color_image/data", text=content)
    runner = CliRunner()
    with runner.isolated_filesystem():
        open(filename, "a").close()
        runner.invoke(cli, ["get-result", "17", "8", "color_image", "--save", filename])
        with open(filename, "r") as f:
            assert f.read() == content
