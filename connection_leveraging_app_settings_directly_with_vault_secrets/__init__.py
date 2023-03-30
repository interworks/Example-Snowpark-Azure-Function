
# Example Azure function which leverages Snowpark for Python 
# sessions to execute queries in Snowflake, authenticating
# with a password stored as a secret in an Azure key vault

## Import Azure packages
import logging
import azure.functions as func
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

## Import Snowpark session module
from snowflake.snowpark import Session

## Import other packages
import os
import pandas
import json

## Function to retrieve the password
## from Azure key vault using app
## settings for key variables
def retrieve_password_from_key_vault() :

  ### Retrieve key vault name from app settings
  ### and convert it into a URI
  key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
  key_vault_uri = f"https://{key_vault_name}.vault.azure.net"

  ### Retrieve password secret name from app settings
  snowflake_password_secret_name = os.getenv("SNOWFLAKE_PASSWORD_SECRET_NAME")

  ### Leverage managed identity to retrieve key vault secrets client
  default_azure_credential = DefaultAzureCredential()
  secret_client = SecretClient(vault_url=key_vault_uri, credential=default_azure_credential)

  ### Retrieve the secret password from the key vault
  snowflake_password = secret_client.get_secret(snowflake_password_secret_name).value

  return snowflake_password

## Define main function for Azure
def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info("HTTP trigger received a new request")
  
  try:

    ### Retrieve the password from the key vault    
    snowflake_password = retrieve_password_from_key_vault()

    ### Retrieve connection parameters from app settings
    snowflake_connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT")
      , "user": os.getenv("SNOWFLAKE_USER")
      , "password": snowflake_password
      , "role": os.getenv("SNOWFLAKE_ROLE")
      , "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE")
    }

    ### Create Snowflake Snowpark session 
    snowpark_session = Session.builder.configs(snowflake_connection_parameters).create()

    ### Execute a SQL command to view the databases in Snowflake
    ### and convert the results in a pandas dataframe
    sf_df_databases = snowpark_session.sql("SHOW DATABASES")
    df_databases = pandas.DataFrame(data=sf_df_databases.collect())

    ### Close the Snowflake Snowpark Session
    snowpark_session.close()
    
    logging.info('df_databases:')
    logging.info(df_databases)
    
    ### Retrieve and return list of database names
    list_database_names = df_databases["name"].to_list()
    logging.info('list_database_names:')
    logging.info(list_database_names)

    return func.HttpResponse(json.dumps(list_database_names))

  except Exception as e:
    
    logging.info(f"Manual log - Error encountered")
    logging.info(e)
    return  func.HttpResponse(f"Error encountered")
