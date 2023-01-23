
# Example Azure function which leverages Snowpark for Python 
# sessions to execute queries in Snowflake

## Import Azure packages
import logging
import azure.functions as func

## Import Snowpark session module
from snowflake.snowpark import Session

## Import other packages
import os
import pandas
import json

## Define main function for Azure
def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info("HTTP trigger received a new request")
  
  try:

    ### Retrieve connection parameters from app settings
    snowflake_connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT")
      , "user": os.getenv("SNOWFLAKE_USER")
      , "password": os.getenv("SNOWFLAKE_PASSWORD")
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
