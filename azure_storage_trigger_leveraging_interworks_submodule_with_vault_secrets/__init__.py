
# Example Azure function which creates a Snowpark
# for Python session leveraging the InterWorks
# submodule to execute a demonstration SELECT
# statement with the contents of a file
# uploaded to blob storage

## Import Azure packages
import logging
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

## Import other packages
import os
import json
from io import BytesIO

## Import shared packages
from ..submodules.interworks_snowpark.interworks_snowpark_python.snowpark_session_builder import build_snowpark_session_using_stored_private_key_in_azure_secrets_vault as build_snowpark_session

## Define function to retrieve the desired
## information from the input message
def parse_input_message(msg: func.QueueMessage):

  ### Retrieve message as JSON
  msg_json = msg.get_json()
  logging.info('Message JSON:')
  logging.info(msg_json)
  
  ### Retrieve message ID
  msg_id = msg_json["id"]
  logging.info(f'Message ID: {msg_id}')

  ### Retrieve full file URL from input blob.
  ### The specific key varies depending on the type
  ### of storage container
  if "url" in msg_json["data"] :
    file_path_url = msg_json["data"]["url"]
  elif "blobUrl" in msg_json["data"] :
    file_path_url = msg_json["data"]["blobUrl"]
  else :
    logging.error("Function abort - Path URL does not match expected storage blob service URI")
    raise ValueError("Function abort - Path URL does not match expected storage blob service URI")
  
  logging.info(f'File path URL: {file_path_url}')
  
  '''
  Expected file URL format:
  https://<storage account>.blob.core.windows.net/<container>/path/to/file.json
    
  Example expected file URL:
  https://my-storage-account.blob.core.windows.net/automated-function-trigger-demo/example_file.json
  '''

  ### Retrieve storage blob service uri
  storage_blob_service_uri = os.getenv("AZURE_STORAGE_IDENTITY__blobServiceUri")

  ### Parse storage queue service URI from file path URL
  if file_path_url.startswith(storage_blob_service_uri) :
    file_path = file_path_url[1 + len(storage_blob_service_uri):]
  else :
    logging.info(f'Function abort - Path URL does not match expected storage blob service URI')
    return
  
  ### Split file path into container and relative file path
  container, relative_file_path = file_path.split('/', 1)

  return storage_blob_service_uri, container, relative_file_path

## Define generic function to create an Azure blob storage client
def azure_retrieve_blob_client(storage_blob_service_uri=None, container=None, target_file_path=None):
  """
  Retrieve an Azure blob client object
  Keyword arguments:
  storage_blob_service_uri -- the uri for the blob storage service (default None)
  container -- the container name (default None)
  target_file_path -- the filepath to that will be leveraged by the blob client (default None)
  
  eg: azure_retrieve_blob_client(storage_blob_service_uri="https://my-storage-account.blob.core.windows.net", container="my-container", target_file_path="my/target/file/path.json")
  """
  logging.info(f'Manual log - Beginning retrieval of blob client')
  try:
    if all([storage_blob_service_uri, container, target_file_path]):
      
      default_azure_credential = DefaultAzureCredential()
      blob_service_client = BlobServiceClient(storage_blob_service_uri, credential=default_azure_credential)
      blob_client = blob_service_client.get_blob_client(container=container, blob=target_file_path)
      logging.info(f'Manual log - Concluded retrieval of blob client')
      return blob_client
    else:
      logging.error(f'Manual log - Aborting retrieval of blob client as function input is missing')
      raise ValueError('Aborting retrieval of blob client as function input is missing')
      
  except Exception as e:
    logging.error(f'Manual log - Error retrieving blob client')
    logging.error(e)
    raise ValueError(f"Error retrieving blob client:\n{e}\n")
    
## Define function to download full JSON file from blob
def azure_download_json_file(storage_blob_service_uri=None, container=None, relative_file_path=None):
  """
  Download JSON file from Azure Blob Storage for given container
  Keyword arguments:
  storage_blob_service_uri -- the uri for the blob storage service (default None)
  container -- the container name (default None)
  download_file_path -- the filepath to download from in the blob (default None)
  
  eg: azure_download_json_file(storage_blob_service_uri="https://my-storage-account.blob.core.windows.net", container="my-container", relative_file_path="my/target/file/path.json")
  """
  logging.info(f'Manual log - Beginning download of JSON file')
  try:
    if all([storage_blob_service_uri, container, relative_file_path]):
      blob_client = azure_retrieve_blob_client(storage_blob_service_uri=storage_blob_service_uri, container=container, target_file_path=relative_file_path)
      with BytesIO() as input_blob:
        blob_client.download_blob().download_to_stream(input_blob)
        input_blob.seek(0)
        json_input = json.load(input_blob)
      logging.info(f'Manual log - Concluding download of JSON file')
      return json_input
    else:
      logging.error(f'Manual log - Aborting download of JSON file as function input is missing')
      raise ValueError('Aborting download of JSON file as function input is missing')
      
  except Exception as e:
    logging.error(f'Manual log - Error downloading JSON file')
    logging.error(e)
    raise ValueError(f"Error downloading JSON file:\n{e}\n")
  
## Define function that retrieve the SQL statement
## to execute from the JSON input
def retrieve_sql_statement_to_execute(json_input: dict):

  '''
  Expected format of JSON file:
  json_input = {
    "sql_statement_to_execute" : "<sql_statement_to_execute>"
  }
  '''

  ### Error if JSON file is not in expected format
  if "sql_statement_to_execute" not in json_input.keys() :
    logging.error(f"Manual log - Downloaded file did not include the key 'sql_statement_to_execute'")
    raise ValueError("Manual log - Downloaded file did not include the key 'sql_statement_to_execute'")

  ### Retrieve the value as its own variable
  sql_statement_to_execute = json_input["sql_statement_to_execute"]

  return sql_statement_to_execute
  
## Define function that executes given SQL in Snowflake
def execute_sql_in_snowflake(sql_statement_to_execute: str):
  try:

    ### Create Snowflake Snowpark session 
    snowpark_session = build_snowpark_session()

    ### Execute the SQL command in Snowflake
    ### and log the result
    sf_df_statement_result = snowpark_session.sql(sql_statement_to_execute).collect()
    
    logging.info("SQL statement result:")
    logging.info(sf_df_statement_result)

    ### Close the Snowflake Snowpark Session
    snowpark_session.close()
    
    return

  except Exception as e:
    
    logging.error(f"Manual log - Error encountered")
    logging.error(e)
    raise

## Define main function for Azure
def main(msg: func.QueueMessage):
  logging.info('Received new message from queue')
  logging.info(msg)

  ### Parse the input message for required information
  storage_blob_service_uri, container, relative_file_path = parse_input_message(msg)

  ### Retrieve JSON input from Azure storage
  json_input = azure_download_json_file(storage_blob_service_uri=storage_blob_service_uri, container=container, relative_file_path=relative_file_path)

  ### Retrieve the value as its own variable
  sql_statement_to_execute = retrieve_sql_statement_to_execute(json_input)
  
  ### Attempt to execute the SQL in Snowflake
  execute_sql_in_snowflake(sql_statement_to_execute)
   
  return
