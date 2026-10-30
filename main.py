from database import get_db_connection
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="廢墟版活動報名平台")


# 1. 首頁：列出可報名的活動清單 + 簡易的操作介面
@app.get("/", response_class=HTMLResponse)
def read_root():
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute("SELECT * FROM events ORDER BY id DESC;")
  events = cur.fetchall()
  cur.close()
  conn.close()

  # 組裝簡單的 HTML 畫面供測試
  html_content = """
    <html>
    <head>
        <title>廢墟版活動報名平台</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f9; }
            .card { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            input, textarea { display: block; margin: 10px 0; padding: 8px; width: 300px; }
            button { background: #007bff; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>🏚️ 廢墟版活動報名平台</h1>
        
        <div class="card">
            <h3>➕ 新增活動 (組員 A 的功能)</h3>
            <form action="/events" method="post">
                <input type="text" name="title" placeholder="活動名稱" required>
                <textarea name="description" placeholder="活動內容描述" required></textarea>
                <button type="submit">建立活動</button>
            </form>
        </div>

        <div class="card">
            <h3>📋 可報名的活動清單 (組員 B 的功能)</h3>
    """

  for event in events:
    html_content += f"""
        <div style="border-bottom: 1px solid #ddd; padding: 10px 0;">
            <h4>{event['title']} (ID: {event['id']})</h4>
            <p>{event['description']}</p>
            <form action="/register" method="post" style="background:#f9f9f9; padding:10px;">
                <input type="hidden" name="event_id" value="{event['id']}">
                <input type="text" name="name" placeholder="您的姓名" required>
                <input type="text" name="phone" placeholder="連絡電話" required>
                <button type="submit" style="background: #28a745;">點擊報名</button>
            </form>
            <p><a href="/events/{event['id']}/registrations" target="_blank">🔍 查看此活動的報名清單 (組員 C 的功能)</a></p>
        </div>
        """

  html_content += """
        </div>
    </body>
    </html>
    """
  return html_content


# 2. 新增活動 API (對應組員 A 的任務)
@app.post("/events")
def create_event(title: str = Form(...), description: str = Form(...)):
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
      "INSERT INTO events (title, description) VALUES (%s, %s)",
      (title, description),
  )
  conn.commit()
  cur.close()
  conn.close()
  return HTMLResponse(
      content="活動新增成功！<br><a href='/'>返回首頁</a>", status_code=200
  )


# 3. 填寫報名表並送出 API (對應組員 B 的任務)
@app.post("/register")
def register_event(
    event_id: int = Form(...),
    name: str = Form(..., description="姓名"),
    phone: str = Form(..., description="連絡電話"),
):
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(
      "INSERT INTO registrations (event_id, name, phone) VALUES (%s, %s, %s)",
      (event_id, name, phone),
  )
  conn.commit()
  cur.close()
  conn.close()
  return HTMLResponse(
      content="報名成功！<br><a href='/'>返回首頁</a>", status_code=200
  )


# 4. 查看特定活動的報名清單 API (對應組員 C 的任務)
@app.get("/events/{event_id}/registrations", response_class=HTMLResponse)
def get_registrations(event_id: int):
  conn = get_db_connection()
  cur = conn.cursor()

  # 取得活動名稱
  cur.execute("SELECT * FROM events WHERE id = %s;", (event_id,))
  event = cur.fetchone()

  if not event:
    raise HTTPException(status_code=404, detail="找不到此活動")

  # 取得該活動的所有報名名單
  cur.execute(
      "SELECT * FROM registrations WHERE event_id = %s;", (event_id,)
  )
  regs = cur.fetchall()

  cur.close()
  conn.close()

  html = f"""
    <html>
    <head><title>{event['title']} - 報名清單</title></head>
    <body style="font-family: Arial; margin: 40px;">
        <h2>📌 活動：{event['title']}</h2>
        <p><b>活動說明：</b>{event['description']}</p>
        <hr>
        <h3>📝 目前報名名單：</h3>
        <ul>
    """
  for r in regs:
    html += f"<li><b>姓名：</b>{r['name']} ｜ <b>電話：</b>{r['phone']}</li>"

  html += """
        </ul>
        <br><a href="/">回首頁</a>
    </body>
    </html>
    """
  return html
