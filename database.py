import os
from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

<<<<<<< HEAD
# è«‹å°‡é€™è£¡çš„é€£ç·šè³‡è¨Šä¿®æ”¹ç‚ºä½ å€‘è‡ªå·±çš„ PostgreSQL è¨­å®š
DB_HOST = "localhost"
DB_NAME = "practice"  # è¨˜å¾—æ”¹æˆä½ å€‘é–‹çš„è³‡æ–™åº«åç¨±
DB_USER = "postgres"
DB_PASSWORD = "1234"  # è¨˜å¾—æ”¹æˆä½ å€‘çš„å¯†ç¢¼
=======
# ½Ð±N³o¸Ìªº³s½u¸ê°T­×§ï¬°§A­Ì¦Û¤vªº PostgreSQL ³]©w
DB_HOST = "localhost"
DB_NAME = "practice"  # °O±o§ï¦¨§A­Ì¶}ªº¸ê®Æ®w¦WºÙ
DB_USER = "postgres"
DB_PASSWORD = "03250801"  # °O±o§ï¦¨§A­Ìªº±K½X
>>>>>>> e0555c7b4399451fa3dfbdc01b6663e22b9fcda9
DB_PORT = "5432"


def get_db_connection():
  conn = psycopg2.connect(
      host=DB_HOST,
      database=DB_NAME,
      user=DB_USER,
      password=DB_PASSWORD,
      port=DB_PORT,
<<<<<<< HEAD
      cursor_factory=RealDictCursor,  # è®“æŸ¥è©¢çµæžœå¯ä»¥ç›´æŽ¥è½‰æˆå­—å…¸æ ¼å¼ï¼Œæ–¹ä¾¿å›žå‚³ JSON
  )
  return conn
=======
      cursor_factory=RealDictCursor,  # Åý¬d¸ßµ²ªG¥i¥Hª½±µÂà¦¨¦r¨å®æ¦¡¡A¤è«K¦^¶Ç JSON
  )
  return conn
>>>>>>> e0555c7b4399451fa3dfbdc01b6663e22b9fcda9
