import pandas as pd
import numpy as np
import os
from pathlib import Path
import aio


def test_read_and_write():
    data_path = (
        Path(__file__).parent.absolute()
        / "test_data"
    )
    file_name = data_path/"sample_materials_inv_and_demand.csv"
    
    aio.read_and_write(file_name, data_path, verbose=True)
    
    parquet_file_name = (
        Path(__file__).parent.absolute()
        /"test_data"/"py_sample_materials_inv_and_demand.parquet"
    )
    csv_file_name = (
        Path(__file__).parent.absolute()
        /"test_data"/"py_sample_materials_inv_and_demand.csv"
    )
    os.remove(parquet_file_name)
    os.remove(csv_file_name)


def test_read_and_write_all():
    data_path = (
        Path(__file__).parent.absolute()
        / "test_data"
    )
    aio.read_and_write_all(data_path)

    parquet_file_name = (
        Path(__file__).parent.absolute()
        /"test_data"/"py_sample_materials_inv_and_demand.parquet"
    )
    csv_file_name = (
        Path(__file__).parent.absolute()
        /"test_data"/"py_sample_materials_inv_and_demand.csv"
    )
    os.remove(parquet_file_name)
    os.remove(csv_file_name)


def test_read_and_concat():
    df_1 = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=['A', 'B', 'C', 'D'])
    df_2 = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=['A', 'B', 'C', 'D'])
    data_path = Path(__file__).parent.absolute() / "test_data" / "read_and_concat"
    data_path.mkdir(exist_ok=True)
    file1 = data_path / "df_1.parquet"
    file2 = data_path / "df_2.parquet"
    df_1.to_parquet(file1)
    df_2.to_parquet(file2)

    aio.read_and_concat([file1, file2])
    os.remove(file1)
    os.remove(file2)
    os.rmdir(data_path)

def test_read_all_sheets():
    data_path = (
            Path(__file__).parent.absolute()
            / "test_data"
    )
    file_name = data_path / "multi_sheets.xlsx"
    aio.read_all_sheets(file_name, data_path)
    
    csv_sheet = (
            Path(__file__).parent.absolute()
            / "test_data/py_multi_sheets.csv"
    )
    
    parquet_sheets = (
            Path(__file__).parent.absolute()
            / "test_data/py_multi_sheets.parquet"
    )

    os.remove(csv_sheet)
    os.remove(parquet_sheets)
    