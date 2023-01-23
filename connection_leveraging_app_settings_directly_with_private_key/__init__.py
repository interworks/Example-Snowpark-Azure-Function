
# Example Azure function which leverages Snowpark for Python 
# sessions to execute queries in Snowflake, authenticating
# via key pair

## Import Azure packages
import logging
import azure.functions as func

## Import Snowpark session module
from snowflake.snowpark import Session

## Import packages with which to parse the private key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

## Import other packages
import os
import pandas
import json

## Function to retrieve the private key
## from app settings and serialize it
## for Snowpark for Python
def retrieve_serialized_private_key() :

  ### Retrieve the private key from app settings
  private_key_plain_text = os.getenv("SNOWFLAKE_PRIVATE_KEY_PLAIN_TEXT")

  ### Encode the private key
  private_key_encoded = private_key_plain_text.encode()
  
  ### Retrieve the private key passphrase from app settings
  private_key_passphrase = os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")
  
  ### Encode the private key passphrase if it has been provided
  private_key_passphrase_encoded = None
  if private_key_passphrase is not None :
    if len(private_key_passphrase) > 0 and private_key_passphrase != "None" :
      private_key_passphrase_encoded = private_key_passphrase.encode()
  
  ### Load the private key, leveraging passphrase if needed
  private_key_loaded = serialization.load_pem_private_key(
      private_key_encoded
    , password = private_key_passphrase_encoded
    , backend = default_backend()
  )
  
  ## Serialize loaded private key
  private_key_serialized = private_key_loaded.private_bytes(
      encoding = serialization.Encoding.DER
    , format = serialization.PrivateFormat.PKCS8
    , encryption_algorithm = serialization.NoEncryption()
  )

  return private_key_serialized

## Define main function for Azure
def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info("HTTP trigger received a new request")
  
  try:

    ### Retrieve the serialized private key    
    private_key_serialized = retrieve_serialized_private_key()

    ### Retrieve connection parameters from app settings
    snowflake_connection_parameters = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT")
      , "user": os.getenv("SNOWFLAKE_USER")
      , "private_key": private_key_serialized
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
