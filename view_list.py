from database import get_db_connection
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/events/{event_id}/registrations")
def get_event_registrations(event_id: int):
  conn = get_db_connection()
  cursor = conn.cursor()

  # 注意：PostgreSQL 的參數佔位符是 %s
  cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
  event = cursor.fetchone()
  if not event:
    cursor.close()
    conn.close()
    raise HTTPException(status_code=404, detail="找不到這個活動")

  cursor.execute(
      "SELECT name, phone FROM registrations WHERE event_id = %s", (event_id,)
  )
  registrations = cursor.fetchall()

  cursor.close()
  conn.close()

  result = []
  for reg in registrations:
    result.append({"name": reg["name"], "phone": reg["phone"]})

  return {
      "event_id": event_id,
      "event_title": event["title"],
      "total_registered": len(result),
      "registrations_list": result,
  }