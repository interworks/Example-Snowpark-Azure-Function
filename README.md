
# Example Azure Function with Snowpark for Python

This is a basic example of an Azure function that leverages a connection to Snowpark.

## Contents

- [Example Azure Function with Snowpark for Python](#example-azure-function-with-snowpark-for-python)
  - [Contents](#contents)
  - [Shared InterWorks Snowpark Package](#shared-interworks-snowpark-package)
  - [Azure Functions](#azure-functions)
    - [Azure App Settings](#azure-app-settings)
      - [Azure App Setting: SNOWFLAKE\_ACCOUNT](#azure-app-setting-snowflake_account)
      - [Azure App Setting: SNOWFLAKE\_DEFAULT\_DATABASE](#azure-app-setting-snowflake_default_database)
      - [Azure App Setting: SNOWFLAKE\_DEFAULT\_SCHEMA](#azure-app-setting-snowflake_default_schema)
      - [Azure App Setting: SNOWFLAKE\_DEFAULT\_ROLE](#azure-app-setting-snowflake_default_role)
      - [Azure App Setting: SNOWFLAKE\_DEFAULT\_WAREHOUSE](#azure-app-setting-snowflake_default_warehouse)
      - [Azure App Setting: SNOWFLAKE\_USER](#azure-app-setting-snowflake_user)
      - [Azure App Setting: SNOWFLAKE\_PRIVATE\_KEY\_PLAIN\_TEXT](#azure-app-setting-snowflake_private_key_plain_text)
      - [Azure App Setting: SNOWFLAKE\_PRIVATE\_KEY\_PASSPHRASE](#azure-app-setting-snowflake_private_key_passphrase)

## Shared InterWorks Snowpark Package

To simplify creating Snowpark sessions for the enclosed scripts, a custom module called "interworks_snowpark" has been used. This is contained in the "shared/interworks_snowpark" subdirectory. More details can be found in the [InterWorks Snowflake Python Functionality GitHub repository](https://github.com/interworks/Snowflake-Python-Functionality). This repository also contains instructions on how to configure your local environment for Snowpark for Python, and pairs well with this [Definitive Guide to Snowflake Sessions with Snowpark for Python](https://interworks.com/blog/2022/09/02/a-definitive-guide-to-snowflake-sessions-with-snowpark-for-python/).

## Azure Functions

This project leverages Azure Functions to trigger and execute Python scripts. To setup your local environment to modify/develop these functions, follow the guidance [here](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python).

### Azure App Settings

When deployed to Azure, this project relies on the following environment variables which should be [configured as App Settings](https://learn.microsoft.com/en-us/azure/app-service/configure-common?tabs=portal):

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

This is the private key used to authenticate the user in Snowflake. This is only stored as plain text as this is a simple example, however it is advised to leveraged managed identities and secrets vaults to access and store private keys.

#### Azure App Setting: SNOWFLAKE_PRIVATE_KEY_PASSPHRASE

This is the optional private key passphrase that pairs with the private key. As with the private key, this is only stored as plain text as this is a simple example. It is advised to leveraged managed identities and secrets vaults to access and store private keys.
