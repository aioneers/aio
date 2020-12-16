import aio
import os


def test_is_running_on_databricks():
    res = aio.is_running_on_databricks()
    assert res == False


def test_is_running_on_devops_pipeline():
    res = aio.is_running_on_devops_pipeline()
    print(res)