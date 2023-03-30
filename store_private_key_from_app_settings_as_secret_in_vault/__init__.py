
# Example Azure function which retrieves the following
# three app settings and uses them to create a secret value
# in Azure key vault:
# - AZURE_KEY_VAULT_NAME
# - SNOWFLAKE_USER - This will identify the relevant secret in the Azure key vault
# - SNOWFLAKE_PRIVATE_KEY_PLAIN_TEXT

## Import Azure packages
import logging
import azure.functions as func
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

## Import other packages
import os

## Define main function for Azure
def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.info("HTTP trigger received a new request")
  
  try:

    ## Retrieve key vault name from app settings
    ## and convert it into a URI
    key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net"

    ## Retrieve secret name from app settings.
    snowflake_user = os.getenv("SNOWFLAKE_USER")

    ### Create name of desired secret
    private_key_secret_name = f"{snowflake_user}__private_key"

    ## Replace underscores with hyphens, as underscores
    ## are expected in Snowflake service account usernames
    ## but secrets in key vault cannot contain underscores
    protected_private_key_secret_name = private_key_secret_name.replace("_", "-")

    ## Retrieve new secret value, which is the
    ## private key in multi-line form
    snowflake_private_key_plain_text = os.getenv("SNOWFLAKE_PRIVATE_KEY_PLAIN_TEXT")

    ## Leverage managed identity to retrieve key vault secrets client
    default_azure_credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=key_vault_uri, credential=default_azure_credential)

    ## Retrieve the secret password from the key vault
    secret_client.set_secret(protected_private_key_secret_name, snowflake_private_key_plain_text, content_type="private key")

    return func.HttpResponse("Success")

  except Exception as e:
    
    logging.info(f"Manual log - Error encountered")
    logging.info(e)
    return  func.HttpResponse(f"Error encountered")
