import os
import aio

dbutils = None


def vault_get_secret(
    scope: str,
    key: str,
    databricks=None,
) -> str:
    """Get a secret from an Azure Key Vault

    This function takes a secret by using either Databricks ``dbutils`` or Azure Python API libraries

    Parameters
    ----------
    scope : str
        The scope used to get the key. If the function is running on Databricks, it is a Databricks Secret Scope, otherwise it is an Azure Key Vault name.
    key : str
        The name of the secret in a Databricks Secret Scope or Azure Key Vault


    Returns
    -------
    str
        Returns the secret as a string
    """

    if aio._is_running_on_databricks():
        return dbutils.secrets.get(scope=scope, key=key)
    elif aio._is_running_on_devops_pipeline():
        key_right_format = key.upper().replace("-", "_")
        return os.environ[key_right_format]
    else:
        from azure.keyvault.secrets import SecretClient
        from azure.identity import AzureCliCredential

        credential = AzureCliCredential()
        vault_url = f"https://{scope}.vault.azure.net/"
        client = SecretClient(vault_url=vault_url, credential=credential)
        return client.get_secret(key).value


def _vault_set_dbutils(dbutils_var: str):
    """Allows the vault functions to use the ``dbutils`` variable

    Parameters
    ----------
        dbutils_var
            ``dbutils`` variable from Databricks should be passed here

    This function sets the variable ``dbutils`` to be used when running Databricks scripts.
    """

    global dbutils
    dbutils = dbutils_var


def _is_running_on_devops_pipeline():
    """Tests if a script is running on an Azure DevOps pipeline

    Returns
    -------
    res : bool
        True, if program is running on an Azure DevOps pipeline, False otherwise.
    """
    try:
        assert isinstance(os.environ["SYSTEM_JOBID"], str)
        res = True
    except KeyError as e:
        res = False
    return res


def _is_running_on_databricks():
    """Tests if a script is running locally or on Databricks

    Returns
    -------
    res : bool
        True, if program is running on Databricks, False otherwise.
    """
    try:
        dbutils.fs
        res = True
    except AttributeError as e:
        res = False
    return res
