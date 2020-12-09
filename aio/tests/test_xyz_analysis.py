import numpy as np
import pandas as pd
import aio


def test_xyz_analysis():
    quantities = {}
    np.random.seed(seed=42)
    df = pd.DataFrame()
    # create random time-series with aio.create_time_series function
    for i in range(100):
        quantities = aio.create_time_series(
            distribution="normal",
            p_mean=1000,
            p_std=300,
            num_periods=12,
            periodicity="M",
            start_date="2020-01-01",
            actual_material_number=str("{:04d}".format(np.random.randint(1000)))
            + str("-")
            + str("{:02d}".format(np.random.randint(20)))
            + str("-")
            + str("{:05d}".format(np.random.randint(5))),
            standard_price=1,
            intermittency=0.2,
        )
        df = df.append(quantities)

    # post process sample data
    df = df.reset_index()
    df = df.drop(columns=["Value", "index"])
    # shorten date format from YYYY-MM-DD to YYYY-MM
    df["Date"] = df["Date"].astype("str").str[:5] + df["Date"].astype("str").str[-2:]
    # split key return from function create_time_series into three columns
    df[["Material", "Country", "Region"]] = df["Material"].str.split("-", expand=True)
    # sort columns into more logical order
    df = df[["Material", "Country", "Region", "Date", "Quantity"]]
    # delete random periods as actual data a likely to be incomplete
    df = df.drop(np.random.choice(len(df), (int(len(df) / 2))))

    # run test with created sample data
    result = aio.xyz_analysis(
        df=df,
        primary_dimension_keys=["Material", "Country", "Region"],
        relevant_numeric_dimension="Quantity",
        relevant_date_dimension="Date",
        periods=12,
        start_date="2020-01-01",
        frequency="M",
    )

    assert len(result)


def test_xyz_analysis_key_without_demand():
    quantities = {}
    np.random.seed(seed=42)
    df = pd.DataFrame()
    # create random time series with aio.create_time_series function
    for i in range(1):
        quantities = aio.create_time_series(
            distribution="normal",
            p_mean=1000,
            p_std=300,
            num_periods=12,
            periodicity="M",
            start_date="2020-01-01",
            actual_material_number=str("{:04d}".format(np.random.randint(1000)))
            + str("-")
            + str("{:02d}".format(np.random.randint(20)))
            + str("-")
            + str("{:05d}".format(np.random.randint(5))),
            standard_price=1,
            intermittency=0.2,
        )
        df = df.append(quantities)

    # post process sample data
    df = df.reset_index()
    df = df.drop(columns=["Value", "index"])
    # shorten date format from YYYY-MM-DD to YYYY-MM
    df["Date"] = df["Date"].astype("str").str[:5] + df["Date"].astype("str").str[-2:]
    # split key return from function create_time_series into three columns
    df[["Material", "Country", "Region"]] = df["Material"].str.split("-", expand=True)
    # sort columns into more logical order
    df = df[["Material", "Country", "Region", "Date", "Quantity"]]
    # delete random periods as actual data a likely to be incomplete
    df = df.drop(np.random.choice(len(df), (int(len(df) / 2))))
    # set demand quantity to 0 for each period
    df["Quantity"] = 0

    # run test with created sample data
    result = aio.xyz_analysis(
        df=df,
        primary_dimension_keys=["Material", "Country", "Region"],
        relevant_numeric_dimension="Quantity",
        relevant_date_dimension="Date",
        periods=12,
        start_date="2020-01-01",
        frequency="M",
    )

    assert len(result[result["XYZ_Class"] == "N"]) == 1


def test_xyz_analysis_str_as_input_for_pri_dim():
    quantities = {}
    np.random.seed(seed=42)
    df = pd.DataFrame()
    # create random time series with aio.create_time_series function
    for i in range(10):
        quantities = aio.create_time_series(
            distribution="normal",
            p_mean=1000,
            p_std=300,
            num_periods=12,
            periodicity="M",
            start_date="2020-01-01",
            actual_material_number=str("{:04d}".format(np.random.randint(1000)))
            + str("-")
            + str("{:02d}".format(np.random.randint(20)))
            + str("-")
            + str("{:05d}".format(np.random.randint(5))),
            standard_price=1,
            intermittency=0.2,
        )
        df = df.append(quantities)

    # post process sample data
    df = df.reset_index()
    df = df.drop(columns=["Value", "index"])
    # shorten date format from YYYY-MM-DD to YYYY-MM
    df["Date"] = df["Date"].astype("str").str[:5] + df["Date"].astype("str").str[-2:]
    # split key return from function create_time_series into three columns
    df[["Material", "Country", "Region"]] = df["Material"].str.split("-", expand=True)
    # sort columns into more logical order
    df = df[["Material", "Country", "Region", "Date", "Quantity"]]
    # delete random periods as actual data a likely to be incomplete
    df = df.drop(np.random.choice(len(df), (int(len(df) / 2))))

    # run test with created sample data
    result = aio.xyz_analysis(
        df=df,
        primary_dimension_keys="Material",
        relevant_numeric_dimension="Quantity",
        relevant_date_dimension="Date",
        periods=12,
        start_date="2020-01-01",
        frequency="M",
    )

    assert len(result)


def test_xyz_analysis_short_list_as_input_for_pri_dim():
    quantities = {}
    np.random.seed(seed=42)
    df = pd.DataFrame()
    # create random time series with aio.create_time_series function
    for i in range(10):
        quantities = aio.create_time_series(
            distribution="normal",
            p_mean=1000,
            p_std=300,
            num_periods=12,
            periodicity="M",
            start_date="2020-01-01",
            actual_material_number=str("{:04d}".format(np.random.randint(1000)))
            + str("-")
            + str("{:02d}".format(np.random.randint(20)))
            + str("-")
            + str("{:05d}".format(np.random.randint(5))),
            standard_price=1,
            intermittency=0.2,
        )
        df = df.append(quantities)

    # post process sample data
    df = df.reset_index()
    df = df.drop(columns=["Value", "index"])
    # shorten date format from YYYY-MM-DD to YYYY-MM
    df["Date"] = df["Date"].astype("str").str[:5] + df["Date"].astype("str").str[-2:]
    # split key return from function create_time_series into three columns
    df[["Material", "Country", "Region"]] = df["Material"].str.split("-", expand=True)
    # sort columns into more logical order
    df = df[["Material", "Country", "Region", "Date", "Quantity"]]
    # delete random periods as actual data a likely to be incomplete
    df = df.drop(np.random.choice(len(df), (int(len(df) / 2))))

    # run test with created sample data
    result = aio.xyz_analysis(
        df=df,
        primary_dimension_keys=["Material"],
        relevant_numeric_dimension="Quantity",
        relevant_date_dimension="Date",
        periods=12,
        start_date="2020-01-01",
        frequency="M",
    )

    assert len(result)


def test_xyz_analysis_weekly():
    quantities = {}
    np.random.seed(seed=42)
    df = pd.DataFrame()
    # create random time series with aio.create_time_series function
    for i in range(10):
        quantities = aio.create_time_series(
            distribution="normal",
            p_mean=1000,
            p_std=300,
            num_periods=52,
            periodicity="W",
            start_date="2020-01-01",
            actual_material_number=str("{:04d}".format(np.random.randint(1000)))
            + str("-")
            + str("{:02d}".format(np.random.randint(20)))
            + str("-")
            + str("{:05d}".format(np.random.randint(5))),
            standard_price=1,
            intermittency=0.2,
        )
        df = df.append(quantities)

    # post process sample data
    df = df.reset_index()
    df = df.drop(columns=["Value", "index"])
    # shorten date format from YYYY-MM-DD to YYYY-MM
    df["Date"] = df["Date"].astype("str").str[:5] + df["Date"].astype("str").str[-2:]
    # split key return from function create_time_series into three columns
    df[["Material", "Country", "Region"]] = df["Material"].str.split("-", expand=True)
    # sort columns into more logical order
    df = df[["Material", "Country", "Region", "Date", "Quantity"]]
    # delete random periods as actual data a likely to be incomplete
    df = df.drop(np.random.choice(len(df), (int(len(df) / 2))))

    # run test with created sample data
    result = aio.xyz_analysis(
        df=df,
        primary_dimension_keys="Material",
        relevant_numeric_dimension="Quantity",
        relevant_date_dimension="Date",
        periods=52,
        start_date="2020-01",
        frequency="W",
    )

    assert len(result)
