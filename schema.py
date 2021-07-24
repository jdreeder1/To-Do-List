#Using PostgreSQL
import os
from dotenv import load_dotenv
load_dotenv()
import psycopg2

postgresql_uri = os.environ.get("POSTGRES_URI")

connection = psycopg2.connect(postgresql_uri)

try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DROP TABLE IF EXISTS users CASCADE;
                CREATE TABLE users(
                    email VARCHAR(64) PRIMARY KEY NOT NULL,
                    fname VARCHAR(64) NOT NULL,
                    lname VARCHAR(64) NOT NULL,
                    password VARCHAR(32) NOT NULL,
                    timeStamp TIMESTAMPTZ
                );"""
            )
except psycopg2.errors.DuplicateTable:
    pass

try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
"""
DROP TABLE IF EXISTS lists;
CREATE TABLE lists(
        list_id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
        email VARCHAR(64) NOT NULL, 
        list_name VARCHAR(32) NOT NULL UNIQUE,
        tasks VARCHAR(255) NOT NULL,
        timeStamp TIMESTAMPTZ,
        CONSTRAINT fk_owner
            FOREIGN KEY(email) 
	            REFERENCES users(email)
                    ON DELETE CASCADE
    );"""
            )
except psycopg2.errors.DuplicateTable:
    pass

try:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
"""CREATE OR REPLACE FUNCTION udf_GetRowsByPageNumberAndSize(
 PageNumber INTEGER = NULL,
 PageSize INTEGER = NULL
 )
 RETURNS SETOF users AS
 $BODY$
 BEGIN
  RETURN QUERY
   SELECT *
   FROM users
   ORDER BY timestamp DESC
   LIMIT PageSize
   OFFSET ((PageNumber-1) * PageSize);
END;
$BODY$
LANGUAGE plpgsql;"""
            )
except psycopg2.errors.DuplicateTable:
    pass