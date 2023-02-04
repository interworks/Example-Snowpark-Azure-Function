
# Example Azure function which creates a Snowpark
# for Python session leveraging the InterWorks
# submodule to retrieve and use a private key
# stored as a secret in an Azure Key Vault

## Import Azure packages
import logging
import azure.functions as func

## Import other packages
import pandas
import json

## Import shared packages
from ..submodules.interworks_snowpark.interworks_snowpark_python.snowpark_session_builder import build_snowpark_session_using_stored_private_key_in_azure_secrets_vault as build_snowpark_session

## Define main function for Azure
def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info("HTTP trigger received a new request")
  
  try:

    ### Create Snowflake Snowpark session 
    snowpark_session = build_snowpark_session()

    ### Execute a SQL command to view the databases in Snowflake
    ### and convert the results in a pandas dataframe
    sf_df_databases = snowpark_session.sql("SHOW DATABASES")
    df_databases = pandas.DataFrame(data=sf_df_databases.collect())

    ### Close the Snowflake Snowpark Session
    snowpark_session.close()
    
    logging.info('df_databases:')
    logging.info(df_databases)
    
    ### Retrieve list of database names
    list_database_names = df_databases["name"].to_list()
    logging.info('list_database_names:')
    logging.info(list_database_names)

    return func.HttpResponse(json.dumps(list_database_names))

  except Exception as e:
    
    logging.info(f"Manual log - Error encountered")
    logging.info(e)
    return  func.HttpResponse(f"Error encountered")