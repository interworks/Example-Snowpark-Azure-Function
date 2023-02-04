
# Example Azure function which retrieves the following
# three app settings and uses them to create a secret value
# in Azure key vault:
# - AZURE_KEY_VAULT_NAME
# - SNOWFLAKE_USER - This will act as the name of the secret in the Azure key vault
# - SNOWFLAKE_PRIVATE_KEY_PLAIN_TEXT

## Import Azure packages
import logging
import azure.functions as func
from azure.keyvault.secrets import SecretClient
from azure.identity import ManagedIdentityCredential

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
    ## Replace underscores with hyphens, as underscores
    ## are expected in Snowflake service account usernames
    ## but secrets in key vault cannot contain underscores
    snowflake_user = os.getenv("SNOWFLAKE_USER")
    protected_snowflake_user = snowflake_user.replace("_", "-")

    ## Retrieve new secret value, which is the
    ## private key in multi-line form
    snowflake_private_key_plain_text = os.getenv("SNOWFLAKE_PRIVATE_KEY_PLAIN_TEXT")

    ## Leverage managed identity to retrieve key vault secrets client
    managed_identity_credential = ManagedIdentityCredential()
    secret_client = SecretClient(vault_url=key_vault_uri, credential=managed_identity_credential)

    ## Retrieve the secret password from the key vault
    secret_client.set_secret(protected_snowflake_user, snowflake_private_key_plain_text)

    return func.HttpResponse("Success")

  except Exception as e:
    
    logging.info(f"Manual log - Error encountered")
    logging.info(e)
    return  func.HttpResponse(f"Error encountered")
