import os
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

# 請將這裡的連線資訊修改為你們自己的 PostgreSQL 設定
DB_HOST = "localhost"
DB_NAME = "practice"  # 記得改成你們開的資料庫名稱
DB_USER = "postgres"
DB_PASSWORD = "1234"  # 記得改成你們的密碼
DB_PORT = "5432"


def get_db_connection():
  conn = psycopg2.connect(
      host=DB_HOST,
      database=DB_NAME,
      user=DB_USER,
      password=DB_PASSWORD,
      port=DB_PORT,
      cursor_factory=RealDictCursor,  # 讓查詢結果可以直接轉成字典格式，方便回傳 JSON
  )
  return conn