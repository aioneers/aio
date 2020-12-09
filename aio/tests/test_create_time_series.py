import aio
import numpy as np
import pandas as pd


def test_create_time_series():
    df = pd.DataFrame()

    # create time-series with defined distribution
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

    # @Titus: why 1200?
    assert len(df) == 1200
    print(len(df))