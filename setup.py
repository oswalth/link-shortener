import sqlite3

def launch_db():
  db = sqlite3.connect('messages.db') 
  sql = db.cursor()

  sql.execute("""CREATE TABLE IF NOT EXISTS ShortLink (
                  id INTEGER PRIMARY KEY,
                  chat_id TEXT,
                  link TEXT,
                  shortened_link TEXT,
                  sent_at TIMESTAMP
  )""")

  db.commit()
  db.close()
  

if __name__ == "__main__":
  launch_db()