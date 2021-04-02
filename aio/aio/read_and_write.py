# Author: Maryam

import pandas as pd
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import warnings


def _write(data,
           file_name,
           file_location=None,
           write_directory=None,
           to='both',
           verbose=False):
    """
    Save dataframe to the directory as parquet, csv or both

    Parameters
    ----------
    data: DataFrame
        The DataFrame to be written (saved).
    file_name: str
        The name of a data file (e.g: 'data.csv').
    file_location: str or path object
        The path of a data file location (folder)
    write_directory: str or path object
        The desired path to save the new file (folder)
    to: {'csv', 'parquet', 'both'}, optional
        The format to save the data. Default is 'both'.
    verbose: bool, default False
        Informs when writing the file is successful.

    Raises
    -------
    Error when the file name does not contain csv or xls.
    """
    if to == 'csv' or to == 'both':
        # save as csv
        csv_file_name = 'py_' + Path(str(file_name)).stem + '.csv'
        if (file_location is None) and (write_directory is None):
            data.to_csv(csv_file_name, index=False)
        elif write_directory is None:
            data.to_csv(join(file_location, csv_file_name), index=False)
        else:
            data.to_csv(join(write_directory, csv_file_name), index=False)
        if verbose:
            print("{} is saved to the directory".format(csv_file_name))
    if to == 'parquet' or to == 'both':
        parquet_file_name = 'py_' + Path(str(file_name)).stem + '.parquet'
        if (file_location is None) and (write_directory is None):
            data.to_parquet(parquet_file_name, index=False)
        elif write_directory is None:
            data.to_parquet(join(file_location, parquet_file_name), index=False)
        else:
            data.to_parquet(join(write_directory, parquet_file_name), index=False)
        if verbose:
            print("{} is saved to the directory".format(parquet_file_name))


def read_and_write(file_name,
                   file_location=None,
                   write_directory=None,
                   to='both',
                   sep=',',
                   verbose=False):
    """
    Read CSV or Excel files by removing bad lines and save them
    as parquet, csv or both

    Parameters
    ----------
    file_name: str
        The name of a data file (e.g: 'data.csv').
    file_location: str or path object
        The path of a data file location (folder)
    write_directory: str or path object
        The desired path to save the new file (folder)
    to: {'csv', 'parquet', 'both'}, optional
        The format to save the data. Default is 'both'.
    sep: str, default ‘,’
        Delimiter to use. 
    verbose: bool, default False
        Informs when writing the file is successful.

    Raises
    -------
    Error when the file name does not contain csv or xls.
    """

    if not _check_file(file_name):
        if verbose:
            warnings.warn("Warning.............{} is not valid or"
                          "it's been already created".format(file_name))
    else:
        # Create file path
        if file_location is not None:
            f_path = join(file_location, file_name)
        else:
            f_path = file_name #os.path.abspath(file_name)

    # try to read the file
    if 'csv' in str(file_name):
        df = pd.read_csv(f_path, sep=sep, error_bad_lines=False, engine="python", dtype=str)
        # Save to directory
        _write(df,
                file_name,
                file_location=file_location,
                write_directory=write_directory,
                to=to,
                verbose=verbose)
    elif "xls" in str(file_name).lower():
        df = pd.read_excel(f_path, dtype=str)
        # Save to directory
        _write(df,
                file_name,
                file_location=file_location,
                write_directory=write_directory,
                to=to,
                verbose=verbose)
    else:
        raise ValueError("Could not read {}, because {} is not .csv or excel file".format(file_name, file_name))


def _check_file(file_name):
    """
    Check if the file name is csv or xls or it has not
    been created already.
    Parameters
    ----------
    file_name: str
        The name of a data file (e.g: 'data.csv').

    Returns
    -------
    bool:
        True if the file is csv or xls and has not been already created.
    """
    # check if the file has been created or not
    if ('py_' in str(file_name)) or ('ipynb' in str(file_name)):
        file = False
    elif ('csv' in str(file_name)) or ("xls" in str(file_name).lower()):
        file = True
    # if it is not csv or xls
    else:
        file = False
    return file


def read_and_write_all(folder_path,
                       to='both',
                       write_directory=None,
                       verbose=False):
    """
    Read CSV or Excel files in the folder by removing bad lines
    and save them as parquet, csv or both

    Parameters
    ----------
    folder_path: str or path object
        The path of a data file location (folder).
    to: {'csv', 'parquet', 'both'}, optional
        The format to save the data. Default is 'both'.
    write_directory: str or path object
        The desired path to save the new file (folder).
    verbose: bool, default False
        Informs when writing the file is successful.

    Raises
    ----------
    Error when the file name does not contain csv or xls.
    """
    for i, f in enumerate(listdir(folder_path)):
        f_path = join(folder_path, f)
        if isfile(f_path) and _check_file(f):
            if verbose:
                print("{}: Reading {} ...".format(i, f))
            read_and_write(f,
                           folder_path,
                           write_directory,
                           to=to,
                           verbose=verbose)


def read_and_concat(list_of_files,
                    file_location=None,
                    write_directory=None,
                    parquet=True,
                    by_row=True,
                    save_by=None,
                    sep=','):
    """
    Read a list of parquet or csv file and concatenate them by row
    or by column. The file is written in the directory under the
    'save_by' name.

    Parameters
    ----------
    list_of_files: list of str
        list of dataframe names (e.g: ['data_0.csv', 'data_1.csv']).
    file_location: str or path object
        The path of a data file location (folder).
    write_directory: str or path object
        The desired path to save the new file (folder).
    parquet: bool, optional. Default True
        If file formats are parquet or csv (False)
    by_row: bool. Default True
        If concatenate by row or by column (False)
    save_by: str, optional. Default None
        If not None, the concatenate dataframe is written to the
        file_location under this name.
    sep: str, default ‘,’
        Delimiter to use. 

    Returns
    -------
    concat_output: DataFrame
        The concatenated dataframe
        optional: Save the concatenated dataframe to the given directory
    """
    if file_location is not None:
        list_of_files_path = [join(file_location, f) for f in list_of_files]
    else:
        list_of_files_path = [os.path.abspath(f) for f in list_of_files]
    lists_of_dfs = []
    if parquet:
        for file in list_of_files_path:
            lists_of_dfs.append(pd.read_parquet(file))
    else:
        for file in list_of_files_path:
            lists_of_dfs.append(pd.read_csv(file, sep=sep, dtype=str))
    if by_row:
        concat_output = pd.concat(lists_of_dfs, axis=0)
    else:
        concat_output = pd.concat(lists_of_dfs, axis=1)
    if save_by is not None:
        if parquet:
            to = 'parquet'
        else:
            to = 'csv'
        _write(concat_output,
               save_by,
               file_location,
               write_directory,
               to=to,
               verbose=False)
    return concat_output


def read_all_sheets(excel_file,
                    file_location=None,
                    write_directory=None,
                    by_row=True,
                    save_by=None,
                    to='both'):
    """
    Read an excel file with multiple sheets and concatenate the sheets

    Parameters
    ----------
    excel_file: str
        The name of a excel file with multiple sheets (e.g. 'data.xlsx')
    file_location: str or path object
        The path of a data file location (folder)
    write_directory: str or path object
        The desired path to save the new file (folder).
    by_row: bool. Default True
        If concatenate by row or by column (False)
    save_by: str, optional. Default None
        If not None, the concatenate dataframe is written to the
        file_location under this name.
    to: {'csv', 'parquet', 'both'}, optional
        The format to save the data. Default is 'both'.

    Returns
    -------
    concat_output: List of DataFrame
        List of dataframes, each sheet is a dataframe
        optional: Save the concatenated dataframe to the given directory
    """
    if file_location is not None:
        excel_file_path = join(file_location, excel_file)
    else:
        excel_file_path = os.path.abspath(excel_file)
    all_sheets = pd.read_excel(excel_file_path, None, dtype=str)
    list_of_dfs = list(all_sheets.values())
    if by_row:
        concat_output = pd.concat(list_of_dfs, axis=0)
    else:
        concat_output = pd.concat(list_of_dfs, axis=1)
    if save_by is not None:
        _write(concat_output,
               save_by,
               file_location,
               write_directory,
               to=to,
               verbose=False)
    return list_of_dfs
