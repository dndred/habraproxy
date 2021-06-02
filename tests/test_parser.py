import os
from pathlib import Path

import pytest

from habraproxy.config import Config
from habraproxy.proxy import Habraparser


@pytest.fixture
def example_data():
    p = Path(__file__).parent
    origin = open(os.path.join(p, "test_origin.html"), "rb").read()
    result = open(os.path.join(p, "test_result.html"), "rb").read()
    return origin, result


def test_sample(example_data):
    config = Config.get_instance()
    config.host = "0.0.0.0"
    config.port = 8080
    origin, result = example_data
    r = Habraparser(origin).process().strip()
    assert r == result.decode("utf-8").strip()
