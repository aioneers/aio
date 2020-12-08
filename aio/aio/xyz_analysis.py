import numpy as np
import pandas as pd
import itertools


def xyz_analysis(
    df,
    primary_dimension_keys,
    relevant_numeric_dimension,
    relevant_date_dimension,
    start_date,
    periods,
    frequency,
    X=0.5,
    Y=1,
    L=0.4,
    M=0.7,
):
    """The XYZ Analysis provides a XYZ variability & frequency classification for a multi-dimensional,
    granular time series input dataset.

    Parameters
    ----------
    df : Pandas.DataFrame
        DataFrame holding the object to be classified, if applicable additional secondary_dimensions, and
        numeric values used for classification, e.g. df.columns = ["product", "country", "quantity"].

    primary_dimension_keys : string or list of strings
        Column name(s) in the input DataFrame holding the object(s) to be classified, e.g. a product number.
        The primary_dimension_keys can be provided on the level of granularity the classification should be 
        performed on, e.g. product, country, region or product, plant, storage location.

    relevant_numeric_dimension : string
        Column name in the input DataFrame holding numeric values to be used for classification, e.g. periods with
        demand for a product.
        
    relevant_date_dimension : string
        Column in the input DataFrame holding the dates to the relevant_numeric_dimension values.

    start_date : string
        Start date of the classification to be provided in format YYYY-MM or YYYY-MM-DD. Start_date should be
        provided together with periods and frequency to enable the function to complete the period range to be
        considered for classification, e.g. start_date = "01.01.2020", periods = 12, frequency = "M" resulting
        in a period range of 12 monthly buckets starting in January 2020 like 2020-01, 2020-02, ... ,2020-12. 

    periods : int
        Number of periods the classification is performed for.

    frequency : string
        Frequency of the periods the classification is performed for, e.g. "D" for days,
        "M" for months, "Q" for quarters, "Y" for years

    X, Y : float = 0.5, 1
        Threshold values to distinct the provided data into three variability classes X, Y & Z.
        e.g. X =< 0.5; 0.5 < Y =< 1; Z > 1

    L, M : float = 0.4, 0.7
        Threshold values to distinct the provided data into three frequency classes Low, Medium, High.
        e.g. Low =< 0.5; 0.5 < Medium =< 1; High > 1

    Returns
    -------
    df_return : Pandas.DataFrame
        Output DataFrame returned grouped by provided primary- & secondary dimensions with respective
        classification and cumulative values
        
    Examples
    --------
    >>> import aio
    >>> 
    >>> # create sample data 
    >>> quantities = {}
    >>> np.random.seed(seed=42)
    >>> df = pd.DataFrame()
    >>> # create random time series with aio.create_time_series function
    >>> for i in range(10):
    >>>     quantities = aio.create_time_series(
    >>>         distribution='normal',
    >>>         p_mean=1000,
    >>>         p_std=300,
    >>>         num_periods=12,
    >>>         periodicity='M',
    >>>         start_date='2020-01-01',
    >>>         actual_material_number=str('{:04d}'.format(np.random.randint(1000))) + str("-") + str('{:02d}'.format(np.random.randint(20))) + str("-") + str('{:05d}'.format(np.random.randint(5))),
    >>>         standard_price=1, intermittency=0.2
    >>>         )
    >>> df = df.append(quantities)
    >>> # post process sample data 
    >>> df = df.reset_index()
    >>> df = df.drop(columns=["Value", "index"])
    >>> # shorten date format from YYYY-MM-DD to YYYY-MM
    >>> df["Date"] = df["Date"].astype("str").str[:5] + df["Date"].astype("str").str[-2:]
    >>> # split key return from function create_time_series into three columns
    >>> df[["Material","Country", "Region"]] = df["Material"].str.split('-', expand=True)
    >>> # sort columns into more logical order
    >>> df = df[['Material','Country', 'Region', 'Date', 'Quantity']]
    >>> # delete random periods as actual data a likely to be incomplete
    >>> df = df.drop(np.random.choice(len(df),(int(len(df)/2))))
    >>>
    >>> Out[1]:
        >>>     Material Country    Region	Date	    Quantity
        >>> 0	0102	    19	    00004	2020-01	    1163.0
        >>> 2	0102	    19	    00004	2020-03	    641.0
        >>> 3	0102	    19	    00004	2020-04	    1642.0
        >>> 4	0102	    19	    00004	2020-05	    972.0
        >>> 5	0102	    19	    00004	2020-06	    721.0
        >>> ...	...	    ...	    ...	        ...	     ...
        >>> 110	0459	    18	    00004	2020-03	    419.0
        >>> 111	0459	    18	    00004	2020-04	    746.0
        >>> 112	0459	    18	    00004	2020-05	    1409.0
        >>> 116	0459	    18	    00004	2020-09	    1835.0
        >>> 119	0459	    18	    00004	2020-12	    1057.0   
    >>> In [2]:
    >>> result = aio.yz_analysis(
    >>>        df=df,primary_dimension_keys=["Material","Country", "Region"],
    >>>        relevant_numeric_dimension="Quantity", 
    >>>        relevant_date_dimension="Date",
    >>>        periods=12,
    >>>        start_date="2020-01-01",
    >>>        frequency="M"
    >>>        )
    >>> result.head()
    >>> Out [2]:
    >>> 	Mean	    Standard_Deviation	Non_Zero_Count	Coefficient_of_Variation 	Relative_Non_Zero_Period_Count	XYZ_Class	Frequency_Class Material Country Region
    >>> 0	592.500000	637.290358	        6	            1.075596	                0.500000                   Z	        Medium	        0008     08       00002
    >>> 1	604.833333	586.178662	        7	            0.969157	                0.583333                   Y	        Medium	        0102     19       00004
    >>> 2	475.000000	619.921109	        5	            1.305097	                0.416667                   Z	        Medium	        0402     02       00002
    >>> 3	561.583333	676.746959	        6	            1.205070	                0.500000                   Z	        Medium	        0459     18       00004
    >>> 4	327.333333	516.059780	        4	            1.576557	                0.333333                   Z	        Low             0498     16       00002
    """
    # create key
    if type(primary_dimension_keys)==list:
        df["key"] = df[primary_dimension_keys].apply(lambda row: "~~~".join(row.values.astype(str)), axis=1)
    elif type(primary_dimension_keys)==str:
        df["key"] = df[primary_dimension_keys]
      
    # rename provided column names of input DataFrame
    d_columns = {
        relevant_numeric_dimension: "numeric_dimension",
        relevant_date_dimension: "Date"
    }
    
    df = df.rename(columns=d_columns)

    # generate list of keys for df_expanded by periods times keys
    l_keys_in_df = (
        df["key"].unique().tolist()
    )  # get a list of all the distinct keys from the input DataFrame    
    
    l_keys_in_df_x_periods = [[key] * periods for key in l_keys_in_df]
    l_keys = list(itertools.chain(*l_keys_in_df_x_periods))
    
    # construct complete DataFrame for statistical analysis
    df_expanded = pd.DataFrame(l_keys, columns=["key"])

    # generate periods ("Date") Series by key times periods
    period_range = pd.period_range(start=start_date, periods=periods, freq=frequency)
    df_periods = pd.DataFrame(period_range.to_series(name="Date").astype(str).reset_index().drop(columns=["index"]))
    
    # add ("Date") Series to df_expanded
    df_expanded["Date"] = pd.concat([df_periods ]*len(l_keys_in_df), ignore_index=True)

    # aggregate input DataFrame to deal with > 1 record per period
    df = df.groupby(["key","Date"]).sum()

    # merge DataFrames (df & df_expanded) & fillna to prepare statisitcal analysis
    df_expanded = df_expanded.merge(
        df, left_on=["key", "Date"], right_on=["key", "Date"], how="outer"
    )
    # fill NaN values with 0 for statistical analysis
    df_expanded["numeric_dimension"] = df_expanded["numeric_dimension"].fillna(0)

    # statistical analysis as preparation for classification
    df_return = pd.DataFrame()
    df_return = (
        df_expanded.groupby("key")
        .agg(["mean", "std"])
        .reset_index()
        .rename(
            columns={
                "numeric_dimension.mean": "Mean",
                "numeric_dimension.std": "Standard_Deviation",
            }
        )
        .reset_index()
    )
  
    df_return.columns = ["index", "key", "Mean", "Standard_Deviation"]
    
    df_return = df_return.merge(
        df_expanded.groupby("key")["numeric_dimension"]
        .apply(lambda x: (x > 0).sum())
        .reset_index(name="Non_Zero_Count"),
        left_on="key",
        right_on="key",
        how="outer",
    )

#     df_return["Coefficient_of_Variation"] = (df_return["Standard_Deviation"]) / (
#         df_return["Mean"]
#     )

    df_return["Coefficient_of_Variation"] = np.where(df_return["Mean"] <= 0, float("NaN") , (df_return["Standard_Deviation"]) / (
        df_return["Mean"]
    ))
    
    df_return["Relative_Non_Zero_Period_Count"] = df_return["Non_Zero_Count"] / periods
    df_return = df_return.drop(columns=["index"])

    # prepare XYZ classification thresholds and classes
  
    class_thresholds_xyz = [
        (df_return["Coefficient_of_Variation"].isna()),
        (
            (df_return["Coefficient_of_Variation"] > 0) &
            (df_return["Coefficient_of_Variation"] <= X)
         ),
        (
            (df_return["Coefficient_of_Variation"] > X)
            & (df_return["Coefficient_of_Variation"] <= Y)
        ),
        (df_return["Coefficient_of_Variation"] > Y)
    ]
    class_values_xyz = ["N","X", "Y", "Z"]
    
    # classify XYZ
    df_return["XYZ_Class"] = np.select(class_thresholds_xyz, class_values_xyz)

    # prepare frequency classification thresholds and classes
    class_thresholds_freq = [
        (df_return["Relative_Non_Zero_Period_Count"] <= L),
        (
            (df_return["Relative_Non_Zero_Period_Count"] > L)
            & (df_return["Relative_Non_Zero_Period_Count"] <= M)
        ),
        (df_return["Relative_Non_Zero_Period_Count"] > M),
    ]
    class_values_freq = ["Low", "Medium", "High"]

    # classify frequency
    df_return["Frequency_Class"] = np.select(class_thresholds_freq, class_values_freq)

    # bring back inputed dimensions names for better understandable output
    df_return[primary_dimension_keys] = df_return["key"].str.split("~~~", expand=True)
    df_return = df_return.drop(columns="key")

    return df_return