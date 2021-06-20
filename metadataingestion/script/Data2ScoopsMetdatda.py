import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

import pandas as pd
from IPython.display import display
#import xlrd #required for xls files
import openpyxl #required for xlsx files
import pyodbc
from sqlalchemy import create_engine
from urllib import parse

#change mode to 'cloud' if not running locally
mode = 'cloud'

#vault end point
keyVaultName = os.environ["KEY_VAULT_NAME"]
KVUri = f"https://{keyVaultName}.vault.azure.net"

#Setting up credentials, in case local, set environment variables - https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

#retrieve secrets to use in application
conn = client.get_secret('sqlConnectionString').value
print(conn)

#In case we want to us it locally
# sqlUsername = '***'
# sqlPassword = '***'
# azureServer = 'localhost' if mode == 'local' else 'serverdata2scoops.database.windows.net'
# database = 'Data2Scoops'
# driver= '{ODBC Driver 17 for SQL Server}'
#conn = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:serverdata2scoops.database.windows.net,1433;Database=Data2Scoops;Uid=d2scoops;Pwd=Newuser123#;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


# #creating connection string based on run mode
# if mode == 'local':
#     conn = 'Driver={0};Server={1};Database={2};UID={3};PWD={4};'\
#         .format(driver, azureServer, database, sqlUsername, sqlPassword)
# else:
#     conn = 'Driver={0};Server=tcp:{1},{2};Database={3};Uid={4};Pwd={5};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'\
#     .format(driver, azureServer, 1433, database, sqlUsername, sqlPassword)

#connection string need to be formatted in sqlalchemy engine format
quoted = parse.quote_plus(conn)

#creating engine for database connection
engine=create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))

# #reading the excel file which contains the metadata information
# df = pd.read_excel("template\\template_client_metadata.xlsx", sheet_name='Transformations')

# #Ingesting the data to SQL
# df.to_sql('Transformations', engine, if_exists='append', index=False) 

#Verifying if the data is ingested correctly
df = pd.read_sql_table("Files", engine)
display(df)











