# AzureBlobToAzureSQL
### Business use case:
- An excel file is present in Azure datalake/blob storage
- Store Sql connection string and other secrets in Key Vault
- Access Storage via OAuth
- Access SQL via connection string in Key Vault
- Ingest the excel file into SQL Database using Python.

P.S. This could have been done as Azure Function in Python however purpose of this is to add this script to build pipeline to perform initial actions as part of CI/CD

OAuth :- Default credentials by saving service principal secrets in Keyvault/environment variables and then use it to authenticate.

In case we want to run this as a cloud application, simply provide rbac to this application and default credential will take care of evrything related to Authentication.

Make sure that services involved are Azure trusted service.