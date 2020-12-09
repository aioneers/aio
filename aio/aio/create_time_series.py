import pandas as pd
import numpy as np
import datetime
from scipy.stats import norm, uniform, poisson


def create_time_series(
    distribution="uniform",
    p_mean=10,
    p_std=1,
    num_periods=365,
    periodicity="D",
    start_date="2020-01-01",
    actual_material_number="Mat-ID-generated",
    standard_price=1,
    intermittency=0,
):
    """Creates a time series with a given distribution

    Parameters
    ----------
    distribution : str = "uniform"
        const | p_mean, normal | p_mean, p_std, uniform | p_mean, p_std or poisson | p_mean

    num_periods : int = 365
        number of increments the time series must be created for

    start_date : str = "2020-01-01"
        reference start date | format yyyy-mm-dd

    actual_material_number : str = "Mat-ID-generated"
        any material identifier

    standard_price : int = 1
        any float/integer value as price of 1 quantity unit

    intermittency : float = 0.0
        percentage of quantity data points = 0 | range 0 to 1, format e.g. 0.4 ~ 40 %

    Examples
    --------
    >>> df = pd.DataFrame()
    >>> # create random time-series with aio.create_time_series function
    >>> for i in range(100):
    >>>     quantities = aio.create_time_series(
    >>>         distribution="normal",
    >>>         p_mean=1000,
    >>>         p_std=300,
    >>>         num_periods=12,
    >>>         periodicity="M",
    >>>         start_date="2020-01-01",
    >>>         actual_material_number=str("{:04d}".format(np.random.randint(1000)))
    >>>         + str("-")
    >>>         + str("{:02d}".format(np.random.randint(20)))
    >>>         + str("-")
    >>>         + str("{:05d}".format(np.random.randint(5))),
    >>>         standard_price=1,
    >>>         intermittency=0.2,
    >>>     )
    >>>     df = df.append(quantities)
    >>> df.head()
    """

    df = pd.DataFrame(columns=["Material", "Date", "Value", "Quantity", "KEY"])

    if distribution == "const":  # constant
        quantity = np.full((num_periods), p_mean)
    elif distribution == "normal":  # normal distributed mean = P1, standard dev = P2
        quantity = np.round(norm.rvs(p_mean, p_std, size=num_periods))
    elif (
        distribution == "uniform"
    ):  # uniform distributed between min = P1, max = P1 + P2
        quantity = np.round(uniform.rvs(p_mean, p_std, size=num_periods))
    elif distribution == "poisson":  # Poisson distributed  mean = P1
        quantity = np.round(poisson.rvs(p_mean, size=num_periods))
    else:
        raise Exception("Distribution expected: const, normal, uniform or poisson")
    try:
        base_date = datetime.date.fromisoformat(start_date)
    except:
        raise Exception("Date format expected: yyyy-mm-dd")

    df["Quantity"] = quantity

    df.loc[df["Quantity"].sample(frac=intermittency).index] = 0

    df["Date"] = pd.date_range(base_date, periods=num_periods, freq="D")

    df["Value"] = df["Quantity"] * standard_price

    df["KEY"] = actual_material_number
    df["Material"] = actual_material_number

    return df