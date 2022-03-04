import os

import pytest


def _determine_recschedule_txt_fname() -> str:
    return os.path.join(os.path.dirname(__file__), "recschedule-test.txt")


@pytest.fixture(scope="session", autouse=True)
def recschedule_txt() -> str:
    with open(_determine_recschedule_txt_fname(), "r") as f:
        return f.read()
