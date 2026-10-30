import os
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

# 設定資料庫連線資訊（請確認密碼是否正確，例如你的密碼是 1234 或 12345）
DB_HOST = "localhost"
DB_NAME = "practice"
DB_USER = "postgres"
DB_PASSWORD = "12345"  # 依你實際設定的密碼為主
DB_PORT = "5432"


def get_db_connection():
  conn = psycopg2.connect(
      host=DB_HOST,
      database=DB_NAME,
      user=DB_USER,
      password=DB_PASSWORD,
      port=DB_PORT,
      cursor_factory=RealDictCursor,  # 讓查詢結果可以直接轉成字典格式
  )
  return conn
