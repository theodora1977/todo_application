import sqlite3
conn=sqlite3.connect('app/test.db')
cur=conn.cursor()
try:
    cur.execute("PRAGMA table_info('users')")
    rows=cur.fetchall()
    print('users table columns:')
    for r in rows:
        print(r)
except Exception as e:
    print('Error:',e)
finally:
    conn.close()
