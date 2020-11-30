import numpy as np
import aio
import pandas as pd


def test_abc_analysis_w_multiple_dimensions():
    # create sample data
    products, quantities, countries, regions, cities = {}, {}, {}, {}, {}
    np.random.seed(seed=0)
    for i in range(1000):
        products[i] = "{:04d}".format(np.random.randint(15))
        quantities[i] = np.random.randint(1000)
        countries[i] = "{:03d}".format(np.random.randint(4))
        regions[i] = "{:05d}".format(np.random.randint(3))
        cities[i] = "{:02d}".format(np.random.randint(2))
    # prepare sample data DataFrame
    df = pd.DataFrame()
    df["Product"] = products.values()
    df["Country"] = countries.values()
    df["Quantity"] = quantities.values()
    df["Region"] = regions.values()
    df["City"] = cities.values()

    results = aio.abc_analysis(
        df,
        primary_dimension="Product",
        secondary_dimensions=["Country", "Region", "City"],
        numeric_dimension="Quantity",
    )

    results[
        (results["secondary_dimension"] == "003-00002-01")
        | (results["secondary_dimension"] == "003-00002-00")
    ]
    assert len(results)


def test_abc_analysis_wo_additional_dimensions():
    # create sample data
    products, quantities = {}, {}
    np.random.seed(seed=0)
    for i in range(1000):
        products[i] = "{:04d}".format(np.random.randint(15))
        quantities[i] = np.random.randint(1000)
    # prepare sample data DataFrame
    df = pd.DataFrame()
    df["Product"] = products.values()
    df["Quantity"] = quantities.values()

    results = aio.abc_analysis(
        df, primary_dimension="Product", numeric_dimension="Quantity"
    )

    assert len(results)
