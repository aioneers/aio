import pandas as pd
import numpy as np
from pathlib import Path
import aio

def test_read_and_write():
    data_path = (
        Path(__file__).parent.absolute()
        / "test_data"
    )
    file_name = data_path/"sample_materials_inv_and_demand.csv"
    aio.read_and_write(file_name, data_path, verbose=True)


def test_read_and_write_all():
    data_path = (
        Path(__file__).parent.absolute()
        / "test_data"
    )
    aio.read_and_write_all(data_path)


