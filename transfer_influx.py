from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from dotenv import load_dotenv
import os
import sqlalchemy

load_dotenv()

def init_connection(sql_connexion: str):
    """
    Initializes a connection to the SQL Server database.

    Parameters:
    sql_connexion (str): The connection string for SQL Server.

    Returns:
    engine: SQLAlchemy engine object for the SQL Server connection.
    """
    connection_string = rf"{sql_connexion}"
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
    engine = create_engine(connection_url, fast_executemany=True)
    return engine

# Initialize the connection to SQL Server
sql_connexion = os.environ['SQL_CONNEXION']
engine = init_connection(sql_connexion)

# Configuration for InfluxDB connection
bucket: str = os.environ['BUCKET_INFLUX']
org: str = os.environ['ORG_INFLUX']
token: str = os.environ['TOKEN_INFLUX']
url:str = os.environ['URL_INFLUX']

print(bucket, org, token, url)
client = InfluxDBClient(url=url, token=token, org=org)

# Function to write data points to InfluxDB
def write_temperature_data(row: sqlalchemy.engine.cursor.CursorResult):
    """
    Writes a row of data to InfluxDB.

    Parameters:
    row (sqlalchemy.engine.cursor.CursorResult): A 'tuple like' containing the row data from SQL Server.
    """
    # Create a data point
    for index, col in enumerate(columns[1:], 1):
        point = Point("_historique") \
            .tag("information", "testing") \
            .field(col, row[index]) \
            .time(row[0], WritePrecision.NS)
        
        # Write the point to InfluxDB
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket=bucket, org=org, record=point)

data_query = text("SELECT * FROM Cave.dbo.historique")
colums_query = text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'historique'")

try: 
    with engine.connect() as connection:
        columns_result = connection.execute(colums_query)
        columns = [row.COLUMN_NAME for row in columns_result]
        print("columns", columns)
    
        result = connection.execute(data_query)
        
        for i, row in enumerate(result):
            if (i == 0):
                start_date = row[0]
            elif (i == len(columns) - 1):
                end_date = row[0]
            write_temperature_data(row)

    query_api = client.query_api()
    query = f'''
    from(bucket: "testBucket")
      |> range(start: 0)
      |> filter(fn: (r) => r._measurement == "_historique")
      |> filter(fn: (r) => r.information == "testing")
    '''
    tables = query_api.query(query, org=org)

    for table in tables:
        for record in table.records:
            print(f'Time: {record.get_time()}, Value: {record.get_value()}')

except Exception as e:
    print("Error", e)

finally:
    # Close the client
    client.close()
