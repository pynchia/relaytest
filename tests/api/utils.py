import json
import pathlib


def load_mock_data(filename: str) -> dict:
    with open(pathlib.Path(__file__).parent.parent.joinpath("mock_data").joinpath(filename)) as f:
        contents = json.load(f)
    return contents
