"""
# The MIT License (MIT)

Copyright © `2020` `aioneers GmbH`

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the “Software”), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""


import numpy as np


def abc_analysis(
    df,
    primary_dimension,
    numeric_dimension,
    secondary_dimensions=None,
    A=0.8,
    B=0.95,
    classified_only=False,
):
    """
    Multi-Dimensional ABC Analysis provides ABC classification for a mutli-dimensional, granular input.

    Parameters
    ----------
    df : Pandas.DataFrame
        DataFrame holding the object to be classified, if applicable additional secondary_dimensions, and
        numeric values used for classification, e.g.

        df.columns = ["product", "country", "quantity"].

    primary_dimension : string
        Column name in input DataFrame holding object to be classified, e.g. product.

    secondary_dimension : list of strings = None
        List of columns names in input DataFrame holding additional attributes of primary_dimension to
        structure classification on a more granular level, e.g. country, region, city

    numeric_dimension : string
        Column name in input DataFrame holding numeric values to be used for classification.

    A : float = 0.8
        Threshold for classification.

    B : float = 0.95
        Threshold for classification.

    classified_only : bool = False
        Provides DataFrame with columns primary_dimension, secondary_dimension, numeric_dimension and class
        in originally provided naming.

    Returns
    -------
    df_grouped : Pandas.DataFrame
        input DataFrame grouped by provided master- & secondary dimensions with respective
        classification and cumulative values.

    Examples
    --------
    >>> import aio
    >>> # create sample data
    >>> products, quantities = {}, {}
    >>> np.random.seed(seed=0)
    >>> for i in range(1000):
    >>>     products[i] = "{:04d}".format(np.random.randint(15))
    >>>     quantities[i] = np.random.randint(1000)
    >>> # prepare sample data DataFrame
    >>> df = pd.DataFrame()
    >>> df["Product"] = products.values()
    >>> df["Quantity"] = quantities.values()
    >>>
    >>> results = aio.abc_analysis(
    >>>     df, primary_dimension="Product", numeric_dimension="Quantity"
    >>> )
    """
    # assign input variables
    A, B = A, B

    columns = {
        primary_dimension: "primary_dimension",
        numeric_dimension: "numeric_dimension",
    }
    df = df.rename(columns=columns)

    if secondary_dimensions is None:
        df["secondary_dimension"] = "No secondary dimension provided"
    #         secondary_dimensions=["X"]
    #         return multi_dim_abc_analysis(df=df,master_dimension=master_dimension,secondary_dimensions="X",numeric_dimension=numeric_dimension)
    else:
        # aggregate secondary dimensions into one key column
        df["secondary_dimension"] = df[secondary_dimensions].agg("-".join, axis=1)

    # calculate cumsum for secondary dimension
    df_subsum = (
        df.groupby("secondary_dimension")
        .sum()
        .sort_values(by=(["secondary_dimension", "numeric_dimension"]), ascending=False)
        .reset_index()
    )

    # create return DataFrame in target grouping
    df_grouped = (
        df.groupby(["secondary_dimension", "primary_dimension"])
        .sum()
        .sort_values(by=(["secondary_dimension", "numeric_dimension"]), ascending=False)
        .reset_index()
    )

    # prepare DataFrame to calculate relative quantity
    dict_subsum = {k: list(v.values()) for k, v in df_subsum.to_dict("index").items()}
    for i in range(len(df_grouped["secondary_dimension"].unique())):
        df_grouped.loc[
            df_grouped["secondary_dimension"] == dict_subsum.get(i)[0], "Cumsum_Sec_Dim"
        ] = dict_subsum.get(i)[1]

    # calculate relative quantity
    df_grouped["Relative_Quantity"] = (
        df_grouped["numeric_dimension"] / df_grouped["Cumsum_Sec_Dim"]
    )

    # calculate cumsum relative quantity
    df_grouped["Cumsum_Relative_Quantity"] = (
        df_grouped["Relative_Quantity"]
        .groupby(df_grouped["secondary_dimension"])
        .cumsum()
    )

    # prepare ABC classification thresholds and classes
    class_thresholds = [
        (df_grouped["Cumsum_Relative_Quantity"] <= A),
        (
            (df_grouped["Cumsum_Relative_Quantity"] > A)
            & (df_grouped["Cumsum_Relative_Quantity"] <= B)
        ),
        (df_grouped["Cumsum_Relative_Quantity"] > B),
    ]
    class_values = ["A", "B", "C"]

    # disagg secondary dimension to provided names
    df_grouped[secondary_dimensions] = df_grouped["secondary_dimension"].str.split(
        "-", expand=True
    )

    # assign classes
    df_grouped["Class"] = np.select(class_thresholds, class_values)

    # rename columns back to provided names
    columns_input = dict((v, k) for k, v in columns.items())
    df_grouped = df_grouped.rename(columns=columns_input)

    # clean output before return
    if classified_only:
        df_grouped = df_grouped.drop(
            columns=[
                "Cumsum_Relative_Quantity",
                "Relative_Quantity",
                "Cumsum_Sec_Dim",
                "Cumsum_Relative_Quantity",
                "secondary_dimension",
            ]
        )

    return df_grouped