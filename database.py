import os
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

DB_HOST = "localhost"
DB_NAME = "practice"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_PORT = "5432"


def get_db_connection():
  conn = psycopg2.connect(
      host=DB_HOST,
      database=DB_NAME,
      user=DB_USER,
      password=DB_PASSWORD,
      port=DB_PORT,
      cursor_factory=RealDictCursor,
  )
  return conn