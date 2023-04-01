
# Example Azure Functions with Snowpark for Python

A collection of basic examples of Azure functions that leverage a connection to Snowpark.

## Contents

- [Example Azure Functions with Snowpark for Python](#example-azure-functions-with-snowpark-for-python)
  - [Contents](#contents)
  - [Shared InterWorks Snowpark Package](#shared-interworks-snowpark-package)
  - [Azure Functions](#azure-functions)
    - [Azure App Settings](#azure-app-settings)
      - [Azure App Setting: AZURE\_KEY\_VAULT\_NAME](#azure-app-setting-azure_key_vault_name)
      - [Azure App Setting: AZURE\_STORAGE\_IDENTITY\_\_blobServiceUri](#azure-app-setting-azure_storage_identity__blobserviceuri)
      - [Azure App Setting: AZURE\_STORAGE\_IDENTITY\_\_credential](#azure-app-setting-azure_storage_identity__credential)
      - [Azure App Setting: AZURE\_STORAGE\_IDENTITY\_\_queueServiceUri](#azure-app-setting-azure_storage_identity__queueserviceuri)
      - [Azure App Setting: SNOWFLAKE\_ACCOUNT](#azure-app-setting-snowflake_account)
      - [Azure App Setting: SNOWFLAKE\_DEFAULT\_DATABASE](#azure-app-setting-snowflake_default_database)
      - [Azure App Setting: SNOWFLAKE\_DEFAULT\_SCHEMA](#azure-app-setting-snowflake_default_schema)
      - [Azure App Setting: SNOWFLAKE\_DEFAULT\_ROLE](#azure-app-setting-snowflake_default_role)
      - [Azure App Setting: SNOWFLAKE\_DEFAULT\_WAREHOUSE](#azure-app-setting-snowflake_default_warehouse)
      - [Azure App Setting: SNOWFLAKE\_USER](#azure-app-setting-snowflake_user)
      - [Azure App Setting: SNOWFLAKE\_PRIVATE\_KEY\_PLAIN\_TEXT](#azure-app-setting-snowflake_private_key_plain_text)
      - [Azure App Setting: SNOWFLAKE\_PRIVATE\_KEY\_PASSPHRASE](#azure-app-setting-snowflake_private_key_passphrase)
      - [Azure App Setting: SNOWFLAKE\_PASSWORD](#azure-app-setting-snowflake_password)
    - [Azure Function: connection\_leveraging\_app\_settings\_directly](#azure-function-connection_leveraging_app_settings_directly)
    - [Azure Function: connection\_leveraging\_app\_settings\_directly\_with\_private\_key](#azure-function-connection_leveraging_app_settings_directly_with_private_key)
    - [Azure Function: connection\_leveraging\_app\_settings\_directly\_with\_vault\_secrets](#azure-function-connection_leveraging_app_settings_directly_with_vault_secrets)
    - [Azure Function: connection\_leveraging\_interworks\_submodule](#azure-function-connection_leveraging_interworks_submodule)
    - [Azure Function: connection\_leveraging\_interworks\_submodule\_with\_vault\_secrets](#azure-function-connection_leveraging_interworks_submodule_with_vault_secrets)
    - [Azure Function: azure\_storage\_trigger\_leveraging\_app\_settings\_directly](#azure-function-azure_storage_trigger_leveraging_app_settings_directly)
    - [Azure Function: azure\_storage\_trigger\_leveraging\_app\_settings\_directly\_with\_vault\_secrets](#azure-function-azure_storage_trigger_leveraging_app_settings_directly_with_vault_secrets)
    - [Azure Function: azure\_storage\_trigger\_leveraging\_interworks\_submodule\_with\_vault\_secrets](#azure-function-azure_storage_trigger_leveraging_interworks_submodule_with_vault_secrets)

## Shared InterWorks Snowpark Package

To simplify creating Snowpark sessions for the enclosed scripts, a custom module called "interworks_snowpark" has been used. This is contained in the "shared/interworks_snowpark" subdirectory. More details can be found in the [InterWorks Snowpark for Python GitHub repository](https://github.com/interworks/InterWorks-Snowpark-for-Python). This repository also contains instructions on how to configure your local environment for Snowpark for Python, and pairs well with this [Definitive Guide to Snowflake Sessions with Snowpark for Python](https://interworks.com/blog/2022/09/02/a-definitive-guide-to-snowflake-sessions-with-snowpark-for-python/).

## Azure Functions

This project leverages Azure Functions to trigger and execute Python scripts. To setup your local environment to modify/develop these functions, follow the guidance [here](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python).

### Azure App Settings

When deployed to Azure, this project relies on the following environment variables which should be [configured as App Settings](https://learn.microsoft.com/en-us/azure/app-service/configure-common?tabs=portal):

#### Azure App Setting: AZURE_KEY_VAULT_NAME

This is the key vault in Azure which securely stores authentication keys and passwords.

#### Azure App Setting: AZURE_STORAGE_IDENTITY__blobServiceUri

This app setting is part of a series of settings that instruct the Azure function to leverage its own managed identity when connecting to the storage container. Specifically, this is the URI of the storage account that contains the container.

Original value: `https://my-storage-account.blob.core.windows.net`

#### Azure App Setting: AZURE_STORAGE_IDENTITY__credential

This app setting is part of a series of settings that instruct the Azure function to leverage its own managed identity when connecting to the storage container and queue. Specifically, this app setting instructs the use of managed identity.

Original value: `managedidentity`

#### Azure App Setting: AZURE_STORAGE_IDENTITY__queueServiceUri

This app setting is part of a series of settings that instruct the Azure function to leverage its own managed identity when connecting to the storage queue. Specifically, this is the URI of the storage account that contains the queue.

Original value: `https://my-storage-account.queue.core.windows.net`

#### Azure App Setting: SNOWFLAKE_ACCOUNT

This is the [account identifier](https://docs.snowflake.com/en/user-guide/admin-account-identifier.html) for the Snowflake account being leveraged for the project.

#### Azure App Setting: SNOWFLAKE_DEFAULT_DATABASE

This is the database within Snowflake that is leveraged for the project.

#### Azure App Setting: SNOWFLAKE_DEFAULT_SCHEMA

This is the schema within Snowflake that is leveraged for the project.

#### Azure App Setting: SNOWFLAKE_DEFAULT_ROLE

This is the role leveraged by the service account accessing Snowflake.

#### Azure App Setting: SNOWFLAKE_DEFAULT_WAREHOUSE

This is the warehouse leveraged by the service account accessing Snowflake.

#### Azure App Setting: SNOWFLAKE_USER

This is the service account accessing Snowflake. This will be authenticated leveraging a private key of a matching name from within the Azure secrets vault.

#### Azure App Setting: SNOWFLAKE_PRIVATE_KEY_PLAIN_TEXT

This is the optional private key used to authenticate the user in Snowflake. This is only stored as plain text as this is a simple example, however it is advised to leverage managed identities and secrets vaults to access and store private keys.

#### Azure App Setting: SNOWFLAKE_PRIVATE_KEY_PASSPHRASE

This is the optional private key passphrase that pairs with the private key. As with the private key, this is only stored as plain text as this is a simple example. It is advised to leverage managed identities and secrets vaults to access and store private keys.

#### Azure App Setting: SNOWFLAKE_PASSWORD

This is the optional password used to authenticate the user in Snowflake. This will only be leveraged if a private key is not provided. This is only stored as plain text as this is a simple example, however it is advised to leverage private keys instead of passwords, along with managed identities and secrets vaults to access and store the private keys.

### Azure Function: connection_leveraging_app_settings_directly

This function is triggered directly using http and is not intended to be run regularly. The function simply establishes a connection to Snowflake using Snowpark for Python, leveraging the connection variables directly from the Azure App Settings. Most notably, this particular function expects the Snowflake user's password to be stored as plain text in the Azure App Settings.

### Azure Function: connection_leveraging_app_settings_directly_with_private_key

This function is triggered directly using http and is not intended to be run regularly. The function simply establishes a connection to Snowflake using Snowpark for Python, leveraging the connection variables directly from the Azure App Settings. Most notably, this particular function expects the Snowflake user's private key to be provided as plain text in the Azure App Settings.

### Azure Function: connection_leveraging_app_settings_directly_with_vault_secrets

This function is triggered directly using http and is not intended to be run regularly. The function simply establishes a connection to Snowflake using Snowpark for Python, leveraging the connection variables directly from the Azure App Settings. Most notably, this particular function expects the Snowflake user's private key to be stored as a secret in an Azure key vault.

### Azure Function: connection_leveraging_interworks_submodule

This function is triggered directly using http and is not intended to be run regularly. The function simply establishes a connection to Snowflake using Snowpark for Python, leveraging the connection variables directly from the Azure App Settings. Most notably, this particular function leverages the "interworks_snowpark" submodule and can accept either the Snowflake user's private key or their password, which should be provided as plain text in the Azure App Settings.

### Azure Function: connection_leveraging_interworks_submodule_with_vault_secrets

This function is triggered directly using http and is not intended to be run regularly. The function simply establishes a connection to Snowflake using Snowpark for Python, leveraging the connection variables directly from the Azure App Settings. Most notably, this particular function leverages the "interworks_snowpark" submodule and leverages a private key stored as a secret in an Azure key vault.

This function is triggered directly using http and is not intended to be run regularly. The function simply establishes a connection to Snowflake using Snowpark for Python, leveraging the connection variables directly from the Azure App Settings. Most notably, this particular function expects the Snowflake user's private key to be provided as plain text in the Azure App Settings.

### Azure Function: azure_storage_trigger_leveraging_app_settings_directly

This function is triggered by a queued message when a file is uploaded to a storage container. The function downloads the file from blob storage, expected in JSON format, and extracts a SQL statement from it. The function then establishes a connection to Snowflake using Snowpark for Python, leveraging the connection variables directly from the Azure App Settings, and executes the SQL statement. Most notably, this particular function expects the Snowflake user's password to be stored as plain text in the Azure App Settings.

### Azure Function: azure_storage_trigger_leveraging_app_settings_directly_with_vault_secrets

This function is triggered by a queued message when a file is uploaded to a storage container. The function downloads the file from blob storage, expected in JSON format, and extracts a SQL statement from it. The function then establishes a connection to Snowflake using Snowpark for Python, leveraging the connection variables directly from the Azure App Settings, and executes the SQL statement. Most notably, this particular function expects the Snowflake user's private key to be stored as a secret in an Azure key vault.

### Azure Function: azure_storage_trigger_leveraging_interworks_submodule_with_vault_secrets

This function is triggered by a queued message when a file is uploaded to a storage container. The function downloads the file from blob storage, expected in JSON format, and extracts a SQL statement from it. The function then establishes a connection to Snowflake using Snowpark for Python, leveraging the connection variables directly from the Azure App Settings, and executes the SQL statement. Most notably, this particular function leverages the "interworks_snowpark" submodule and can accept either the Snowflake user's private key or their password, which should be provided as plain text in the Azure App Settings.
