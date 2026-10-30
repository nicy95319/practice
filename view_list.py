from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()


# 輔助函式：用來連接資料庫
def get_db_connection():
  conn = sqlite3.connect("database.db")
  conn.row_factory = sqlite3.Row  # 讓查詢結果可以用欄位名稱讀取
  return conn


# 查詢特定活動的報名清單
@app.get("/events/{event_id}/registrations")
def get_event_registrations(event_id: int):
  conn = get_db_connection()
  cursor = conn.cursor()

  # 1. 檢查這個活動是否存在
  event = cursor.execute(
      "SELECT * FROM events WHERE id = ?", (event_id,)
  ).fetchone()
  if not event:
    conn.close()
    raise HTTPException(status_code=404, detail="找不到這個活動")

  # 2. 從資料庫撈出該活動的所有報名資料（姓名與電話）
  registrations = cursor.execute(
      "SELECT name, phone FROM registrations WHERE event_id = ?", (event_id,)
  ).fetchall()

  conn.close()

  # 3. 整理成清單格式回傳
  result = []
  for reg in registrations:
    result.append({"name": reg["name"], "phone": reg["phone"]})

  return {
      "event_id": event_id,
      "event_title": event["title"],
      "total_registered": len(result),
      "registrations_list": result,
  }