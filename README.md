# Data Transfer Project: SQL Server to InfluxDB

## Project Overview

The goal of this project is to transfer data from a Microsoft SQL Server database to an InfluxDB time-series database. This setup allows us to leverage the high-performance storage and querying capabilities of InfluxDB for time-series data analysis.

## Objectives

- **Extract** data from SQL Server.
- **Transform** the data to match the schema and requirements of InfluxDB.
- **Load** the transformed data into InfluxDB.
- **Visualize** the data using InfluxDB dashboards with auto-refresh capabilities.

## Technologies Used

- **SQL Server**: Source database containing the original data.
- **SQLAlchemy**: ORM for connecting to and querying the SQL Server database.
- **InfluxDB**: Time-series database for storing and querying the transformed data.
- **InfluxDBClient**: Python client for interacting with InfluxDB.
- **Flux**: Scripting and query language for InfluxDB.
- **Python**: Programming language used to script the ETL (Extract, Transform, Load) process.

## USAGE
Use SQLAlchemy to connect to the SQL Server database and execute queries to retrieve data from the `historique` table.

### Install and run 

```
python -m venv venv
source venv/bin/activate
pip install sqlalchemy
pip install influxdb_client
python InfluxDB/transfer_influx.py
```
