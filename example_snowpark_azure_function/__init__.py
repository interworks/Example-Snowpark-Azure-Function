
# Example Azure function which leverages Snowpark for Python 
# sessions to execute queries in Snowflake

## Import Azure packages
import logging
import azure.functions as func

## Import other packages
import pandas

## Import shared packages
from ..submodules.interworks_snowpark.interworks_snowpark_python.snowpark_session_builder import build_snowpark_session_via_environment_variables as build_snowpark_session

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

    return func.HttpResponse(f"Complete")

  except Exception as e:
    
    logging.info(f"Manual log - Error encountered")
    logging.info(e)
    return  func.HttpResponse(f"Error encountered")