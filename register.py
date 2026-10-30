import sqlite3


DB_NAME = 'app.db'

def get_db_connection():
    """建立並傳回資料庫連線"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """初始化資料庫：自動建立資料表並寫入預設測試活動"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    ''')
    
   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
   
    cursor.execute("SELECT COUNT(*) FROM events")
    if cursor.fetchone()[0] == 0:
        sample_events = [
            ("Python 基礎工作坊", "適合初學者的 Python 實作課程", "2026-11-15"),
            ("Git 協作教學", "學習 GitHub 與團隊開發流程", "2026-11-20"),
            ("網頁開發交流會", "分享前端與後端開發心得", "2026-12-01")
        ]
        cursor.executemany(
            "INSERT INTO events (title, description, date) VALUES (?, ?, ?)",
            sample_events
        )
    
    conn.commit()
    conn.close()

def show_events():
    """功能 1：讀取 events 資料表，將可報名的活動印在畫面上"""
    print("\n=================== 可報名活動清單 ===================")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, description, date FROM events")
    events = cursor.fetchall()
    
    if not events:
        print("目前沒有任何可報名的活動。")
        conn.close()
        return []
    
    print(f"{'編號':<6} | {'活動名稱':<20} | {'活動日期':<12}")
    print("-" * 50)
    for event in events:
        print(f"{event['id']:<6} | {event['title']:<20} | {event['date']:<12}")
        
    conn.close()
    return events

def register_event():
    """功能 2：製作報名表單（姓名、連絡電話），將資料寫入 registrations 資料表"""
    print("\n=================== 活動報名表單 ===================")
    
    event_id = input("請輸入欲報名的活動編號: ").strip()
    name = input("請輸入您的姓名: ").strip()
    phone = input("請輸入您的連絡電話: ").strip()
    
    if not event_id or not name or not phone:
        print("❌ 所有欄位皆為必填，報名失敗！")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO registrations (event_id, name, phone) VALUES (?, ?, ?)",
            (event_id, name, phone)
        )
        conn.commit()
        print(f"\n✅ 報名成功！感謝 {name} 的報名。")
    except sqlite3.Error as e:
        print(f"\n❌ 報名失敗，錯誤訊息：{e}")
    finally:
        conn.close()

def main():
   
    init_db()
    
    
    events = show_events()
    
    
    if events:
        choice = input("\n是否要進行報名？(y/n): ").strip().lower()
        if choice == 'y':
            register_event()
        else:
            print("已取消報名。")

if __name__ == '__main__':
    main()