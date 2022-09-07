from decouple import config
from peewee import PostgresqlDatabase

db = PostgresqlDatabase( # db settings for PostgreSQL
    database = config('DATABASE'),
    user = config('USER'),
    password = config('PASSWORD'),
    host = 'localhost',
    port = 5432
)