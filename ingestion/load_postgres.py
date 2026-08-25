from dotenv import load_dotenv
import os

from sqlalchemy import (    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Numeric)

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

engine= create_engine( 
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"
)

    
    
metadata= MetaData(schema="raw")

customers_table= Table(
    "customers",
    metadata,
    Column("_id", String, primary_key=True),
    Column("customer_id", Integer),
    Column("first_name", String),
    Column("last_name", String),
    Column("email", String),
    Column("city", String),
    Column("age", Integer),
    Column("created_at", String),
)

sales_table = Table(
    "sales",
    metadata,
    Column("_id", String, primary_key=True),
    Column("order_id", Integer),
    Column("customer_id", Integer),
    Column("product_id", Integer),
    Column("product_name", String),
    Column("category", String),
    Column("quantity", Integer),
    Column("unit_price", Numeric),
    Column("order_date", String),
    Column("payment_method", String),
)

metadata.create_all(engine)

from pymongo import MongoClient

mongo_client = MongoClient(
    "mongodb://root:example@localhost:27017/?authSource=admin"
)

mongo_db = mongo_client["source_db"]

mongo_customers = mongo_db["customers"]

customers = list(mongo_customers.find())

for customer in customers:
    customer["_id"] = str(customer["_id"])

mongo_sales = mongo_db["sales"]

sales = list(mongo_sales.find())

for sale in sales:
    sale["_id"] = str(sale["_id"])

with engine.begin() as connection:
    connection.execute(customers_table.delete())
    connection.execute(customers_table.insert(), customers)

    connection.execute(sales_table.delete())
    connection.execute(sales_table.insert(), sales)

print(f"{len(customers)} customers yazildi")
print(f"{len(sales)} sales yazildi")