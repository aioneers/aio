from .abc_analysis import abc_analysis
from .xyz_analysis import xyz_analysis
from .create_time_series import create_time_series


def set_dbutils(dbutils_var):
    """Allows the vault functions to use the ``dbutils`` variable

    Parameters
    ----------
        dbutils_var
            `dbutils` variable from databricks should be passed here
    """
    vault_set_dbutils(dbutils_var)
