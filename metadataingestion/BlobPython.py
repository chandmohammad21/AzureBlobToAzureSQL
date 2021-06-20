from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
import pandas as pd
from IPython.display import display
import openpyxl #required for xlsx files else import xlrd
import pyodbc
from sqlalchemy import create_engine
from urllib import parse


SOURCE_FILE = 'template_client_metadata.xlsx'
DEST_FILE = 'template_client_metadata.xlsx'

AZURE_STORAGE_ACCOUNT_NAME = 'storagedata2scoops'
url = "https://{0}.blob.core.windows.net".format(
        AZURE_STORAGE_ACCOUNT_NAME)

#Setting up credentials, in case local, set environment variables - https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate
credential = DefaultAzureCredential()
blob_service_client = BlobServiceClient(
            account_url=url,
            credential=credential
        )

container_client = blob_service_client.get_container_client("data2scoops")
blob_client = container_client.get_blob_client("metadata/template_client_metadata.xlsx")

with open(DEST_FILE, "wb") as my_blob:
                download_stream = blob_client.download_blob()
                my_blob.write(download_stream.readall())

#vault end point
keyVaultName = os.environ["KEY_VAULT_NAME"]
KVUri = f"https://{keyVaultName}.vault.azure.net"

kvClient = SecretClient(vault_url=KVUri, credential=credential)
#retrieve secrets to use in application
conn = kvClient.get_secret('sqlConnectionString').value

#connection string need to be formatted in sqlalchemy engine format
quoted = parse.quote_plus(conn)

#creating engine for database connection
engine=create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))

# #reading the excel file which contains the metadata information
df = pd.read_excel("template_client_metadata.xlsx", sheet_name='Transformations')

#Ingesting the data to SQL
df.to_sql('Transformations', engine, if_exists='append', index=False) 

dfSql = pd.read_sql_table("Transformations", engine)
display(dfSql)