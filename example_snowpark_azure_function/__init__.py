
# Example Azure function which leverages Snowpark for Python 
# sessions to execute queries in Snowflake

## Import Azure packages
import logging
import azure.functions as func

## Import shared packages

from ..shared.interworks_snowpark.interworks_snowpark_python.snowpark_session_builder import build_snowpark_session_via_environment_variables as build_snowpark_session

## Define main function for Azure
def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info("HTTP trigger received a new request")
  
  try:

    ### Create Snowflake Snowpark session 
    snowpark_session = build_snowpark_session()

    ### Execute various SQL commands
    snowpark_session.sql("CREATE WAREHOUSE IF NOT EXISTS GENERAL").collect()
    snowpark_session.sql("USE SCHEMA CONTROL_TABLE_EXAMPLE").collect()

    ### Execute a SQL command and store the results in a pandas dataframe
    sf_df_results = snowpark_session.sql("SELECT * FROM CONTROL_TABLE").collect()
    df_results = sf_df_results.to_pandas()

    ### Close the Snowflake Snowpark Session
    snowpark_session.close()

    return func.HttpResponse(f"Complete")

  except Exception as e:
    
    logging.info(f"Manual log - Error encountered")
    logging.info(e)
    return  func.HttpResponse(f"Error encountered")