# Author: Maryam

import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from pathlib import Path
from functools import reduce


def _write(data, file_name, file_location=None, write_directory=None, to='both', verbose=False):
    """
    Save dataframe to the directory as parquet, csv or both

    Parameters
    ----------
    data: DataFrame
        The DataFrame to be written.
    file_name: str
        The name of a data file
    file_location: str
        The path of a data file location (folder)
    write_directory: str
        The desired path to save the new file
    to: {'csv', 'parquet', 'both'}, optional
        The format to save the data. Default is 'both'.
    verbose: bool, default False
        Print out when writing the file

    Raises
    -------
    Error when the file name does not contain csv or xls.
    """
    if to == 'csv' or to == 'both':
        # save as csv
        csv_file_name = 'py_' + Path(file_name).stem + '.csv'
        if (file_location is None) and (write_directory is None):
            data.to_csv(csv_file_name, index=False)
        elif write_directory is None:
            data.to_csv(join(file_location, csv_file_name), index=False)
        else:
            data.to_csv(join(write_directory, csv_file_name), index=False)
        if verbose:
            print("{} is saved to the directory".format(csv_file_name))
    if to == 'parquet' or to == 'both':
        parquet_file_name = 'py_' + Path(file_name).stem + '.parquet'
        if (file_location is None) and (write_directory is None):
            data.to_csv(parquet_file_name, index=False)
        elif write_directory is None:
            data.to_csv(join(file_location, parquet_file_name), index=False)
        else:
            data.to_csv(join(write_directory, parquet_file_name), index=False)
        data.to_parquet(join(file_location, parquet_file_name), index=False)
        if verbose:
            print("{} is saved to the directory".format(parquet_file_name))


def read_and_write(file_name, file_location=None, write_directory=None, to='both', verbose=False):
    """
    Read CSV or Excel files by removing bad lines and save them
    as parquet, csv or both

    Parameters
    ----------
    file_name: str
        The name of a data file
    file_location: str
        The path of a data file location (folder)
    write_directory: str
        The desired path to save the new file
    to: {'csv', 'parquet', 'both'}, optional
        The format to save the data. Default is 'both'.
    verbose: bool, default False
        Print out when writing the file

    Raises
    -------
    Error when the file name does not contain csv or xls.
    """

    # Create file path
    if file_location is not None:
        f_path = join(file_location, file_name)
    else:
        f_path = file_name

    # try to read the file
    try:
        if 'csv' in file_name:
            df = pd.read_csv(f_path, error_bad_lines=False, engine="python", dtype=str)
            # Save to directory
            _write(df,
                   file_name,
                   file_location=file_location,
                   write_directory=write_directory,
                   to=to,
                   verbose=verbose)
        elif "xls" in file_name.lower():
            df = pd.read_excel(f_path, dtype=str)
            # Save to directory
            _write(df,
                   file_name,
                   file_location=file_location,
                   write_directory=write_directory,
                   to=to,
                   verbose=verbose)
    except Exception as e:
        print("Could not read {}, because {}".format(file_name, e))


def _check_file(file_name):
    """
    Check if the file name is csv or xls or it has not
    been created already.
    Parameters
    ----------
    file_name: str
        The name of a data file

    Returns
    -------
    bool:
        True if the file is csv or xls and has not been already created.
    """
    # check if the file has been created or not
    if ('py_' in file_name) or ('ipynb' in file_name):
        file = False
    elif ('csv' in file_name) or ("xls" in file_name.lower()):
        file = True
    # if it is not csv or xls
    else:
        file = False
    return file


def read_and_write_all(folder_path, to='both', write_directory=None, verbose=False):
    """
        Read CSV or Excel files in the folder by removing bad lines
        and save them as parquet, csv or both

        Parameters
        ----------
        folder_path: str
            The path of a data file location (folder)
        to: {'csv', 'parquet', 'both'}, optional
            The format to save the data. Default is 'both'.
        write_directory: str
            The desired path to save the new file
        verbose: bool, default False
            Print out when reading and writing the file

        Raises
        -------
        Error when the file name does not contain csv or xls.
    """
    for i, f in enumerate(listdir(folder_path)):
        f_path = join(folder_path, f)
        if isfile(f_path) and _check_file(f):
            if verbose:
                print("{}: Reading {} ...".format(i, f))
            read_and_write(f, folder_path, to=to, verbose=verbose)